"""room.py のテスト。WSL は差し替え、一時ディレクトリの Vault（git）で `open → start → close` を通す。"""
import argparse
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import room  # noqa: E402

GITIGNORE = "**/_noai/\n~$*\n!**/ai/out/\n**/ai/ctx/\n*.tmp\n"
AREA_README = """---
status: active
boundary: internal
updated: 2026-10-01
---

# area-x

## 進行中の Project

なし。

## 次の Project の候補

なし。
"""


class FakeWsl:
    def __init__(self, distros=("room-area-x",)):
        self._distros = list(distros)
        self.mounted = False
        self.scripts = []
        self.interactive_calls = []
        self.pushes = []
        self.keepalives = []
        self.keep_procs = []
        self.on_interactive = None  # AI が行う作業の代わり

    def distros(self):
        return list(self._distros)

    def script(self, distro, text, root=False):
        self.scripts.append((distro, text, root))
        assert "\r" not in text, "CRLF が混ざった"
        if "mount -t drvfs" in text:
            self.mounted = True
        if "umount" in text:
            self.mounted = False
        if text.startswith("grep ' /mnt/room/' /proc/mounts") and self.mounted:
            return 0, "C:\\x /mnt/room/p 9p rw 0 0\n", ""
        return 0, "", ""

    def keepalive(self, distro):
        self.keepalives.append(distro)

        class K:
            terminated = False

            def terminate(self):
                self.terminated = True
        k = K()
        self.keep_procs.append(k)
        return k

    def push(self, distro, data, script):
        self.pushes.append((distro, data, script))
        return 0, "", ""

    def interactive(self, distro, command):
        self.interactive_calls.append((distro, command))
        if self.on_interactive:
            self.on_interactive()
        return 0


def sh(vault, *args):
    subprocess.run(["git", "-C", str(vault), *args], check=True, capture_output=True)


def make_vault(tmp, gitignore=GITIGNORE):
    v = Path(tmp)
    (v / "areas" / "area-x").mkdir(parents=True)
    (v / "areas" / "area-x" / "README.md").write_text(AREA_README, encoding="utf-8", newline="\n")
    (v / "projects").mkdir()
    (v / "archives").mkdir()
    (v / ".gitignore").write_text(gitignore, encoding="utf-8", newline="\n")
    sh(v, "init", "-q")
    sh(v, "config", "user.email", "t@example.com")
    sh(v, "config", "user.name", "t")
    sh(v, "config", "core.autocrlf", "false")
    sh(v, "add", "-A")
    sh(v, "commit", "-qm", "init", "--allow-empty")
    return v


def ctx_for(v, wsl=None):
    msgs = []
    c = room.Ctx(v, wsl=wsl or FakeWsl(), today="2026-10-12", now="2026-10-12 10:00", say=msgs.append, settle=0)
    c.msgs = msgs
    return c


def opened(tmp, wsl=None):
    v = make_vault(tmp)
    c = ctx_for(v, wsl)
    room.cmd_open(c, argparse.Namespace(name="proj-a", area="area-x", type="doc", boundary=None, commit=True))
    return v, c


