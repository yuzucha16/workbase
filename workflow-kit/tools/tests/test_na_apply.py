"""na_apply.py（close / due-up）の単体テスト。一時ディレクトリの小さな docs/ だけを触る。
実行: python -I -m unittest discover -s workflow-kit/tools/tests
"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import na_apply as na  # noqa: E402

LOG = """# 作業ログ（log）

説明。

## Next Actions

1. 【期日 11-13】一つ目。
2. 【期日 11-13】二つ目。
   続きの行。

4. 【起票 11-01】四つ目。

## Open Questions

- 疑問その一。
"""

HIST = """# 作業ログの経緯（log-history）

## Log

### 2026-11-01（前の日）
- 前の記録。
"""

DUE = """# 期日

| 期日 | 種別 | 内容 | 担当 |
|---|---|---|---|
| 2026-11-02 | 単発 | topic NA 1: 試行 | ユーザー |
| 2026-11-01 | 定例 | 週1の review | ユーザー |
| 2026-11-20 | 単発 | 先の行 | ユーザー |
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.log = self.dir / "log.md"
        self.hist = self.dir / "log-history.md"
        self.due = self.dir / "due.md"
        self.log.write_text(LOG, encoding="utf-8")
        self.hist.write_text(HIST, encoding="utf-8")
        self.due.write_text(DUE, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def plan(self, items, **kw):
        p = {"log": str(self.log), "date": "2026-11-02", "title": "テスト", "items": items}
        p.update(kw)
        return p

    def apply(self, plan):
        for path, lines in na.plan_close(plan):
            Path(path).write_text("\n".join(lines), encoding="utf-8", newline="")


class CloseTest(Base):
    def test_done_moves_item_to_history_and_keeps_numbers(self):
        self.apply(self.plan([{"item": 2, "kind": "done", "note": "根拠A"}]))
        log = self.log.read_text(encoding="utf-8")
        self.assertNotIn("二つ目", log)
        self.assertNotIn("続きの行", log)
        self.assertIn("4. 【起票 11-01】四つ目。", log)
        self.assertNotIn("\n\n\n", log)
        hist = self.hist.read_text(encoding="utf-8")
        self.assertIn("### 2026-11-02（テスト）\n- 済（NA2）: 根拠A\n  - 元の項目: 【期日 11-13】二つ目。 続きの行。", hist)
        self.assertLess(hist.index("2026-11-02"), hist.index("2026-11-01"))

    def test_partial_rewrites_and_keeps_marker(self):
        self.apply(self.plan([{"item": "四つ目", "kind": "partial", "note": "半分済", "rewrite": "【起票 11-01】残り。"}]))
        log = self.log.read_text(encoding="utf-8")
        self.assertIn("4. 【起票 11-01】残り。", log)
        self.assertNotIn("元の項目", self.hist.read_text(encoding="utf-8"))

    def test_open_questions_and_due_row(self):
        self.apply(self.plan([{"item": "疑問", "section": "Open Questions", "kind": "omit", "note": "不要",
                               "due_match": "topic NA 1"}], due=str(self.due)))
        self.assertNotIn("疑問その一", self.log.read_text(encoding="utf-8"))
        due = self.due.read_text(encoding="utf-8")
        self.assertNotIn("topic NA 1", due)
        self.assertIn("週1の review", due)
        self.assertIn("omit（OQ）", self.hist.read_text(encoding="utf-8"))

    def test_same_heading_appends(self):
        self.apply(self.plan([{"item": 1, "kind": "done", "note": "a"}, {"item": 2, "kind": "omit", "note": "b"}]))
        hist = self.hist.read_text(encoding="utf-8")
        self.assertEqual(hist.count("### 2026-11-02（テスト）"), 1)
        self.assertIn("（NA1）: a", hist)
        self.assertIn("（NA2）: b", hist)

    def test_existing_heading_gets_new_bullets(self):
        self.apply(self.plan([{"item": 1, "kind": "done", "note": "a"}], title="前の日", date="2026-11-01"))
        hist = self.hist.read_text(encoding="utf-8")
        self.assertEqual(hist.count("### 2026-11-01（前の日）"), 1)
        self.assertLess(hist.index("前の記録"), hist.index("（NA1）: a"))

    def test_ambiguous_or_missing_stops_without_writing(self):
        before = self.log.read_text(encoding="utf-8")
        for bad in ({"item": "【期日"}, {"item": 9}, {"item": 1, "kind": "bogus"}):
            spec = {"kind": "done", "note": "x"}
            spec.update(bad)
            with self.assertRaises(na.Stop):
                na.plan_close(self.plan([spec]))
        with self.assertRaises(na.Stop):
            na.plan_close(self.plan([{"item": 1, "kind": "done", "note": "x"}, {"item": 9, "kind": "done", "note": "y"}]))
        with self.assertRaises(na.Stop):
            na.plan_close(self.plan([{"item": 1, "kind": "partial", "note": "x"}]))
        self.assertEqual(before, self.log.read_text(encoding="utf-8"))

    def test_missing_log_section_stops(self):
        self.log.write_text("# x\n", encoding="utf-8")
        with self.assertRaises(na.Stop):
            na.plan_close(self.plan([{"item": 1, "kind": "done", "note": "x"}]))


class DueUpTest(Base):
    def run_up(self, **kw):
        out, lines, skipped = na.plan_due_up(str(self.due), str(self.log), kw.get("only", []),
                                             kw.get("nexts", []), date(2026, 11, 2))
        for path, new in out:
            Path(path).write_text("\n".join(new), encoding="utf-8", newline="")
        return lines, skipped

    def test_single_row_moves_and_numbers_continue(self):
        lines, skipped = self.run_up()
        self.assertEqual(lines, ["5. 【起票 11-02、期日 11-02】topic NA 1: 試行（担当: ユーザー）"])
        self.assertEqual(len(skipped), 1)
        log = self.log.read_text(encoding="utf-8")
        self.assertIn("4. 【起票 11-01】四つ目。\n5. 【起票 11-02", log)
        due = self.due.read_text(encoding="utf-8")
        self.assertNotIn("topic NA 1", due)
        self.assertIn("週1の review", due)
        self.assertIn("先の行", due)

    def test_recurring_with_next_rewrites_date(self):
        lines, skipped = self.run_up(nexts=[("週1", "2026-11-09")])
        self.assertEqual(skipped, [])
        self.assertEqual(len(lines), 2)
        self.assertIn("| 2026-11-09 | 定例 | 週1の review", self.due.read_text(encoding="utf-8"))

    def test_only_filters_rows(self):
        lines, _ = self.run_up(only=["試行"])
        self.assertEqual(len(lines), 1)
        self.assertIn("週1の review", self.due.read_text(encoding="utf-8"))


class CliTest(Base):
    def test_stop_exits_2_and_dry_run_writes_nothing(self):
        plan = self.dir / "plan.json"
        plan.write_text(json.dumps(self.plan([{"item": 1, "kind": "done", "note": "x"}]), ensure_ascii=False), encoding="utf-8")
        before = self.log.read_text(encoding="utf-8")
        argv = sys.argv
        sys.argv = ["na_apply.py", "close", "--plan", str(plan), "--dry-run"]
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                na.main()
        except SystemExit:
            self.fail("dry-run が止まった")
        finally:
            sys.argv = argv
        self.assertEqual(before, self.log.read_text(encoding="utf-8"))
        self.assertIn("-1. 【期日 11-13】一つ目。", out.getvalue())


if __name__ == "__main__":
    unittest.main()
