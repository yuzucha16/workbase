"""triggers 系の道具（find_knowledge.py の --triggers / --check-triggers / --check-index、triggers_hook.py、triggers_stats.py）の単体テスト。

実際の exmem/ には触れない。一時ディレクトリに小さな repo（exmem/lessons、guides/explain、exmem/inbox、exmem-index.md）を作って確かめる。
実行: python -I -m unittest discover -s workflow-kit/tools/tests
"""
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import find_knowledge as fk  # noqa: E402


def note(triggers=None, title="t"):
    front = ["---", "type: knowledge", f"title: {title}"]
    if triggers is not None:
        front.append(f"triggers: [{', '.join(triggers)}]")
    front += ["---", "", "# 本文", ""]
    return "\n".join(front)


class RepoCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.repo = self.tmp
        for d in ("exmem/lessons", "exmem/inbox", "guides/explain"):
            (self.repo / d).mkdir(parents=True)

    def write(self, rel, text):
        p = self.repo / rel
        p.write_text(text, encoding="utf-8")
        return p

    def run_fn(self, fn, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ret = fn(*args)
        return ret, buf.getvalue()


class ReadTriggersTest(RepoCase):
    def test_reads_words_and_strips_spaces(self):
        p = self.write("exmem/lessons/a.md", note(["消化", " review 消化 ", "FAIL"]))
        self.assertEqual(fk.read_triggers(p), ["消化", "review 消化", "FAIL"])

    def test_none_without_frontmatter_or_line(self):
        self.assertIsNone(fk.read_triggers(self.write("exmem/lessons/a.md", "# 見出しだけ\n")))
        self.assertIsNone(fk.read_triggers(self.write("exmem/lessons/b.md", note(None))))

    def test_handles_crlf_and_bom(self):
        p = self.repo / "exmem/lessons/c.md"
        p.write_bytes(b"\xef\xbb\xbf" + note(["語a", "語b"]).replace("\n", "\r\n").encode("utf-8"))
        self.assertEqual(fk.read_triggers(p), ["語a", "語b"])

    def test_empty_list_is_empty(self):
        self.assertEqual(fk.read_triggers(self.write("exmem/lessons/d.md", note([]))), [])


class LookupTriggersTest(RepoCase):
    def test_hits_ranked_by_word_count_and_case_insensitive(self):
        self.write("exmem/lessons/one.md", note(["消化"]))
        self.write("exmem/lessons/two.md", note(["消化", "Next Actions"]))
        _, out = self.run_fn(fk.lookup_triggers, self.repo, "review 消化 と next actions", 5)
        lines = out.strip().splitlines()
        self.assertTrue(lines[0].startswith("exmem/lessons/two.md"))
        self.assertIn("2語", lines[0])
        self.assertTrue(lines[1].startswith("exmem/lessons/one.md"))

    def test_no_hit_message(self):
        self.write("exmem/lessons/one.md", note(["消化"]))
        _, out = self.run_fn(fk.lookup_triggers, self.repo, "関係ない依頼", 5)
        self.assertTrue(out.startswith("該当なし"))

    def test_one_char_words_are_ignored(self):
        self.write("exmem/lessons/one.md", note(["a", "消"]))
        _, out = self.run_fn(fk.lookup_triggers, self.repo, "a 消 を含む", 5)
        self.assertTrue(out.startswith("該当なし"))

    def test_sources_inbox_marked_and_inbox_readme_skipped(self):
        self.write("guides/explain/g.md", note(["理解ガイド"]))
        self.write("exmem/inbox/memo.md", note(["理解ガイド"]))
        self.write("exmem/inbox/README.md", note(["理解ガイド"]))
        _, out = self.run_fn(fk.lookup_triggers, self.repo, "理解ガイドにして", 5)
        self.assertIn("guides/explain/g.md", out)
        self.assertIn("exmem/inbox/memo.md", out)
        self.assertIn("（未統合）", out)
        self.assertNotIn("README", out)

    def test_top_limits_and_reports_rest(self):
        for i in range(4):
            self.write(f"exmem/lessons/n{i}.md", note(["語語"]))
        _, out = self.run_fn(fk.lookup_triggers, self.repo, "語語", 2)
        self.assertIn("ほか 2 件", out)

    def test_substring_match_false_positive_is_current_behavior(self):
        # 部分一致の誤爆（NA 13）。「ログ」の札が「ログイン」に当たる現状を固定する。変えるときはこのテストを直す。
        self.write("exmem/lessons/log.md", note(["ログ"]))
        _, out = self.run_fn(fk.lookup_triggers, self.repo, "ログインできない", 5)
        self.assertIn("exmem/lessons/log.md", out)


class CheckTriggersTest(RepoCase):
    def test_ok(self):
        self.write("exmem/lessons/a.md", note(["x1"]))
        self.write("guides/explain/b.md", note(["y1"]))
        bad, out = self.run_fn(fk.check_triggers, self.repo)
        self.assertEqual(bad, 0)
        self.assertIn("fail=0", out)

    def test_missing_and_too_many_and_empty(self):
        self.write("exmem/lessons/none.md", note(None))
        self.write("exmem/lessons/many.md", note([f"w{i}" for i in range(fk.TRIGGERS_MAX + 1)]))
        self.write("guides/explain/empty.md", note([]))
        self.write("exmem/lessons/max.md", note([f"w{i}" for i in range(fk.TRIGGERS_MAX)]))
        bad, out = self.run_fn(fk.check_triggers, self.repo)
        self.assertEqual(bad, 3)
        self.assertIn("triggers が無い: exmem/lessons/none.md", out)
        self.assertIn(f"triggers が {fk.TRIGGERS_MAX + 1} 語", out)
        self.assertIn("guides/explain/empty.md", out)
        self.assertNotIn("max.md", out)

    def test_inbox_is_not_checked_here(self):
        self.write("exmem/inbox/memo.md", note(None))
        bad, _ = self.run_fn(fk.check_triggers, self.repo)
        self.assertEqual(bad, 0)


class CheckIndexTest(RepoCase):
    def index(self, *lines):
        self.write("exmem/exmem-index.md", "---\ntype: index\n---\n\n" + "\n".join(lines) + "\n")

    def test_ok(self):
        self.write("exmem/lessons/a.md", note(["x1"]))
        self.write("exmem/lessons/b.md", note(["y1"]))
        self.index("- [[a]]: 説明", "- [[b|別名]]: 説明")
        bad, out = self.run_fn(fk.check_index, self.repo)
        self.assertEqual(bad, 0)
        self.assertIn("索引 2 行 / lessons 2 本", out)

    def test_missing_extra_and_duplicate(self):
        self.write("exmem/lessons/a.md", note(["x1"]))
        self.write("exmem/lessons/b.md", note(["y1"]))
        self.index("- [[a]]: 説明", "- [[a]]: 重複", "- [[ghost]]: 無いノート")
        bad, out = self.run_fn(fk.check_index, self.repo)
        self.assertEqual(bad, 3)
        self.assertIn("索引に無い: b", out)
        self.assertIn("索引にあるがノートが無い: ghost", out)
        self.assertIn("索引に重複: a", out)

    def test_grouped_line_counts_only_first_link(self):
        # 1 行に [[a]] / [[b]] と並べると、先頭しか数えない（2026-10-30 に 5 件が落ちた原因）。1 ノート 1 行で書く。
        self.write("exmem/lessons/a.md", note(["x1"]))
        self.write("exmem/lessons/b.md", note(["y1"]))
        self.index("- [[a]] / [[b]]: まとめた行")
        bad, out = self.run_fn(fk.check_index, self.repo)
        self.assertEqual(bad, 1)
        self.assertIn("索引に無い: b", out)


class RealRepoTest(unittest.TestCase):
    """実際のリポジトリの点検。exmem/ が無い環境（部屋など）では飛ばす。"""

    def setUp(self):
        self.repo = TOOLS.parent.parent
        if not (self.repo / "exmem" / "lessons").is_dir():
            self.skipTest("exmem/lessons が無い")

    def test_triggers_and_index_pass(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            t = fk.check_triggers(self.repo)
            i = fk.check_index(self.repo)
        self.assertEqual((t, i), (0, 0), buf.getvalue())


class HookTest(RepoCase):
    def setUp(self):
        super().setUp()
        tools = self.repo / "workflow-kit" / "tools"
        tools.mkdir(parents=True)
        for n in ("find_knowledge.py", "triggers_hook.py"):
            shutil.copy(TOOLS / n, tools / n)
        self.hook = tools / "triggers_hook.py"
        self.write("exmem/lessons/digest.md", note(["消化"]))

    def run_hook(self, stdin):
        p = subprocess.run([sys.executable, "-I", str(self.hook)], input=stdin.encode("utf-8"), capture_output=True)
        return p.returncode, p.stdout.decode("utf-8")

    def test_prints_marker_and_hit(self):
        rc, out = self.run_hook(json.dumps({"prompt": "review 消化"}))
        self.assertEqual(rc, 0)
        self.assertTrue(out.startswith("[作業の言葉の索引]"))
        self.assertIn("exmem/lessons/digest.md", out)

    def test_silent_when_no_hit_short_prompt_or_bad_input(self):
        for stdin in (json.dumps({"prompt": "関係ない依頼です"}), json.dumps({"prompt": "消化"}), json.dumps({}), "not json", ""):
            rc, out = self.run_hook(stdin)
            self.assertEqual((rc, out.strip()), (0, ""), stdin)


class StatsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def session(self, rows):
        p = self.tmp / "s.jsonl"
        p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
        return p

    def rows(self):
        hook = "[作業の言葉の索引] 依頼に当たる知識:\nexmem/lessons/a-note.md  (4KB)  [1語: x]\nexmem/lessons/b-note.md  (4KB)  [1語: y]"
        return [
            {"type": "user", "timestamp": "2026-10-30T01:00:00Z", "message": {"content": "最初の依頼"}},
            {"type": "attachment", "attachment": {"type": "hook_success", "content": hook}},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "input": {"file_path": "C:\\w\\exmem\\lessons\\a-note.md"}}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "content": "x"}]}},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "input": {"command": "cat exmem/lessons/z-missed.md"}}]}},
            {"type": "user", "timestamp": "2026-10-29T01:00:00Z", "isMeta": True, "message": {"content": "メタ"}},
            {"type": "user", "timestamp": "2026-10-30T02:00:00Z", "isSidechain": True, "message": {"content": "サブ"}},
        ]

    def test_analyze_collects_hits_and_reads(self):
        sys.path.insert(0, str(TOOLS))
        import triggers_stats as ts
        turns = ts.analyze(self.session(self.rows()), "0000-00-00")
        self.assertEqual(len(turns), 1)  # メタ・サイドチェーン・tool_result は依頼に数えない
        self.assertEqual(turns[0]["hits"], ["exmem/lessons/a-note.md", "exmem/lessons/b-note.md"])
        self.assertIn("exmem/lessons/a-note.md", turns[0]["text"])  # バックスラッシュは / にそろう
        self.assertEqual(ts.analyze(self.session(self.rows()), "2026-10-31"), [])

    def test_cli_rates_and_missed(self):
        self.session(self.rows())
        p = subprocess.run([sys.executable, "-I", str(TOOLS / "triggers_stats.py"), "--detail", str(self.tmp)], capture_output=True)
        out = p.stdout.decode("utf-8")
        self.assertEqual(p.returncode, 0, p.stderr.decode("utf-8", "replace"))
        self.assertIn("引当率（出したノートが読まれた）: 1/2 = 50%  上位1件: 1/1 = 100%", out)
        self.assertIn("取りこぼし候補 1 件", out)
        self.assertIn("exmem/lessons/z-missed.md", out)

    def test_cli_without_hook_records(self):
        self.session([{"type": "user", "timestamp": "2026-10-30T01:00:00Z", "message": {"content": "依頼"}}])
        p = subprocess.run([sys.executable, "-I", str(TOOLS / "triggers_stats.py"), str(self.tmp)], capture_output=True)
        self.assertIn("索引が出した記録がまだ無い", p.stdout.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