class FrontmatterTest(unittest.TestCase):
    def test_update_and_remove(self):
        t = "---\nstatus: active\nreview: 仮置き\nupdated: 2026-10-01\n---\n\n# x\n"
        r = room.update_frontmatter(t, {"status": "done", "closed": "2026-10-12"}, remove=("review",))
        self.assertIn("status: done", r)
        self.assertNotIn("review", r)
        self.assertIn("closed: 2026-10-12", r)
        self.assertTrue(r.endswith("\n# x\n"))

    def test_read_ignores_trailing_comment(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "R.md"
            p.write_text("---\nboundary: internal   # 印\nstatus: active\n---\n", encoding="utf-8")
            self.assertEqual(room.read_frontmatter(p), {"boundary": "internal", "status": "active"})


class AreaListTest(unittest.TestCase):
    def test_add_replaces_none(self):
        r = room.add_area_entry(AREA_README, "## 進行中の Project", "- [[projects/a/README|a]]")
        self.assertIn("- [[projects/a/README|a]]", r)
        self.assertNotIn("## 進行中の Project\n\nなし。", r)

    def test_move_to_done(self):
        t = room.add_area_entry(AREA_README, "## 進行中の Project", "- [[projects/a/README|a]]（開始）")
        r = room.move_area_entry(t, "a", "2026-10-12")
        self.assertIn("## 完了した Project", r)
        self.assertIn("[[archives/a/README|a]]（開始、2026-10-12 完了）", r)
        self.assertNotIn("[[projects/a/README", r)
        head = r.split("## 完了した Project")[0]
        self.assertIn("なし。", head)


class InboxTest(unittest.TestCase):
    def test_idempotent_and_numbering(self):
        t, n = room.append_inbox(room.INBOX_NEW, "p", "2026-10-12", ["A", "B"], "src")
        self.assertEqual(n, 2)
        self.assertIn("`p#1` A", t)
        t2, n2 = room.append_inbox(t, "p", "2026-10-13", ["B", "C"], "src")
        self.assertEqual(n2, 1)
        self.assertIn("`p#3` C", t2)
        self.assertEqual(t2.count("`p#2` B"), 1)
        self.assertLess(t2.index("`p#3` C"), t2.index("## 取り込み済み"))

    def test_parse_cases(self):
        md = "- 【案件】やること1\n- 【汎用】別\n  - 【案件】やること2\n本文 【案件】は拾わない\n"
        self.assertEqual(room.parse_cases(md), ["やること1", "やること2"])


class OpenTest(unittest.TestCase):
    def test_open_creates_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            p = v / "projects" / "proj-a"
            for d in room.AI_DIRS:
                self.assertTrue((p / d).is_dir(), d)
            self.assertIn("area: area-x", (p / "README.md").read_text(encoding="utf-8"))
            self.assertIn("[[projects/proj-a/README|proj-a]]", (v / "areas/area-x/README.md").read_text(encoding="utf-8"))
            tracked = subprocess.run(["git", "-C", str(v), "ls-files"], capture_output=True, text=True, encoding="utf-8").stdout
            self.assertIn("projects/proj-a/ai/in/.gitkeep", tracked)
            self.assertNotIn("_noai", tracked)

    def test_open_refuses_without_gitignore_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp, gitignore="*.tmp\n")
            with self.assertRaises(room.RoomError):
                room.cmd_open(ctx_for(v), argparse.Namespace(name="p", area="area-x", type="doc", boundary=None, commit=False))

    def test_open_requires_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            (v / "areas/area-x/README.md").write_text("---\nstatus: active\n---\n\n# x\n", encoding="utf-8")
            a = argparse.Namespace(name="p", area="area-x", type="doc", boundary=None, commit=False)
            with self.assertRaises(room.RoomError):
                room.cmd_open(ctx_for(v), a)
            a.boundary = "internal"
            room.cmd_open(ctx_for(v), a)
            self.assertIn("boundary: internal", (v / "areas/area-x/README.md").read_text(encoding="utf-8"))


