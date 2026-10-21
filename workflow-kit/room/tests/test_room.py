"""room.py のテスト。WSL は差し替え、一時ディレクトリの Vault（git）で `open → start → close` を通す。"""
import argparse
import json
import os
import shutil
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
        if text.startswith("echo user="):
            return 0, getattr(self, "isolation", "user=ai\nc=0\ncmd=no\nsudo=no\n"), ""
        if text.startswith("export PATH") and "claude --version" in text:
            return 0, "2.1.296 (Claude Code)\n", ""
        if text.startswith("grep ' /mnt/room/' /proc/mounts") and self.mounted:
            return 0, "C:\\x /mnt/room/p 9p rw 0 0\n", ""
        return 0, "", ""

    def install(self, distro, base):
        self.installed = (distro, base)
        self._distros.append(distro)
        return 0

    def terminate(self, distro):
        self.terminated = getattr(self, "terminated", []) + [distro]

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

    def shell(self, distro):
        self.shells = getattr(self, "shells", []) + [distro]
        return 0

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
    room.cmd_open(c, argparse.Namespace(name="proj-a", area="area-x", type="doc", data="restore", boundary=None, commit=True))
    return v, c


@unittest.skipUnless(shutil.which("openssl"), "openssl が PATH にない")
class CaCertTest(unittest.TestCase):
    def make_cert(self, tmp, n=1):
        pems = []
        for i in range(n):
            subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", str(Path(tmp) / f"k{i}.pem"),
                            "-out", str(Path(tmp) / f"c{i}.pem"), "-subj", f"/CN=test-ca-{i}", "-days", "1"], check=True, capture_output=True)
            pems.append((Path(tmp) / f"c{i}.pem").read_text(encoding="utf-8"))
        f = Path(tmp) / f"bundle{n}.pem"
        f.write_text("".join(pems), encoding="utf-8")
        return f

    def test_init_installs_ca_cert_as_root_after_apt_and_before_curl(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = self.make_cert(tmp)
            wsl = FakeWsl(distros=())
            room.cmd_init(ctx_for(make_vault(tmp), wsl), argparse.Namespace(area="area-x", resume=False, ca_cert=str(f)))
            scripts = [(s[1], s[2]) for s in wsl.scripts]
            idx = lambda key: [i for i, (t, _) in enumerate(scripts) if key in t][0]
            self.assertLess(idx("apt-get"), idx("update-ca-certificates"))
            self.assertLess(idx("update-ca-certificates"), idx("astral.sh"))
            text, root = scripts[idx("update-ca-certificates")]
            self.assertTrue(root)
            self.assertIn("BEGIN CERTIFICATE", text)

    def test_init_without_ca_cert_installs_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl(distros=())
            room.cmd_init(ctx_for(make_vault(tmp), wsl), argparse.Namespace(area="area-x", resume=False))
            self.assertFalse(any("update-ca-certificates" in s[1] for s in wsl.scripts))

    def test_ca_cert_rejects_private_key_too_many_and_non_pem_before_touching_room(self):
        with tempfile.TemporaryDirectory() as tmp:
            one = self.make_cert(tmp)
            with_key = Path(tmp) / "withkey.pem"
            with_key.write_text(one.read_text(encoding="utf-8") + (Path(tmp) / "k0.pem").read_text(encoding="utf-8"), encoding="utf-8")
            many = self.make_cert(tmp, n=room.CA_MAX_CERTS + 1)
            junk = Path(tmp) / "junk.cer"
            junk.write_bytes(b"\x30\x82\x01")
            v = make_vault(tmp)
            for bad in (with_key, many, junk, Path(tmp) / "none.pem"):
                wsl = FakeWsl(distros=())
                with self.assertRaises(room.RoomError):
                    room.cmd_init(ctx_for(v, wsl), argparse.Namespace(area="area-x", resume=False, ca_cert=str(bad)))
                self.assertFalse(hasattr(wsl, "installed"))


class WslEnvTest(unittest.TestCase):
    def test_wslenv_is_removed(self):
        saved = {k: os.environ.get(k) for k in ("WSLENV", "KEEP_ME")}
        os.environ["WSLENV"] = "SSL_CERT_FILE/p"
        os.environ["KEEP_ME"] = "1"
        try:
            env = room.wsl_env()
        finally:
            for k, v in saved.items():
                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
        self.assertNotIn("WSLENV", {k.upper() for k in env})
        self.assertEqual(env["KEEP_ME"], "1")


class PushAssignTest(unittest.TestCase):
    def test_assignment_in_script_is_rejected(self):
        for script in ('d="$HOME/x"; rm -rf "$d"', "set -e; d=1; echo $d", "a=1 b=2 true"):
            with self.assertRaises(room.RoomError):
                room.Wsl().push("room-x", b"", script)

    def test_options_and_comparisons_are_not_assignments(self):
        for script in ('tar xzf - --exclude=x -C "$HOME/y"', "[ a == b ] && true", 'chmod -R a-w "$HOME/x"'):
            self.assertIsNone(room.SCRIPT_ASSIGN.search(script), script)


class AwsKeyTest(unittest.TestCase):
    def ctx(self, tmp, answers, secrets, wsl):
        v = Path(tmp) if (Path(tmp) / "areas").exists() else make_vault(tmp)
        c = ctx_for(v, wsl)
        c.ask = lambda _p: answers.pop(0)
        c.ask_secret = lambda _p: secrets.pop(0)
        return c

    def run_cmd(self, c, area="area-x", profile="n1-trial"):
        room.cmd_aws_key(c, argparse.Namespace(area=area, profile=profile))

    def test_key_goes_through_stdin_not_the_command_line_or_messages(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            c = self.ctx(tmp, ["AKIAEXAMPLE0000000"], ["s" * 40, ""], wsl)
            self.run_cmd(c)
            self.assertEqual(wsl.pushes, [])  # sh -c の引数では渡さない（wsl.exe の側のシェルが、スクリプト内で代入した変数を先に展開して空にする）
            distro, script, root = wsl.scripts[0]
            self.assertEqual(distro, "room-area-x")
            self.assertFalse(root)
            self.assertIn("[n1-trial]", script)
            self.assertIn("aws_secret_access_key=" + "s" * 40, script)
            self.assertNotIn("aws_session_token", script)
            self.assertIn("<<'ROOM_AWS_EOF'", script)  # 引用つき: 本文の $ を展開しない
            self.assertIn("chmod 600", script)
            self.assertFalse(any("s" * 40 in m or "AKIAEXAMPLE" in m for m in c.msgs))

    def test_session_token_is_written_when_given(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            self.run_cmd(self.ctx(tmp, ["AKIAEXAMPLE0000000"], ["s" * 40, "t" * 60], wsl))
            self.assertIn("aws_session_token=" + "t" * 60, wsl.scripts[0][1])

    def test_bad_input_and_missing_room_write_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            for answers, secrets, profile, area in ((["bad key"], ["s" * 40, ""], "n1", "area-x"),
                                                    (["AKIAEXAMPLE0000000"], ["short", ""], "n1", "area-x"),
                                                    (["AKIAEXAMPLE0000000"], ["s" * 40, ""], "a b;rm", "area-x"),
                                                    (["AKIAEXAMPLE0000000"], ["s" * 40, ""], "n1", "no-room")):
                wsl = FakeWsl()
                with self.assertRaises(room.RoomError):
                    self.run_cmd(self.ctx(tmp, list(answers), list(secrets), wsl), area=area, profile=profile)
                self.assertEqual(wsl.pushes, [])
                self.assertEqual(wsl.scripts, [])


class ShellTest(unittest.TestCase):
    def test_shell_enters_the_room_and_refuses_a_missing_room(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            room.cmd_shell(ctx_for(make_vault(tmp), wsl), argparse.Namespace(area="area-x"))
            self.assertEqual(wsl.shells, ["room-area-x"])
            with self.assertRaises(room.RoomError):
                room.cmd_shell(ctx_for(Path(tmp), FakeWsl()), argparse.Namespace(area="no-room"))

    def test_aws_key_script_stops_when_files_are_not_owned_by_the_user(self):
        self.assertIn("[ -O", room.aws_credentials_script("n1", "[n1]\n"))
        self.assertIn("chown -R ai:ai", room.aws_credentials_script("n1", "[n1]\n"))


class InitTest(unittest.TestCase):
    def test_init_creates_room_configures_and_installs(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl(distros=())
            v = make_vault(tmp)
            c = ctx_for(v, wsl)
            room.cmd_init(c, argparse.Namespace(area="area-x", resume=False))
            self.assertEqual(wsl.installed, ("room-area-x", "Ubuntu-26.04"))
            scripts = [(s[1], s[2]) for s in wsl.scripts]
            conf = [t for t, root in scripts if "/etc/wsl.conf" in t][0]
            self.assertIn("enabled=false", conf)
            self.assertIn("default=ai", conf)
            self.assertLess([i for i, (t, _) in enumerate(scripts) if "useradd" in t][0],
                            [i for i, (t, _) in enumerate(scripts) if "/etc/wsl.conf" in t][0])
            self.assertEqual(wsl.terminated, ["room-area-x"])
            self.assertTrue(any("apt-get" in t and root for t, root in scripts))
            idx = lambda key: [i for i, (t, _) in enumerate(scripts) if key in t][0]
            node = idx("latest-v24.x")
            self.assertTrue(scripts[node][1])  # root で入れる
            self.assertIn("sha256sum -c", scripts[node][0])
            self.assertLess(node, idx("astral.sh"))
            self.assertIn("npm config set cafile", scripts[idx("npm config set cafile")][0])
            conv = idx("libreoffice-calc")
            self.assertTrue(scripts[conv][1])  # root で入れる
            for pkg in ("libreoffice-writer", "libreoffice-impress", "fonts-noto-cjk", "pandoc"):
                self.assertIn(pkg, scripts[conv][0])
            self.assertIn("Noto Sans CJK JP", scripts[conv][0])
            self.assertIn("fc-cache", scripts[conv][0])
            # PlemolJP は、安定するまで init から外している（2026-10-20）。戻すときは、ここを元の確認（root で入れる、SHA-256 の照合、conv の後）に戻す
            self.assertFalse(any("PlemolJP_" in t for t, _ in scripts))
            self.assertIn("sha256sum -c", room.PLEMOLJP_INSTALL)
            self.assertIn(room.PLEMOLJP_SHA256, room.PLEMOLJP_INSTALL)
            self.assertIn("<family>PlemolJP</family>", scripts[conv][0])
            cr = idx("playwright@")
            self.assertTrue(scripts[cr][1])  # root で入れる
            for key in ("libasound2t64", "/opt/ms-playwright", room.PLAYWRIGHT_VERSION, room.MERMAID_CLI_VERSION,
                        "--no-sandbox", "NODE_EXTRA_CA_CERTS"):
                self.assertIn(key, scripts[cr][0])
            self.assertLess(conv, cr)
            self.assertLess(idx("latest-v24.x"), conv)
            self.assertLess(conv, idx("astral.sh"))

    def test_init_refuses_existing_and_bad_isolation_stops_before_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            with self.assertRaises(room.RoomError):
                room.cmd_init(ctx_for(v, FakeWsl()), argparse.Namespace(area="area-x", resume=False))
            wsl = FakeWsl(distros=())
            wsl.isolation = "user=ai\nc=3\ncmd=no\nsudo=no\n"
            with self.assertRaises(room.RoomError):
                room.cmd_init(ctx_for(v, wsl), argparse.Namespace(area="area-x", resume=False))
            self.assertFalse(any("apt-get" in s[1] for s in wsl.scripts))

    def git_out(self, v, *args):
        return subprocess.run(["git", "-C", str(v), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout

    def test_init_creates_area_with_boundary_and_commits_only_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            (v / "areas" / "area-x" / "memo.md").write_text("別の編集\n", encoding="utf-8")  # 巻き込まれてはいけない
            wsl = FakeWsl(distros=())
            room.cmd_init(ctx_for(v, wsl), argparse.Namespace(area="area-y", resume=False, boundary="internal", commit=True))
            text = (v / "areas" / "area-y" / "README.md").read_text(encoding="utf-8")
            self.assertIn("boundary: internal", text)
            self.assertEqual(self.git_out(v, "show", "--name-only", "--format=", "HEAD").split(), ["areas/area-y/README.md"])
            self.assertIn("?? areas/area-x/memo.md", self.git_out(v, "status", "--porcelain"))

    def test_room_commit_has_trailers_with_kit_rev(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            room.cmd_init(ctx_for(v, FakeWsl(distros=())), argparse.Namespace(area="area-y", resume=False, boundary="internal", commit=True))
            tr = self.git_out(v, "log", "-1", "--format=%(trailers:key=Room-Op,key=Room-Rev,key=Room-Area,key=Room-Project,separator=%x0a)").split("\n")
            tr = [l for l in tr if l]
            self.assertIn("Room-Op: init", tr)
            self.assertIn("Room-Area: area-y", tr)
            self.assertTrue(any(l.startswith("Room-Rev: ") and len(l) > len("Room-Rev: ") for l in tr), tr)
            self.assertFalse(any(l.startswith("Room-Project") for l in tr))

    def test_init_without_boundary_does_not_create_area(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            wsl = FakeWsl(distros=())
            with self.assertRaises(room.RoomError):
                room.cmd_init(ctx_for(v, wsl), argparse.Namespace(area="area-y", resume=False, boundary=None, commit=True))
            self.assertFalse((v / "areas" / "area-y").exists())
            self.assertFalse(hasattr(wsl, "installed"))

    def test_init_existing_area_makes_no_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            before = self.git_out(v, "rev-parse", "HEAD")
            room.cmd_init(ctx_for(v, FakeWsl(distros=())), argparse.Namespace(area="area-x", resume=False, boundary=None, commit=True))
            self.assertEqual(self.git_out(v, "rev-parse", "HEAD"), before)

    def test_init_no_commit_leaves_area_uncommitted(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            before = self.git_out(v, "rev-parse", "HEAD")
            room.cmd_init(ctx_for(v, FakeWsl(distros=())), argparse.Namespace(area="area-y", resume=False, boundary="internal", commit=False))
            self.assertEqual(self.git_out(v, "rev-parse", "HEAD"), before)
            self.assertIn("areas/area-y/", self.git_out(v, "status", "--porcelain"))

    def test_init_and_open_commit_only_their_paths_when_other_changes_are_staged(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            (v / "other.txt").write_text("取り残し\n", encoding="utf-8")
            sh(v, "add", "other.txt")
            room.cmd_init(ctx_for(v, FakeWsl(distros=())), argparse.Namespace(area="area-y", resume=False, boundary="internal", commit=True))
            self.assertEqual(self.git_out(v, "show", "--name-only", "--format=", "HEAD").split(), ["areas/area-y/README.md"])
            room.cmd_open(ctx_for(v), argparse.Namespace(name="proj-a", area="area-x", type="doc", data="restore", boundary=None, commit=True))
            files = self.git_out(v, "show", "--name-only", "--format=", "HEAD").split()
            self.assertNotIn("other.txt", files)
            self.assertIn("projects/proj-a/README.md", files)
            self.assertEqual(self.git_out(v, "diff", "--cached", "--name-only").split(), ["other.txt"])  # ステージに残る

    def test_open_commits_initial_state_without_other_area_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            (v / "areas" / "area-x" / "memo.md").write_text("別の編集\n", encoding="utf-8")
            room.cmd_open(ctx_for(v), argparse.Namespace(name="proj-a", area="area-x", type="doc", data="restore", boundary=None, commit=True))
            files = self.git_out(v, "show", "--name-only", "--format=", "HEAD").split()
            self.assertIn("areas/area-x/README.md", files)
            self.assertIn("projects/proj-a/README.md", files)
            self.assertNotIn("areas/area-x/memo.md", files)

    def test_init_resume_needs_existing_room(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            with self.assertRaises(room.RoomError):
                room.cmd_init(ctx_for(v, FakeWsl(distros=())), argparse.Namespace(area="area-x", resume=True))
            wsl = FakeWsl()
            room.cmd_init(ctx_for(v, wsl), argparse.Namespace(area="area-x", resume=True))
            self.assertFalse(hasattr(wsl, "installed"))


class RenameAreaTest(unittest.TestCase):
    def git_out(self, v, *args):
        return subprocess.run(["git", "-C", str(v), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout

    def args(self, old="area-x", new="area-z", commit=True):
        return argparse.Namespace(old=old, new=new, commit=commit)

    def test_rename_moves_area_rewrites_projects_and_manifest_and_commits(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            (v / "areas" / "area-x" / "memo.md").write_text("追跡外\n", encoding="utf-8")
            p = room.Project.load(c, "proj-a")
            (p.ai / "in" / "a.txt").write_text("x", encoding="utf-8")
            room.adopt_in(c, p)
            sh(v, "add", "-A")
            sh(v, "commit", "-qm", "setup")
            room.cmd_rename_area(c, self.args())
            self.assertFalse((v / "areas" / "area-x").exists())
            self.assertTrue((v / "areas" / "area-z" / "memo.md").exists())
            readme = (v / "projects" / "proj-a" / "README.md").read_text(encoding="utf-8")
            self.assertIn("area: area-z", readme)
            self.assertIn("[[areas/area-z/README|area-z]]", readme)
            self.assertNotIn("area-x", readme)
            self.assertIn("[[projects/proj-a/README", (v / "areas" / "area-z" / "README.md").read_text(encoding="utf-8"))
            self.assertEqual(room.Project.load(c, "proj-a").area, "area-z")
            self.assertEqual(room.check_provenance(room.Project.load(c, "proj-a")), [])
            self.assertEqual(self.git_out(v, "status", "--porcelain", "--", "areas", "projects").strip().splitlines(), [])

    def test_rename_refuses_bad_missing_existing_and_mounted(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            (v / "areas" / "area-y").mkdir()
            c = ctx_for(v)
            for old, new in (("area-x", "日本語"), ("area-x", "area-x"), ("nothing", "area-z"), ("area-x", "area-y")):
                with self.assertRaises(room.RoomError):
                    room.cmd_rename_area(c, self.args(old, new))
            self.assertTrue((v / "areas" / "area-x").exists())
            wsl = FakeWsl()
            wsl.mounted = True
            with self.assertRaises(room.RoomError):
                room.cmd_rename_area(ctx_for(v, wsl), self.args())
            self.assertTrue((v / "areas" / "area-x").exists())


class ReapTest(unittest.TestCase):
    def archived(self, v, name, reap_after, status="done", reaped=None):
        d = v / "archives" / name
        d.mkdir(parents=True)
        fm = f"---\narea: area-x\nstatus: {status}\nreap_after: {reap_after}\n" + (f"reaped: {reaped}\n" if reaped else "") + "---\n\n# x\n"
        (d / "README.md").write_text(fm, encoding="utf-8", newline="\n")

    def test_find_only_due_and_not_reaped(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            self.archived(v, "old", "2026-10-01")
            self.archived(v, "today", "2026-10-12")
            self.archived(v, "future", "2026-10-30")
            self.archived(v, "done-already", "2026-10-01", reaped="2026-10-05")
            self.assertEqual([n for n, _a, _d in room.find_reapable(ctx_for(v))], ["old", "today"])

    def test_reap_removes_history_and_tmp_only_for_that_project_and_marks(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v = make_vault(tmp)
            self.archived(v, "old", "2026-10-01")
            c = ctx_for(v, wsl)
            self.assertEqual(room.offer_reap(c, yes=True), 1)
            text = wsl.scripts[-1][1]
            self.assertIn("-mnt-room-old", text)
            self.assertIn("$HOME/tmp/old", text)
            self.assertNotIn("-mnt-room-old-", text)
            # 確認の ls は、対象が消えていると終了コード 2 を返す。スクリプト全体が失敗にならないよう || true で終える（実機で発見: 2026-10-18）
            self.assertTrue(text.rstrip().endswith("|| true"))
            self.assertIn("reaped: 2026-10-12", (v / "archives/old/README.md").read_text(encoding="utf-8"))
            self.assertEqual(room.find_reapable(c), [])

    def test_reap_warns_about_home_history_without_deleting_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            orig = wsl.script
            wsl.script = lambda d, t, root=False: (0, "remain\n", "") if "-home-ai" in t and t.startswith("test -d") else orig(d, t, root)
            v = make_vault(tmp)
            self.archived(v, "old", "2026-10-01")
            said = []
            c = ctx_for(v, wsl)
            c.say = said.append
            self.assertEqual(room.offer_reap(c, yes=True), 1)
            self.assertTrue(any("-home-ai" in s and "警告" in s for s in said))
            self.assertFalse(any("rm -rf" in s[1] and "-home-ai" in s[1] for s in wsl.scripts))

    def test_unsafe_name_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v = make_vault(tmp)
            self.archived(v, "a b;rm", "2026-10-01")
            with self.assertRaises(room.RoomError):
                room.reap_project(ctx_for(v, wsl), "a b;rm", "area-x")
            self.assertEqual(wsl.scripts, [])

    def test_cmd_reap_named_requires_due_unless_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            self.archived(v, "future", "2026-10-30")
            a = lambda: argparse.Namespace(name="future", yes=True, force=False)
            with self.assertRaises(room.RoomError):
                room.cmd_reap(ctx_for(v), a())
            room.cmd_reap(ctx_for(v), argparse.Namespace(name="future", yes=True, force=True))
            self.assertIn("reaped", (v / "archives/future/README.md").read_text(encoding="utf-8"))


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

    def test_start_snapshots_area_readme_readonly_during_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            seen = {}

            def during():
                f = v / "projects/proj-a/ai/ctx/area-README.md"
                seen["exists"] = f.exists()
                seen["same"] = f.read_text(encoding="utf-8") == (v / "areas/area-x/README.md").read_text(encoding="utf-8")
                seen["readonly"] = not os.stat(f).st_mode & stat.S_IWRITE
            wsl.on_interactive = during
            room.cmd_start(c, self.args())
            self.assertEqual(seen, {"exists": True, "same": True, "readonly": True})
            self.assertFalse((v / "projects/proj-a/ai/ctx").exists(), "ctx は消える")
            self.assertFalse(any("Area の README が大きい" in m for m in c.msgs))

    def test_start_warns_when_area_readme_is_large(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            readme = v / "areas/area-x/README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "x" * (room.AREA_README_WARN_BYTES + 1) + "\n",
                              encoding="utf-8")
            room.cmd_start(c, self.args())
            self.assertTrue(any("Area の README が大きい" in m for m in c.msgs))

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

    def test_restore_stops_when_final_was_edited_by_human(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c, p = self.setup_project(tmp, wsl)
            write = lambda: (p / "ai/out/report.md").write_text("⟦CUST_001⟧ の売上は増加\n", encoding="utf-8", newline="\n")
            wsl.on_interactive = write
            room.cmd_start(c, self.args())
            final = p / "_noai/final/report.md"
            final.write_text("人が直した\n", encoding="utf-8", newline="\n")
            (p / "ai/out/report.md").write_text("⟦CUST_001⟧ の売上は減少\n", encoding="utf-8", newline="\n")
            k, problems = room.restore_project(c, room.Project.load(c, "proj-a"))
            self.assertEqual(k, 0)
            self.assertIn("report.md", problems[0])
            self.assertEqual(final.read_text(encoding="utf-8"), "人が直した\n")
            k, problems = room.restore_project(c, room.Project.load(c, "proj-a"), force=True)
            self.assertEqual((k, problems), (1, []))
            self.assertIn("減少", final.read_text(encoding="utf-8"))
            # AI だけが変えたときは止まらない
            (p / "ai/out/report.md").write_text("⟦CUST_001⟧ の売上は横ばい\n", encoding="utf-8", newline="\n")
            self.assertEqual(room.restore_project(c, room.Project.load(c, "proj-a"))[1], [])

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

    def test_broken_bracket_in_explanation_stops_with_hint(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c, p = self.setup_project(tmp, wsl)
            wsl.on_interactive = lambda: (p / "ai/out/r.md").write_text("形は ⟦CUST_nnn⟧ です\n", encoding="utf-8", newline="\n")
            with self.assertRaises(room.RoomError) as cm:
                room.cmd_start(c, self.args())
            self.assertIn("括弧を外す", str(cm.exception))
            self.assertFalse((p / "_noai/final/r.md").exists())
            self.assertFalse(wsl.mounted)


class PullKnowledgeTest(unittest.TestCase):
    MASK = '[terms.CUST]\nacme = ["アクメ商事株式会社", "アクメ商事"]\n'

    def note(self, org, status="active", body="アクメ商事の件。決定: 切替は11月\n"):
        return f"---\ntype: area-note\nkind: meeting\nstatus: {status}\norg:\n  - {org}\n---\n\n# 定例\n\n{body}"

    def setup_area(self, tmp, wsl=None):
        v, c = opened(tmp, wsl)
        p = v / "projects/proj-a"
        (p / "_noai/mask.toml").write_text(self.MASK, encoding="utf-8", newline="\n")
        k = v / "areas/area-x/knowledge"
        k.mkdir()
        (k / "2026-10-14-アクメ商事-定例.md").write_text(self.note("アクメ商事"), encoding="utf-8", newline="\n")
        (k / "2026-10-15-other.md").write_text(self.note("自社", body="自社のみ\n"), encoding="utf-8", newline="\n")
        (k / "2026-10-01-old.md").write_text(self.note("アクメ商事", status="superseded"), encoding="utf-8", newline="\n")
        return v, c, p, k

    def pull(self, c, **kw):
        d = dict(name="proj-a", where=["org=アクメ商事"], yes=True)
        d.update(kw)
        room.cmd_pull(c, argparse.Namespace(**d))

    def test_pull_filters_and_hides_real_file_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, k = self.setup_area(tmp)
            self.pull(c)
            names = sorted(f.name for f in (p / "_noai/raw/area").iterdir())
            self.assertEqual(len(names), 1)  # org 一致かつ status: active の1件だけ
            self.assertTrue(names[0].startswith("2026-10-14-"))
            self.assertNotIn("アクメ", names[0])
            src = json.loads((p / "_noai/map/pull-sources.json").read_text(encoding="utf-8"))
            self.assertEqual(list(src.values()), ["2026-10-14-アクメ商事-定例.md"])

    def test_pull_then_start_then_integrated_note_returns_to_area(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c, p, k = self.setup_area(tmp, wsl)
            self.pull(c)
            seen = {}

            def ai():
                f = next((p / "ai/in/area").iterdir())
                seen["in"] = f.read_text(encoding="utf-8")
                seen["name"] = f.name
                (p / "ai/out/knowledge").mkdir(parents=True)
                (p / "ai/out/knowledge/topic-cutover.md").write_text("---\nkind: integrated\n---\n⟦CUST_001⟧ の切替は11月\n", encoding="utf-8", newline="\n")
            wsl.on_interactive = ai
            room.cmd_start(c, argparse.Namespace(name="proj-a", cmd="claude", no_launch=False, adopt=False, commit=False, yes=True))
            self.assertNotIn("アクメ", seen["in"])
            self.assertNotIn("アクメ", seen["name"])
            self.assertIn("⟦CUST_001⟧", seen["in"])
            self.assertIn("アクメ商事株式会社 の切替は11月", (k / "topic-cutover.md").read_text(encoding="utf-8"))
            man = (p / "ai/records/manifest.json").read_text(encoding="utf-8")
            self.assertNotIn("アクメ", man)
            self.assertIn("pull-sources.json", man)

    def test_changed_area_file_stops_restore_unless_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c, p, k = self.setup_area(tmp, wsl)
            out = p / "ai/out/knowledge"
            out.mkdir(parents=True)
            (out / "t.md").write_text("⟦CUST_001⟧ v1\n", encoding="utf-8", newline="\n")
            self.pull(c)
            room.mask_project(c, room.Project.load(c, "proj-a"), yes=True)
            self.assertEqual(room.restore_project(c, room.Project.load(c, "proj-a")), (1, []))
            self.assertEqual(room.restore_project(c, room.Project.load(c, "proj-a")), (1, []))  # 人が変えていなければ止まらない
            (k / "t.md").write_text("人が直した\n", encoding="utf-8", newline="\n")
            (out / "t.md").write_text("⟦CUST_001⟧ v2\n", encoding="utf-8", newline="\n")
            n, problems = room.restore_project(c, room.Project.load(c, "proj-a"))
            self.assertEqual(n, 0)
            self.assertIn("t.md", problems[0])
            self.assertEqual((k / "t.md").read_text(encoding="utf-8"), "人が直した\n")  # 何も書かない
            self.assertFalse((p / "_noai/final/_prev").exists())
            self.assertEqual(room.restore_project(c, room.Project.load(c, "proj-a"), force=True)[1], [])
            self.assertIn("v2", (k / "t.md").read_text(encoding="utf-8"))
            self.assertEqual((p / "_noai/final/_prev/knowledge/t.md").read_text(encoding="utf-8"), "人が直した\n")

    def test_restore_without_knowledge_dir_stops_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, k = self.setup_area(tmp)
            self.pull(c)
            room.mask_project(c, room.Project.load(c, "proj-a"), yes=True)
            out = p / "ai/out/knowledge"
            out.mkdir(parents=True)
            (out / "t.md").write_text("⟦CUST_001⟧ v1\n", encoding="utf-8", newline="\n")
            shutil.rmtree(k)
            n, problems = room.restore_project(c, room.Project.load(c, "proj-a"))
            self.assertEqual(n, 0)
            self.assertIn("room init area-x", problems[0])
            self.assertFalse(k.exists())
            self.assertFalse((p / "_noai/final/knowledge").exists())

    def test_bad_names_and_options_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, k = self.setup_area(tmp)
            out = p / "ai/out/knowledge"
            out.mkdir(parents=True)
            (out / "⟦CUST_001⟧.md").write_text("x\n", encoding="utf-8", newline="\n")
            k_, problems = room.restore_project(c, room.Project.load(c, "proj-a"))
            self.assertEqual(k_, 0)
            self.assertIn("プレースホルダー", problems[0])
            self.assertFalse((k / "⟦CUST_001⟧.md").exists())
            with self.assertRaises(room.RoomError):
                self.pull(c, where=["org"])
            (v / "projects/proj-a/README.md").write_text(
                (v / "projects/proj-a/README.md").read_text(encoding="utf-8").replace("---\n", "---\nknowledge_dest: ../x\n", 1),
                encoding="utf-8", newline="\n")
            with self.assertRaises(room.RoomError):
                self.pull(c)

    def test_pull_refuses_unless_restore_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, k = self.setup_area(tmp)
            readme = p / "README.md"
            readme.write_text(readme.read_text(encoding="utf-8").replace("data: restore", "data: mask"), encoding="utf-8", newline="\n")
            with self.assertRaises(room.RoomError):
                self.pull(c)


class DataModeTest(unittest.TestCase):
    def open_with(self, tmp, wsl=None, **kw):
        v = make_vault(tmp)
        c = ctx_for(v, wsl)
        d = dict(name="proj-a", area="area-x", type="doc", boundary=None, commit=True)
        d.update(kw)
        room.cmd_open(c, argparse.Namespace(**d))
        return v, c, v / "projects/proj-a"

    def args(self, **kw):
        d = dict(name="proj-a", cmd="claude", no_launch=False, adopt=False, commit=False, yes=True)
        d.update(kw)
        return argparse.Namespace(**d)

    def test_open_creates_dirs_per_mode(self):
        for data, want, not_want in (("none", ["user"], ["raw", "map", "final"]),
                                     ("mask", ["raw", "map", "user"], ["final"]),
                                     ("restore", ["raw", "map", "final", "user"], [])):
            with tempfile.TemporaryDirectory() as tmp:
                _v, _c, p = self.open_with(tmp, data=data)
                for d in want:
                    self.assertTrue((p / "_noai" / d).is_dir(), (data, d))
                for d in not_want:
                    self.assertFalse((p / "_noai" / d).exists(), (data, d))
                self.assertIn(f"data: {data}\n", (p / "README.md").read_text(encoding="utf-8"))

    def test_default_is_none_for_every_type(self):
        for t in ("doc", "research"):
            with tempfile.TemporaryDirectory() as tmp:
                _v, _c, p = self.open_with(tmp, type=t)
                self.assertIn("data: none\n", (p / "README.md").read_text(encoding="utf-8"))
                self.assertFalse((p / "_noai/raw").exists())
        with tempfile.TemporaryDirectory() as tmp:
            _v, c, p = self.open_with(tmp, type="dev")
            self.assertIn("data: none\n", (p / "README.md").read_text(encoding="utf-8"))
            self.assertFalse(any("警告" in m for m in c.msgs))

    def test_dev_with_mask_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            _v, c, p = self.open_with(tmp, type="dev", data="mask")
            self.assertTrue(any("仕様外" in m for m in c.msgs))

    def test_missing_data_means_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            _v, c, p = self.open_with(tmp)
            text = (p / "README.md").read_text(encoding="utf-8").replace("data: none\n", "")
            (p / "README.md").write_text(text, encoding="utf-8", newline="\n")
            self.assertEqual(room.Project.load(c, "proj-a").data, "restore")

    def test_none_refuses_raw_originals(self):
        with tempfile.TemporaryDirectory() as tmp:
            _v, c, p = self.open_with(tmp, data="none")
            (p / "_noai/raw").mkdir()
            (p / "_noai/raw/a.csv").write_text("x\n", encoding="utf-8")
            with self.assertRaises(room.RoomError) as cm:
                room.cmd_start(c, self.args())
            self.assertIn("data: none", str(cm.exception))

    def test_mask_only_masks_and_does_not_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            _v, c, p = self.open_with(tmp, wsl, data="mask")
            (p / "_noai/mask.toml").write_text('[terms.CUST]\nacme = ["アクメ商事"]\n', encoding="utf-8", newline="\n")
            (p / "_noai/raw/議事録.md").write_text("アクメ商事との定例\n", encoding="utf-8", newline="\n")
            seen = {}

            def ai():
                seen["in"] = (p / "ai/in/議事録.md").read_text(encoding="utf-8")
                (p / "ai/work/要点.md").write_text("⟦CUST_001⟧ の要点\n", encoding="utf-8", newline="\n")
                (p / "ai/out/tool.py").write_text("print(1)\n", encoding="utf-8", newline="\n")  # 復元できない形式でも止まらない
            wsl.on_interactive = ai
            room.cmd_start(c, self.args())
            self.assertNotIn("アクメ", seen["in"])
            self.assertFalse((p / "_noai/final").exists())
            self.assertFalse(wsl.mounted)

    def test_restore_command_refuses_unless_restore_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            _v, c, _p = self.open_with(tmp, data="mask")
            with self.assertRaises(room.RoomError):
                room.cmd_restore(c, argparse.Namespace(name="proj-a", force=False))


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
            (r / "topics").mkdir()
            (r / "topics/x.md").write_text("no", encoding="utf-8")
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
            self.assertFalse([n for n in names if ".venv" in n or "topics" in n])
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

    def test_explain_kind_is_carried_and_never_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, r, base = self.setup(tmp)
            p = v / "projects/proj-a"
            (r / "exmem/lessons/topic-a.md").write_text("v2\n", encoding="utf-8")
            sh(r, "add", "-A"); sh(r, "commit", "-qm", "c2")
            (p / "ai/out/stock").mkdir(parents=True)
            draft = self.DRAFT.format(base=base).replace("type: inbox\n", "type: inbox\nkind: explain\n")
            (p / "ai/out/stock/2026-10-12-topic-a.md").write_text(draft, encoding="utf-8")
            room.cmd_stock(c, self.ns())
            got = (r / "exmem/inbox/2026-10-12-topic-a.md").read_text(encoding="utf-8")
            self.assertIn("kind: explain", got)
            self.assertNotIn("base_stale", got)

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
            env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))  # Windows の expanduser は USERPROFILE を見る
            for _ in range(2):
                subprocess.run([sys.executable, "-c", room.SHARED_RULE_PY], env=env, check=True)
            d = json.loads((home / ".claude/settings.json").read_text(encoding="utf-8"))
            self.assertEqual(d["model"], "x")
            self.assertEqual(d["permissions"]["deny"], ["Read(~/.ssh/**)"])
            self.assertEqual(d["permissions"]["allow"], ["Bash(ls)", "Read(~/shared/**)"])

    def test_snippet_creates_file_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, HOME=tmp, USERPROFILE=tmp)  # Windows の expanduser は USERPROFILE を見る
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


class ProjectTrustTest(unittest.TestCase):
    def run_snippet(self, home, path):
        env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
        subprocess.run([sys.executable, "-c", room.TRUST_PY.format(path=json.dumps(path))], env=env, check=True)
        return json.loads((Path(home) / ".claude.json").read_text(encoding="utf-8"))

    def test_snippet_adds_trust_keeps_existing_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".claude.json").write_text(
                json.dumps({"userID": "u", "projects": {"/mnt/room/a": {"allowedTools": ["x"]}}}), encoding="utf-8")
            self.run_snippet(tmp, "/mnt/room/b")
            d = self.run_snippet(tmp, "/mnt/room/b")
            self.assertEqual(d["userID"], "u")
            self.assertEqual(d["projects"]["/mnt/room/a"], {"allowedTools": ["x"]})
            self.assertTrue(d["projects"]["/mnt/room/b"]["hasTrustDialogAccepted"])

    def test_snippet_creates_file_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self.run_snippet(tmp, "/mnt/room/b")
            self.assertTrue(d["projects"]["/mnt/room/b"]["hasTrustDialogAccepted"])

    def test_start_installs_trust_for_the_mount_point(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            room.cmd_start(c, argparse.Namespace(name="proj-a", cmd="claude", no_launch=False, adopt=False, commit=False, yes=False))
            self.assertTrue(any("ROOM_TRUST_EOF" in s[1] and "/mnt/room/proj-a" in s[1] for s in wsl.scripts))


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


def fill_readme(p):
    """open のひな形の <...> を、実際の文に置き換える。"""
    text = (p / "README.md").read_text(encoding="utf-8")
    for m in room.README_PLACEHOLDERS:
        text = "\n".join("記入済み" if m in line else line for line in text.splitlines()) + "\n"
    (p / "README.md").write_text(text, encoding="utf-8", newline="\n")


class CloseTest(unittest.TestCase):
    def test_close_refuses_template_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            p = v / "projects/proj-a"
            (p / "ai/out/close.md").write_text("- 【案件】x\n", encoding="utf-8")
            with self.assertRaisesRegex(room.RoomError, "ひな形のまま"):
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            self.assertTrue(p.exists())

    def test_close_requires_close_md_and_unmounted(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            fill_readme(v / "projects/proj-a")
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
            fill_readme(p)
            room.scaffold_area(c, "area-x")  # inbox は init が作る（close は作らない）
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

    def test_close_without_inbox_stops_before_any_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            p = v / "projects/proj-a"
            fill_readme(p)
            (p / "ai/out/close.md").write_text("- 【案件】運用で埋める\n", encoding="utf-8")
            with self.assertRaises(room.RoomError) as e:
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            self.assertIn("room init area-x", str(e.exception))
            self.assertFalse((v / "areas/area-x/ai/docs/inbox.md").exists())
            self.assertTrue(p.exists())
            self.assertFalse((v / "archives/proj-a").exists())

    def test_init_scaffolds_area_knowledge_and_inbox_without_touching_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            room.cmd_init(ctx_for(v, FakeWsl(distros=())), argparse.Namespace(area="area-y", resume=False, boundary="internal", commit=False))
            self.assertTrue((v / "areas/area-y/knowledge").is_dir())
            self.assertEqual((v / "areas/area-y/ai/docs/inbox.md").read_text(encoding="utf-8"), room.INBOX_NEW)
            (v / "areas/area-y/ai/docs/inbox.md").write_text("既存\n", encoding="utf-8")
            room.scaffold_area(ctx_for(v, FakeWsl()), "area-y")
            self.assertEqual((v / "areas/area-y/ai/docs/inbox.md").read_text(encoding="utf-8"), "既存\n")

    def test_init_scaffolds_existing_area_even_when_room_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            with self.assertRaises(room.RoomError):
                room.cmd_init(ctx_for(v, FakeWsl()), argparse.Namespace(area="area-x", resume=False))
            self.assertTrue((v / "areas/area-x/knowledge").is_dir())

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


class ShareTarTest(unittest.TestCase):
    def test_room_code_is_not_shared_but_readme_is(self):
        import io
        import tarfile
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "AGENTS.md").write_text("a", encoding="utf-8")
            kit = root / "workflow-kit"
            (kit / "room" / "tests").mkdir(parents=True)
            (kit / "hooks.md").write_text("h", encoding="utf-8")
            for rel in ("room/README.md", "room/room.py", "room/maskkit.py", "room/pyproject.toml", "room/tests/test_x.py"):
                (kit / rel).write_text("x", encoding="utf-8")
            with tarfile.open(fileobj=io.BytesIO(__import__("gzip").decompress(room.build_share_tar(root))), mode="r") as tf:
                names = set(tf.getnames())
        self.assertIn("workflow-kit/hooks.md", names)
        self.assertIn("workflow-kit/room/README.md", names)
        self.assertNotIn("workflow-kit/room/room.py", names)
        self.assertNotIn("workflow-kit/room/maskkit.py", names)
        self.assertNotIn("workflow-kit/room/pyproject.toml", names)
        self.assertNotIn("workflow-kit/room/tests", names)
        self.assertNotIn("workflow-kit/room/tests/test_x.py", names)


if __name__ == "__main__":
    unittest.main()