class StartTest(unittest.TestCase):
    def args(self, **kw):
        d = dict(name="proj-a", cmd="claude", no_launch=False, adopt=False, commit=False, yes=False)
        d.update(kw)
        return argparse.Namespace(**d)

    def test_start_flow_mounts_runs_unmounts(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            p = v / "projects" / "proj-a"
            wsl.on_interactive = lambda: (p / "ai/out/result.md").write_text("done\n", encoding="utf-8")
            room.cmd_start(c, self.args())
            mount_scripts = [s for s in wsl.scripts if "mount -t drvfs" in s[1]]
            self.assertEqual(len(mount_scripts), 1)
            self.assertTrue(mount_scripts[0][2], "マウントは root で行う")
            self.assertIn("/mnt/room/proj-a", mount_scripts[0][1])
            self.assertIn("-o metadata,uid=1000,gid=1000", mount_scripts[0][1])
            self.assertEqual(wsl.interactive_calls[0][1], "cd /mnt/room/proj-a && claude")
            self.assertFalse(wsl.mounted)
            self.assertFalse((p / "ai/ctx").exists(), "ctx は消える")
            self.assertIn("start", (p / "ai/records/room-log.md").read_text(encoding="utf-8"))
            self.assertTrue(any("result.md" in m for m in c.msgs))

    def test_start_snapshots_readme_readonly_during_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            seen = {}

            def during():
                f = v / "projects/proj-a/ai/ctx/README.md"
                seen["exists"] = f.exists()
                seen["readonly"] = not os.stat(f).st_mode & stat.S_IWRITE
            wsl.on_interactive = during
            room.cmd_start(c, self.args())
            self.assertEqual(seen, {"exists": True, "readonly": True})

    def test_start_restores_write_permission_of_all_in_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            keep = v / "projects/proj-a/ai/in/.gitkeep"

            def ro():  # マウント中に、部屋が in/ の全ファイルを読み取り専用にした状態
                os.chmod(keep, stat.S_IREAD)
            wsl.on_interactive = ro
            room.cmd_start(c, self.args())
            self.assertTrue(os.stat(keep).st_mode & stat.S_IWRITE)

    def test_start_blocked_by_existing_mount(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            wsl.mounted = True
            with self.assertRaises(room.RoomError) as cm:
                room.cmd_start(c, self.args())
            self.assertIn("マウントが残っている", str(cm.exception))
            self.assertEqual(wsl.interactive_calls, [])

    def test_start_blocked_without_distro(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            c.wsl._distros = []
            with self.assertRaises(room.RoomError):
                room.cmd_start(c, self.args())

    def test_provenance_blocks_unknown_file_and_adopt_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            f = v / "projects/proj-a/ai/in/data.csv"
            f.write_text("a,b\n1,2\n", encoding="utf-8")
            with self.assertRaises(room.RoomError) as cm:
                room.cmd_start(c, self.args())
            self.assertIn("由来の記録が無い", str(cm.exception))
            self.assertEqual(wsl.interactive_calls, [])
            room.cmd_start(c, self.args(adopt=True))
            man = json.loads((v / "projects/proj-a/ai/records/manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(man["files"]["in/data.csv"]["area"], "area-x")
            # 入力は書き込み可能に戻る（人が差し替えられる）
            self.assertTrue(os.stat(f).st_mode & stat.S_IWRITE)
            # 中身が変わると止まる
            f.write_text("a,b\n9,9\n", encoding="utf-8")
            with self.assertRaises(room.RoomError) as cm2:
                room.cmd_start(c, self.args())
            self.assertIn("ハッシュが違う", str(cm2.exception))

    def test_provenance_blocks_file_from_other_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            p = v / "projects/proj-a"
            (p / "ai/in/x.csv").write_text("x\n", encoding="utf-8")
            room.cmd_start(c, self.args(adopt=True))
            man = json.loads((p / "ai/records/manifest.json").read_text(encoding="utf-8"))
            man["files"]["in/x.csv"]["project"] = "other"
            (p / "ai/records/manifest.json").write_text(json.dumps(man), encoding="utf-8")
            with self.assertRaises(room.RoomError) as cm:
                room.cmd_start(c, self.args())
            self.assertIn("由来が違う", str(cm.exception))

    def test_start_warns_about_ignored_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            p = v / "projects/proj-a"
            wsl.on_interactive = lambda: (p / "ai/work/scratch.tmp").write_text("x", encoding="utf-8")
            room.cmd_start(c, self.args())
            self.assertTrue(any("無視されている" in m for m in c.msgs))
            self.assertTrue(any("scratch.tmp" in m for m in c.msgs))

    def test_start_unmounts_even_if_ai_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)

            def boom():
                raise KeyboardInterrupt
            wsl.on_interactive = boom
            with self.assertRaises(KeyboardInterrupt):
                room.cmd_start(c, self.args())
            self.assertFalse(wsl.mounted)
            self.assertFalse((v / "projects/proj-a/ai/ctx").exists())

    def test_commit_refuses_stray_staged_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            (v / "other.txt").write_text("x", encoding="utf-8")
            sh(v, "add", "other.txt")
            (v / "projects/proj-a/ai/out/r.md").write_text("r", encoding="utf-8")
            with self.assertRaises(room.RoomError) as cm:
                room.cmd_start(c, self.args(commit=True))
            self.assertIn("対象外", str(cm.exception))


class MaskIntegrationTest(unittest.TestCase):
    MASK = '[terms.CUST]\nacme = ["アクメ商事株式会社", "アクメ商事"]\n'

    def args(self, **kw):
        d = dict(name="proj-a", cmd="claude", no_launch=False, adopt=False, commit=False, yes=True)
        d.update(kw)
        return argparse.Namespace(**d)

    def setup_project(self, tmp, wsl):
        v, c = opened(tmp, wsl)
        p = v / "projects/proj-a"
        (p / "_noai/mask.toml").write_text(self.MASK, encoding="utf-8", newline="\n")
        (p / "_noai/raw/売上.csv").write_text("顧客,額\nアクメ商事株式会社,100\n", encoding="utf-8", newline="\n")
        return v, c, p

    def test_start_masks_runs_and_restores(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c, p = self.setup_project(tmp, wsl)
            seen = {}

            def ai():
                seen["in"] = (p / "ai/in/売上.csv").read_text(encoding="utf-8-sig")
                (p / "ai/out/report.md").write_text("⟦CUST_001⟧ の売上は増加\n", encoding="utf-8", newline="\n")
            wsl.on_interactive = ai
            room.cmd_start(c, self.args())
            self.assertNotIn("アクメ", seen["in"])
            self.assertIn("⟦CUST_001⟧", seen["in"])
            self.assertIn("アクメ商事株式会社 の売上は増加", (p / "_noai/final/report.md").read_text(encoding="utf-8"))
            self.assertIn("⟦CUST_001⟧", (p / "ai/out/report.md").read_text(encoding="utf-8"))
            man = json.loads((p / "ai/records/manifest.json").read_text(encoding="utf-8"))
            e = man["files"]["in/売上.csv"]
            self.assertTrue(e["raw_sha256"] and e["mask_sha256"] and e["mapping_version"] == 1)
            mapping = (p / "_noai/map/mapping.json").read_text(encoding="utf-8")
            self.assertNotIn("アクメ", (p / "ai/records/manifest.json").read_text(encoding="utf-8"))
            self.assertIn("アクメ商事株式会社", mapping)

    def test_unchanged_raw_is_not_remasked_and_changed_toml_asks(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c, p = self.setup_project(tmp, wsl)
            room.cmd_start(c, self.args())
            mt = (p / "ai/in/売上.csv").stat().st_mtime_ns
            room.cmd_start(c, self.args())
            self.assertEqual(mt, (p / "ai/in/売上.csv").stat().st_mtime_ns)
            (p / "_noai/mask.toml").write_text(self.MASK + '[terms.PERSON]\nt = ["田中太郎"]\n', encoding="utf-8", newline="\n")
            (p / "_noai/raw/売上.csv").write_text("顧客,額\nアクメ商事株式会社,100\n田中太郎,1\n", encoding="utf-8", newline="\n")
            room.cmd_start(c, self.args())
            self.assertIn("⟦PERSON_001⟧", (p / "ai/in/売上.csv").read_text(encoding="utf-8-sig"))

    def test_raw_without_mask_toml_stops_before_mount(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c, p = self.setup_project(tmp, wsl)
            (p / "_noai/mask.toml").unlink()
            with self.assertRaises(room.RoomError):
                room.cmd_start(c, self.args())
            self.assertEqual(wsl.interactive_calls, [])

    def test_unresolved_placeholder_stops_and_writes_no_final(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c, p = self.setup_project(tmp, wsl)
            wsl.on_interactive = lambda: (p / "ai/out/r.md").write_text("⟦CUST_099⟧\n", encoding="utf-8", newline="\n")
            with self.assertRaises(room.RoomError) as cm:
                room.cmd_start(c, self.args())
            self.assertIn("CUST_099", str(cm.exception))
            self.assertFalse((p / "_noai/final/r.md").exists())
            self.assertFalse(wsl.mounted)


class SharedPushTest(unittest.TestCase):
    def test_push_records_base_commit_and_sends_tar(self):
        import io
        import tarfile
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            r = v / "resources"
            (r / "workflow-kit").mkdir(parents=True)
            (r / "workflow-kit/hooks.md").write_text("hooks\n", encoding="utf-8")
            (r / "workflow-kit/.venv").mkdir()
            (r / "workflow-kit/.venv/x").write_text("no", encoding="utf-8")
            (r / "exmem/lessons").mkdir(parents=True)
            (r / "exmem/lessons/a.md").write_text("a\n", encoding="utf-8")
            (r / "mobile-session").mkdir()
            (r / "mobile-session/x.md").write_text("no", encoding="utf-8")
            sh(r, "init", "-q"); sh(r, "config", "user.email", "t@e"); sh(r, "config", "user.name", "t")
            sh(r, "add", "-A"); sh(r, "commit", "-qm", "c")
            commit = subprocess.run(["git", "-C", str(r), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            # 外側の Vault の git に resources を追跡させない（入れ子の git）
            args = argparse.Namespace(name="proj-a", cmd="claude", no_launch=False, adopt=False, commit=False, yes=False)
            room.cmd_start(c, args)
            self.assertEqual(len(wsl.pushes), 1)
            distro, data, script = wsl.pushes[0]
            self.assertEqual(distro, "room-area-x")
            self.assertIn("chmod -R a-w", script)
            names = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz").getnames()
            self.assertIn("workflow-kit/hooks.md", names)
            self.assertIn("exmem/lessons/a.md", names)
            self.assertIn("ROOM.md", names)
            self.assertFalse([n for n in names if ".venv" in n or "mobile-session" in n])
            man = json.loads((v / "projects/proj-a/ai/records/manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(man["shared"]["commit"], commit)
            self.assertFalse(man["shared"]["dirty"])
            # 部屋の ~/.claude/CLAUDE.md への案内（目印の範囲だけを入れ替える sh -s のスクリプト）
            ptr = [t for (_d, t, _r) in wsl.scripts if "room-shared:begin" in t]
            self.assertEqual(len(ptr), 1)
            self.assertIn("~/shared/ROOM.md", ptr[0])
            self.assertIn("$HOME/.claude/CLAUDE.md", ptr[0])
            self.assertIn("sed -i '/^<!-- room-shared:begin/,/^<!-- room-shared:end -->/d'", ptr[0])
            # 同じ内容なら同じバイト列
            self.assertEqual(data, room.build_share_tar(r, {"ROOM.md": tarfile.open(fileobj=io.BytesIO(data), mode="r:gz").extractfile("ROOM.md").read().decode()}))

    def test_no_resources_skips(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            room.cmd_start(c, argparse.Namespace(name="proj-a", cmd="claude", no_launch=False, adopt=False, commit=False, yes=False))
            self.assertEqual(wsl.pushes, [])


class ReadmeDraftTest(unittest.TestCase):
    def test_draft_replaces_body_keeps_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            p = v / "projects/proj-a"
            before = (p / "README.md").read_text(encoding="utf-8")
            fm_before = room.split_frontmatter(before)[0]
            (p / "ai/out/readme-draft.md").write_text("# 目的\n\n新しい目的\n", encoding="utf-8")
            room.cmd_readme(c, argparse.Namespace(name="proj-a", yes=True, commit=False))
            after = (p / "README.md").read_text(encoding="utf-8")
            self.assertIn("新しい目的", after)
            self.assertIn("status: active", after)
            self.assertIn("area: area-x", after)
            self.assertIn("updated: 2026-10-12", after)
            self.assertEqual(room.split_frontmatter(after)[0].count("\n"), fm_before.count("\n"))

    def test_draft_with_frontmatter_or_missing_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            p = v / "projects/proj-a"
            args = argparse.Namespace(name="proj-a", yes=True, commit=False)
            with self.assertRaises(room.RoomError):
                room.cmd_readme(c, args)
            (p / "ai/out/readme-draft.md").write_text("---\nstatus: done\n---\nx\n", encoding="utf-8")
            with self.assertRaises(room.RoomError):
                room.cmd_readme(c, args)


class StockTest(unittest.TestCase):
    DRAFT = ("---\ntype: inbox\ntitle: テスト知識\ntags:\n  - a\n  - b\n  - c\ncreated: 2026-10-12\nbase_commit: {base}\nobserved: 2026-10-12\n"
             "sources:\n  - Claude Code conversation \"x\"\n---\n\n# t\n\n## Goal\nx\n統合先の候補: lessons/topic-a.md（キーワード: a）\n\n## Principles\nなし\n")

    def setup(self, tmp):
        v, c = opened(tmp)
        r = v / "resources"
        (r / "exmem/lessons").mkdir(parents=True)
        (r / "exmem/inbox").mkdir(parents=True)
        (r / "exmem/lessons/topic-a.md").write_text("v1\n", encoding="utf-8")
        sh(r, "init", "-q"); sh(r, "config", "user.email", "t@e"); sh(r, "config", "user.name", "t")
        sh(r, "add", "-A"); sh(r, "commit", "-qm", "c1")
        base = subprocess.run(["git", "-C", str(r), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        return v, c, r, base

    def ns(self, **kw):
        d = dict(name="proj-a", yes=True)
        d.update(kw)
        return argparse.Namespace(**d)

    def test_delivers_without_stale_mark_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, r, base = self.setup(tmp)
            p = v / "projects/proj-a"
            (p / "ai/out/stock").mkdir(parents=True)
            (p / "ai/out/stock/2026-10-12-topic-a.md").write_text(self.DRAFT.format(base=base), encoding="utf-8")
            room.cmd_stock(c, self.ns())
            got = (r / "exmem/inbox/2026-10-12-topic-a.md").read_text(encoding="utf-8")
            self.assertNotIn("base_stale", got)
            room.cmd_stock(c, self.ns())
            self.assertEqual(len(list((r / "exmem/inbox").glob("*.md"))), 1)

    def test_stale_mark_when_target_lesson_changed(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, r, base = self.setup(tmp)
            p = v / "projects/proj-a"
            (r / "exmem/lessons/topic-a.md").write_text("v2\n", encoding="utf-8")
            sh(r, "add", "-A"); sh(r, "commit", "-qm", "c2")
            (p / "ai/out/stock").mkdir(parents=True)
            (p / "ai/out/stock/2026-10-12-topic-a.md").write_text(self.DRAFT.format(base=base), encoding="utf-8")
            room.cmd_stock(c, self.ns())
            got = (r / "exmem/inbox/2026-10-12-topic-a.md").read_text(encoding="utf-8")
            self.assertIn("base_stale:", got)
            self.assertIn("topic-a.md", got)

    def test_refuses_missing_header_and_masked_terms(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, r, base = self.setup(tmp)
            p = v / "projects/proj-a"
            (p / "ai/out/stock").mkdir(parents=True)
            (p / "ai/out/stock/no-header.md").write_text("---\ntype: inbox\ntitle: x\n---\nx\n", encoding="utf-8")
            leak = self.DRAFT.format(base=base).replace("テスト知識", "アクメ商事の知識")
            (p / "ai/out/stock/leak.md").write_text(leak, encoding="utf-8")
            (p / "_noai/mask.toml").write_text('[terms.CUST]\nacme = ["アクメ商事"]\n', encoding="utf-8")
            (p / "_noai/raw/a.csv").write_text("x\nアクメ商事\n", encoding="utf-8")
            room.mask_project(c, room.Project.load(c, "proj-a"), yes=True)
            room.cmd_stock(c, self.ns())
            self.assertEqual(list((r / "exmem/inbox").glob("*.md")), [])


class SharedPermissionTest(unittest.TestCase):
    def test_snippet_merges_keeps_existing_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            (home / ".claude/settings.json").write_text(
                json.dumps({"model": "x", "permissions": {"allow": ["Bash(ls)"], "deny": ["Read(~/.ssh/**)"]}}), encoding="utf-8")
            env = dict(os.environ, HOME=str(home))
            for _ in range(2):
                subprocess.run([sys.executable, "-c", room.SHARED_RULE_PY], env=env, check=True)
            d = json.loads((home / ".claude/settings.json").read_text(encoding="utf-8"))
            self.assertEqual(d["model"], "x")
            self.assertEqual(d["permissions"]["deny"], ["Read(~/.ssh/**)"])
            self.assertEqual(d["permissions"]["allow"], ["Bash(ls)", "Read(~/shared/**)"])

    def test_snippet_creates_file_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, HOME=tmp)
            subprocess.run([sys.executable, "-c", room.SHARED_RULE_PY], env=env, check=True)
            d = json.loads((Path(tmp) / ".claude/settings.json").read_text(encoding="utf-8"))
            self.assertEqual(d["permissions"]["allow"], ["Read(~/shared/**)"])

    def test_start_installs_permission_with_shared(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            (v / "resources/workflow-kit").mkdir(parents=True)
            (v / "resources/workflow-kit/hooks.md").write_text("h\n", encoding="utf-8")
            room.cmd_start(c, argparse.Namespace(name="proj-a", cmd="claude", no_launch=False, adopt=False, commit=False, yes=False))
            self.assertTrue(any("ROOM_PERM_EOF" in s[1] and s[2] is False for s in wsl.scripts))


class KeepaliveTest(unittest.TestCase):
    def test_no_launch_keeps_room_alive_and_stops_it(self):
        import builtins
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            orig = builtins.input
            builtins.input = lambda *a, **k: ""
            try:
                room.cmd_start(c, argparse.Namespace(name="proj-a", cmd="claude", no_launch=True, adopt=False, commit=False, yes=False))
            finally:
                builtins.input = orig
            self.assertEqual(wsl.keepalives, ["room-area-x"])
            self.assertTrue(wsl.keep_procs[0].terminated)


class CloseTest(unittest.TestCase):
    def test_close_requires_close_md_and_unmounted(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            with self.assertRaises(room.RoomError):
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            (v / "projects/proj-a/ai/out/close.md").write_text("- 【案件】x\n", encoding="utf-8")
            wsl.mounted = True
            with self.assertRaises(room.RoomError):
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))

    def test_close_moves_to_archives_and_hands_over(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            p = v / "projects/proj-a"
            (p / "ai/out/close.md").write_text("- 【案件】運用で埋める\n- 【案件】表記ゆれを直す\n", encoding="utf-8")
            (p / "ai/out/final.md").write_text("成果物\n", encoding="utf-8")
            (p / "_noai/raw/orig.csv").write_text("secret\n", encoding="utf-8")
            (p / "_noai/map").mkdir(exist_ok=True)
            (p / "ai/ctx").mkdir(exist_ok=True)
            (p / "ai/ctx/README.md").write_text("snapshot", encoding="utf-8")
            room.cmd_close(c, argparse.Namespace(name="proj-a", commit=True))
            a = v / "archives/proj-a"
            self.assertFalse(p.exists())
            self.assertTrue((a / "ai/out/final.md").exists())
            self.assertTrue((a / "ai/out/close.md").exists())
            self.assertEqual((a / "_noai/raw/orig.csv").read_text(encoding="utf-8"), "secret\n", "追跡外も移る")
            self.assertFalse((a / "ai/ctx").exists())
            fm = room.read_frontmatter(a / "README.md")
            self.assertEqual((fm["status"], fm["closed"], fm["reap_after"]), ("done", "2026-10-12", "2026-10-26"))
            self.assertNotIn("review", fm)
            inbox = (v / "areas/area-x/ai/docs/inbox.md").read_text(encoding="utf-8")
            self.assertIn("`proj-a#1` 運用で埋める", inbox)
            self.assertIn("`proj-a#2` 表記ゆれを直す", inbox)
            area = (v / "areas/area-x/README.md").read_text(encoding="utf-8")
            self.assertIn("[[archives/proj-a/README|proj-a]]", area)
            tracked = subprocess.run(["git", "-C", str(v), "ls-files"], capture_output=True, text=True, encoding="utf-8").stdout
            self.assertIn("archives/proj-a/ai/out/final.md", tracked)
            self.assertNotIn("projects/proj-a", tracked)
            self.assertNotIn("_noai", tracked)
            self.assertNotIn("secret", tracked)
            status = subprocess.run(["git", "-C", str(v), "status", "--porcelain"], capture_output=True, text=True, encoding="utf-8").stdout
            self.assertEqual(status.strip(), "", "コミット後はクリーン")
            log = subprocess.run(["git", "-C", str(v), "log", "-1", "--format=%s"], capture_output=True, text=True, encoding="utf-8").stdout
            self.assertIn("[room] proj-a を close", log)

    def test_close_second_run_does_not_duplicate_inbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            text, n = room.append_inbox(room.INBOX_NEW, "proj-a", "2026-10-12", ["x"], "s")
            again, n2 = room.append_inbox(text, "proj-a", "2026-10-12", ["x"], "s")
            self.assertEqual((n, n2), (1, 0))
            self.assertEqual(text, again)


class WslQuotingTest(unittest.TestCase):
    def test_script_text_keeps_backslashes_and_lf(self):
        wsl = FakeWsl()
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, wsl)
            p = room.Project.load(c, "proj-a")
            room.mount(c, p)
            text = [s for s in wsl.scripts if "mount -t drvfs" in s[1]][0][1]
            self.assertIn(str(p.ai), text)  # Windows のパスが、そのまま（引用符つきで）入る
            self.assertNotIn("\r", text)
            self.assertTrue(text.startswith("set -e\n"))


if __name__ == "__main__":
    unittest.main()
