"""room.py のテスト。WSL は差し替え、一時ディレクトリの Vault（git）で `open → start → close` を通す。"""
import argparse
import contextlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
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
        self.mounted = False  # proj-a（テストの Project）のマウント
        self.others = []  # 同じ部屋でほかの Project が開いているマウント（Project 名）
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
            if "/proc/mounts | cut" in text:  # cmd_umount は部屋の全マウントを外す
                self.others = []
        if text == "id -un\n":
            return 0, getattr(self, "default_user", "ai") + "\n", ""
        if text.startswith("echo user="):
            return 0, getattr(self, "isolation", "user=ai\nc=0\ncmd=no\nsudo=no\n"), ""
        if text.startswith("export PATH") and "claude --version" in text:
            return 0, "2.1.296 (Claude Code)\n", ""
        if text.startswith("grep ' /mnt/room/' /proc/mounts"):
            names = (["proj-a"] if self.mounted else []) + self.others
            return 0, "".join(f"C:\\x /mnt/room/{n} 9p rw 0 0\n" for n in names), ""
        return 0, "", ""

    def install(self, distro, base):
        self.installed = (distro, base)
        self._distros.append(distro)
        return 0

    def terminate(self, distro):
        self.terminated = getattr(self, "terminated", []) + [distro]

    def export(self, distro, tar):
        self.exports = getattr(self, "exports", []) + [distro]
        return getattr(self, "export_rc", 0)

    def import_(self, distro, dest, tar):
        self.imports = getattr(self, "imports", []) + [(distro, str(dest))]
        if getattr(self, "import_rc", 0) == 0:
            self._distros.append(distro)
        return getattr(self, "import_rc", 0)

    def unregister(self, distro):
        self.unregistered = getattr(self, "unregistered", []) + [distro]
        if distro in self._distros:
            self._distros.remove(distro)
        return 0

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
    room.cmd_open(c, argparse.Namespace(name="proj-a", area="area-x", type="dev", boundary=None, commit=True))
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


TOKEN1 = "a" * 30 + ".b" * 10
TOKEN2 = "c" * 30 + ".d" * 10


class GatewayTest(unittest.TestCase):
    def args(self, **kw):
        d = dict(name="proj-a", cmd="claude", no_launch=False, adopt=False, commit=False, yes=False, gateway=True)
        d.update(kw)
        return argparse.Namespace(**d)

    def setup_gw(self, tmp, c, tokens):
        g = Path(tmp) / "gw"
        g.mkdir()
        (g / "settings.json").write_text(json.dumps({
            "apiKeyHelper": "claude-gateway-token.cmd", "model": "sonnet", "env": {"ANTHROPIC_BASE_URL": "https://gw.example"},
            "hooks": {"x": "C:\\win.cmd"}, "permissions": {"allow": []}}), encoding="utf-8")
        c.gateway_dir = g
        c.gateway_token = lambda: tokens.pop(0) if len(tokens) > 1 else tokens[0]
        return g

    def test_start_pushes_settings_and_token_then_removes_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            self.setup_gw(tmp, c, [TOKEN1])
            room.cmd_start(c, self.args())
            gw = [s[1] for s in wsl.scripts if ".claude-gateway" in s[1]]
            self.assertEqual(len(gw), 2)
            push, rm = gw
            self.assertIn("<<'ROOM_GW_EOF'", push)
            self.assertIn('"apiKeyHelper": "cat \\"$HOME/.claude-gateway/token\\""', push)
            self.assertIn("https://gw.example", push)
            self.assertNotIn("hooks", push)  # Windows のコマンドは部屋へ写さない
            self.assertNotIn("permissions", push)
            self.assertIn("chmod 600", push)
            self.assertIn("mv \"$d/token.new\" \"$d/token\"", push)  # 横で完成させてから置き換える
            self.assertIn(TOKEN1, push)
            self.assertTrue(rm.startswith("rm -f") and "token" in rm and TOKEN1 not in rm)
            self.assertFalse(any(TOKEN1 in m for m in c.msgs))
            cmd = wsl.interactive_calls[0][1]
            self.assertIn('CLAUDE_CONFIG_DIR="$HOME/.claude-gateway"', cmd)
            self.assertIn("-u CLAUDE_CODE_USE_BEDROCK", cmd)
            self.assertTrue(cmd.endswith(" claude"))
            self.assertLess(wsl.scripts.index(next(s for s in wsl.scripts if s[1] == push)), wsl.scripts.index(next(s for s in wsl.scripts if s[1] == rm)))

    def test_token_is_refreshed_while_the_session_runs(self):
        import time
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            self.setup_gw(tmp, c, [TOKEN1, TOKEN2])
            c.gateway_interval = 0.05
            wsl.on_interactive = lambda: time.sleep(0.4)
            room.cmd_start(c, self.args())
            pushes = [s[1] for s in wsl.scripts if "token.new" in s[1] and "printf" in s[1]]
            self.assertIn(TOKEN1, pushes[0])
            self.assertGreaterEqual(len(pushes), 2)
            self.assertIn(TOKEN2, pushes[1])
            self.assertNotIn("settings.json.new", pushes[1])  # 更新は token だけ

    def test_refresh_failure_is_reported_after_the_session(self):
        import time
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            calls = []

            def tok():
                calls.append(1)
                if len(calls) > 1:
                    raise room.RoomError("expired")
                return TOKEN1
            self.setup_gw(tmp, c, [TOKEN1])
            c.gateway_token = tok
            c.gateway_interval = 0.05
            wsl.on_interactive = lambda: (time.sleep(0.3), self.assertFalse(any("失敗" in m for m in c.msgs)))
            room.cmd_start(c, self.args())
            self.assertTrue(any("更新に" in m and "失敗" in m for m in c.msgs))

    def test_missing_settings_or_bad_token_stops_before_mounting(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            c.gateway_dir = Path(tmp) / "none"
            with self.assertRaises(room.RoomError):
                room.cmd_start(c, self.args())
            self.setup_gw(tmp, c, ["bad token"])
            with self.assertRaises(room.RoomError):
                room.cmd_start(c, self.args())
            self.assertFalse(wsl.mounted)
            self.assertEqual(wsl.interactive_calls, [])

    def test_fetch_asks_for_a_token_valid_past_the_next_push(self):
        # 残り2分まで同じトークンを返す既定のままだと、50分後に約10分で切れるトークンを押してしまう
        done = subprocess.CompletedProcess([], 0, stdout=TOKEN1.encode(), stderr=b"")
        with mock.patch.object(room.shutil, "which", return_value="claude-gateway-token.cmd"), \
                mock.patch.object(room.subprocess, "run", return_value=done) as run:
            self.assertEqual(room.fetch_gateway_token(), TOKEN1)
        argv = run.call_args[0][0]
        self.assertEqual(argv[1], "-MinValidSec")
        self.assertGreater(int(argv[2]), room.GATEWAY_REFRESH_SEC)

    def test_without_the_flag_nothing_is_pushed(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            room.cmd_start(c, self.args(gateway=False))
            self.assertFalse(any(".claude-gateway" in s[1] for s in wsl.scripts))
            self.assertEqual(wsl.interactive_calls[0][1], "cd /mnt/room/proj-a && claude")


class ReposTest(unittest.TestCase):
    README = ("---\nstatus: active\nrepos:\n  - url: git@github.com:o/alpha.git\n    branch: main\n"
              "  - url: https://example.com/o/beta\n    where: win\n---\n本文\n")

    def test_read_repos_defaults_where_to_wsl(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "README.md"
            f.write_text(self.README, encoding="utf-8")
            r = room.read_repos(f)
            self.assertEqual([x["where"] for x in r], ["wsl", "win"])
            self.assertEqual(r[0]["branch"], "main")
            self.assertEqual(room.repo_dir_name(r[0]["url"]), "alpha")

    def test_extra_args_only_for_wsl_repos_and_claude(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            p = room.Project.load(c, "proj-a")
            p.readme.write_text(self.README, encoding="utf-8")
            env, extra = room.claude_extra_args(c, p, "claude")
            self.assertEqual(env, "CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 ")
            self.assertEqual(extra, ' --add-dir "$HOME/src/alpha"')
            self.assertEqual(room.claude_extra_args(c, p, "bash"), ("", ""))

    def test_unpushed_repos_reports_dirty_or_ahead_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            p = room.Project.load(c, "proj-a")
            p.readme.write_text(self.README, encoding="utf-8")
            wsl.script = lambda distro, text, root=False: (0, "dirty=0\nahead=0\n", "")
            self.assertEqual(room.unpushed_repos(c, p), [])
            wsl.script = lambda distro, text, root=False: (0, "dirty=2\nahead=1\n", "")
            self.assertEqual(room.unpushed_repos(c, p), ["~/src/alpha: 未コミットの変更 2 件、remote に無いコミット 1 件"])
            wsl.script = lambda distro, text, root=False: (0, "", "")  # clone が無い
            self.assertEqual(room.unpushed_repos(c, p), [])


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
            # Marp CLI（2026-11-04）: root が版を固定して入れ、Chromium の後。room-chrome を指す包みを置く
            mp = idx("@marp-team/marp-cli@")
            self.assertTrue(scripts[mp][1])
            self.assertLess(cr, mp)
            for key in (room.MARP_CLI_VERSION, "--browser-path /usr/local/bin/room-chrome", "room-marp", "</dev/null", "PUPPETEER_SKIP_DOWNLOAD=1"):
                self.assertIn(key, scripts[mp][0])
            self.assertLess(idx("latest-v24.x"), conv)
            self.assertLess(conv, idx("astral.sh"))
            # PowerShell 7 と静的チェッカーの道具（2026-10-21）: root が、版と SHA-256 を固定して入れる
            pw = idx("/opt/microsoft/powershell/7")
            self.assertTrue(scripts[pw][1])  # root で入れる
            self.assertIn("sha256sum -c", scripts[pw][0])
            self.assertIn(room.PWSH_VERSION, scripts[pw][0])
            self.assertIn(room.PWSH_SHA256["x64"], scripts[pw][0])
            self.assertIn(room.PWSH_SHA256["arm64"], scripts[pw][0])
            for key in ("PSScriptAnalyzer", room.PSSA_VERSION, "Pester", room.PESTER_VERSION, "-Scope AllUsers",
                        "DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1", "POWERSHELL_UPDATECHECK=Off", "/usr/local/bin/pwsh"):
                self.assertIn(key, scripts[pw][0])
            self.assertNotIn("%(", scripts[pw][0])  # 書式の置換漏れが無い
            self.assertLess(cr, pw)
            self.assertLess(pw, idx("astral.sh"))
            self.assertTrue(any("pwsh --version" in t for t, _ in scripts))  # 道具の確認に入っている

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

    def test_init_without_boundary_creates_external_area(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            room.cmd_init(ctx_for(v, FakeWsl(distros=())), argparse.Namespace(area="area-y", resume=False, boundary=None, commit=True))
            self.assertIn("boundary: external", (v / "areas/area-y/README.md").read_text(encoding="utf-8"))

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
            room.cmd_open(ctx_for(v), argparse.Namespace(name="proj-a", area="area-x", type="dev", boundary=None, commit=True))
            files = self.git_out(v, "show", "--name-only", "--format=", "HEAD").split()
            self.assertNotIn("other.txt", files)
            self.assertIn("projects/proj-a/README.md", files)
            self.assertEqual(self.git_out(v, "diff", "--cached", "--name-only").split(), ["other.txt"])  # ステージに残る

    def test_open_commits_initial_state_without_other_area_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            (v / "areas" / "area-x" / "memo.md").write_text("別の編集\n", encoding="utf-8")
            room.cmd_open(ctx_for(v), argparse.Namespace(name="proj-a", area="area-x", type="dev", boundary=None, commit=True))
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

    def test_init_only_runs_selected_steps(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            wsl = FakeWsl()
            room.cmd_init(ctx_for(v, wsl), argparse.Namespace(area="area-x", resume=False, only="apt,pwsh"))
            texts = "\n".join(t for _, t, _ in wsl.scripts)
            self.assertIn("apt-get install -y -qq curl", texts)
            self.assertIn("powershell", texts.lower())
            self.assertNotIn("useradd", texts)
            self.assertNotIn("libreoffice", texts)
            self.assertNotIn("astral.sh", texts)
            self.assertFalse(hasattr(wsl, "terminated"))
            self.assertFalse(hasattr(wsl, "installed"))

    def test_init_python_step_installs_canonical_version_as_python3(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            wsl = FakeWsl()
            room.cmd_init(ctx_for(v, wsl), argparse.Namespace(area="area-x", resume=False, only="python"))
            self.assertEqual(len(wsl.scripts), 2)  # Python の段と、道具の確認だけ
            _, text, root = wsl.scripts[0]
            self.assertFalse(root)  # 部屋の一般ユーザー（ai）の ~/.local に入れる
            pyver = (Path(room.__file__).parent / ".python-version").read_text(encoding="utf-8").strip()
            self.assertIn(f"uv\" python install {pyver} --default", text)
            self.assertIn("SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt", text)
            self.assertIn("python3 --version", wsl.scripts[1][1])

    def test_python_version_rejects_unreadable_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / ".python-version"
            f.write_text("3.13.14\n", encoding="utf-8")
            with mock.patch.object(room, "PYTHON_VERSION_FILE", f):
                self.assertEqual(room.python_version(), "3.13.14")
                f.write_text("latest\n", encoding="utf-8")
                with self.assertRaises(room.RoomError):
                    room.python_version()

    def load_stop_hook(self, tmp):
        import importlib.util
        f = Path(tmp) / "room_stop_record.py"
        f.write_text(room.STOP_RECORD_PY, encoding="utf-8", newline="\n")
        spec = importlib.util.spec_from_file_location("room_stop_record", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # 構文エラー（docstring のバックスラッシュなど）もここで出る
        return mod

    def test_init_stophook_step_installs_hook_and_registers_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            wsl = FakeWsl()
            room.cmd_init(ctx_for(v, wsl), argparse.Namespace(area="area-x", resume=False, only="stophook"))
            self.assertEqual(len(wsl.scripts), 2)  # フックの設置と、道具の確認だけ
            distro, text, root = wsl.scripts[0]
            self.assertFalse(root)  # 部屋の一般ユーザー（ai）の ~/.claude に置く
            self.assertIn(f"$HOME/.claude/hooks/{room.STOP_HOOK_NAME}", text)
            self.assertIn("python3 $HOME/.claude/hooks/" + room.STOP_HOOK_NAME, text)
            self.assertIn('"Stop"', text)
            self.assertEqual(text.count("ROOM_STOP_EOF"), 2)  # heredoc の区切りが本文に混ざっていない

    def test_stop_hook_script_redacts_windows_user_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            mod = self.load_stop_hook(tmp)
            for src in ("C:\\Users\\taro\\works\\x", "c:/Users/taro/works/x", "/mnt/c/Users/taro/works/x", "/mnt/d/Users/taro/x"):
                self.assertNotIn("taro", mod.redact(src))
                self.assertIn("%USERPROFILE%", mod.redact(src))
            self.assertEqual(mod.redact("C:\\Users\\taro\\works\\x"), "%USERPROFILE%\\works\\x")
            self.assertEqual(mod.redact("/mnt/room/proj-a/ai/out"), "/mnt/room/proj-a/ai/out")  # 部屋のパスは変えない

    def test_stop_hook_script_records_into_project_ai_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            mod = self.load_stop_hook(tmp)
            self.assertEqual(mod.record_dir("/mnt/room/proj-a"), "/mnt/room/proj-a/records")  # マウント先が Project の ai/ なので、ai/ai/records にしない
            self.assertEqual(mod.record_dir("/mnt/room/proj-a/work"), "/mnt/room/proj-a/records")
            self.assertTrue(mod.record_dir("/home/ai/other").endswith(os.path.join("claude-records", "other")))
            # 本体の通し: 記録先だけ差し替えて、応答本文の置換と同じ session の行の置き換えを確かめる
            out = Path(tmp) / "records"
            mod.record_dir = lambda cwd: str(out)
            tr = Path(tmp) / "t.jsonl"
            tr.write_text(json.dumps({"type": "assistant", "message": {"id": "m1", "model": "claude-sonnet-5-5",
                                                                        "usage": {"input_tokens": 10, "output_tokens": 5}}}) + "\n", encoding="utf-8")
            import io
            for _ in range(2):
                sys.stdin = io.StringIO(json.dumps({"cwd": "/mnt/room/proj-a", "transcript_path": str(tr), "session_id": "abcdef123456",
                                                    "last_assistant_message": "開いた: C:\\Users\\taro\\x"}))
                try:
                    mod.main()
                finally:
                    sys.stdin = sys.__stdin__
            rows = (out / "sessions.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(rows), 1)  # 同じ session_id は置き換え
            self.assertEqual(json.loads(rows[0])["requests"], 1)
            reply = next((out / "replies").iterdir()).read_text(encoding="utf-8")
            self.assertIn("%USERPROFILE%\\x", reply)
            self.assertNotIn("taro", reply)

    def test_init_only_rejects_unknown_step_and_missing_room(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            wsl = FakeWsl()
            with self.assertRaises(room.RoomError):
                room.cmd_init(ctx_for(v, wsl), argparse.Namespace(area="area-x", resume=False, only="apt,nope"))
            self.assertEqual(wsl.scripts, [])
            with self.assertRaises(room.RoomError):
                room.cmd_init(ctx_for(v, FakeWsl(distros=())), argparse.Namespace(area="area-x", resume=False, only="apt"))


class MvTest(unittest.TestCase):
    def git_out(self, v, *args):
        return subprocess.run(["git", "-C", str(v), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout

    def args(self, old="area-x", new="area-z", commit=True):
        return argparse.Namespace(old=old, new=new, commit=commit)

    def test_mv_renames_area_room_links_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            (v / ".gitignore").write_text((Path(room.__file__).parent.parent / "templates" / "workspace" / "gitignore.template").read_text(encoding="utf-8"), encoding="utf-8")
            a = v / "areas" / "area-x"
            (a / "memo.md").write_text("追跡外\n", encoding="utf-8")
            (a / "docs").mkdir(exist_ok=True)
            (a / "docs" / "log.md").write_text("[[areas/area-x/memo]] と [[areas/area-x/README|area-x]]\n", encoding="utf-8")
            (a / "_noai").mkdir(exist_ok=True)
            (a / "_noai" / "src.md").write_text("[[areas/area-x/x]]\n", encoding="utf-8")
            p = room.Project.load(c, "proj-a")
            (p.ai / "in" / "a.txt").write_text("x", encoding="utf-8")
            room.adopt_in(c, p)
            (v / "projects" / "proj-a" / "docs").mkdir(exist_ok=True)
            (v / "projects" / "proj-a" / "docs" / "n.md").write_text("[[areas/area-x/README|area-x]]\n", encoding="utf-8")
            sh(v, "add", "-A")
            sh(v, "commit", "-qm", "setup")
            wsl = c.wsl
            room.cmd_mv(c, self.args())
            self.assertFalse((v / "areas" / "area-x").exists())
            self.assertTrue((v / "areas" / "area-z" / "memo.md").exists())
            self.assertEqual(wsl.exports, ["room-area-x"])
            self.assertEqual(wsl.imports[0][0], "room-area-z")
            self.assertEqual(wsl.unregistered, ["room-area-x"])
            self.assertEqual(wsl.distros(), ["room-area-z"])
            readme = (v / "projects" / "proj-a" / "README.md").read_text(encoding="utf-8")
            self.assertIn("area: area-z", readme)
            self.assertNotIn("area-x", readme)
            self.assertNotIn("area-x", (v / "projects" / "proj-a" / "docs" / "n.md").read_text(encoding="utf-8"))
            self.assertNotIn("area-x", (v / "areas" / "area-z" / "docs" / "log.md").read_text(encoding="utf-8"))
            self.assertIn("area-x", (v / "areas" / "area-z" / "_noai" / "src.md").read_text(encoding="utf-8"))
            self.assertEqual(room.Project.load(c, "proj-a").area, "area-z")
            self.assertEqual(room.check_provenance(room.Project.load(c, "proj-a")), [])
            self.assertEqual(self.git_out(v, "status", "--porcelain", "--", "areas", "projects").strip().splitlines(), [])
            self.assertIn("Room-Op: mv", self.git_out(v, "log", "-1", "--format=%B"))

    def test_mv_without_room_only_renames_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            wsl = FakeWsl(distros=())
            room.cmd_mv(ctx_for(v, wsl), self.args())
            self.assertTrue((v / "areas" / "area-z").exists())
            self.assertFalse(hasattr(wsl, "exports"))

    def test_mv_refuses_bad_missing_existing_and_mounted(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            (v / "areas" / "area-y").mkdir()
            c = ctx_for(v)
            for old, new in (("area-x", "日本語"), ("area-x", "area-x"), ("nothing", "area-z"), ("area-x", "area-y")):
                with self.assertRaises(room.RoomError):
                    room.cmd_mv(c, self.args(old, new))
            self.assertTrue((v / "areas" / "area-x").exists())
            wsl = FakeWsl()
            wsl.mounted = True
            with self.assertRaises(room.RoomError):
                room.cmd_mv(ctx_for(v, wsl), self.args())
            self.assertTrue((v / "areas" / "area-x").exists())
            wsl = FakeWsl(distros=("room-area-x", "room-area-z"))
            with self.assertRaises(room.RoomError):
                room.cmd_mv(ctx_for(v, wsl), self.args())

    def test_mv_stops_before_touching_files_when_room_rename_fails(self):
        for failure in ("export_rc", "import_rc", "default_user"):
            with tempfile.TemporaryDirectory() as tmp:
                v = make_vault(tmp)
                wsl = FakeWsl()
                setattr(wsl, failure, "root" if failure == "default_user" else 1)
                with self.assertRaises(room.RoomError):
                    room.cmd_mv(ctx_for(v, wsl), self.args())
                self.assertTrue((v / "areas" / "area-x").exists(), failure)
                self.assertFalse((v / "areas" / "area-z").exists(), failure)
                self.assertIn("room-area-x", wsl.distros(), failure)
                self.assertNotIn("room-area-z", wsl.distros(), failure)


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

    def test_reap_backs_up_history_before_deleting_and_stops_on_bad_tar(self):
        import io, tarfile

        def tar_of(name):
            buf = io.BytesIO()
            with tarfile.open(fileobj=buf, mode="w") as tf:
                data = b'{"type":"assistant"}\n'
                ti = tarfile.TarInfo(name)
                ti.size = len(data)
                tf.addfile(ti, io.BytesIO(data))
            return buf.getvalue()

        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v = make_vault(tmp)
            self.archived(v, "old", "2026-10-01")
            c = ctx_for(v, wsl)
            c.history_backup = Path(tmp) / "bk"
            wsl.tar_history = lambda distro, hist: tar_of(f"{hist}/s.jsonl")
            self.assertEqual(room.offer_reap(c, yes=True), 1)
            self.assertTrue((Path(tmp) / "bk/room-area-x/-mnt-room-old/s.jsonl").exists())
            # 不正な tar なら、消さずに止まる
            self.archived(v, "bad", "2026-10-01")
            wsl.scripts.clear()
            wsl.tar_history = lambda distro, hist: tar_of("../evil.jsonl")
            with self.assertRaises(room.RoomError):
                room.reap_project(c, "bad", "area-x")
            self.assertFalse(any("rm -rf" in s[1] for s in wsl.scripts))

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

    def test_open_puts_docs_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            d = v / "projects" / "proj-a" / "ai" / "docs"
            self.assertEqual(sorted(f.name for f in d.iterdir()), ["decisions.md", "log-history.md", "log.md"])
            tracked = subprocess.run(["git", "-C", str(v), "ls-files"], capture_output=True, text=True, encoding="utf-8").stdout
            self.assertIn("projects/proj-a/ai/docs/log.md", tracked)

    def test_open_readme_has_plan_pointer_that_is_not_a_placeholder(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            text = (v / "projects" / "proj-a" / "README.md").read_text(encoding="utf-8")
            self.assertIn("計画: `ai/work/plan/`", text)
            self.assertFalse([l for l in room.readme_placeholders(text) if "計画" in l])

    def test_open_refuses_without_gitignore_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp, gitignore="*.tmp\n")
            with self.assertRaises(room.RoomError):
                room.cmd_open(ctx_for(v), argparse.Namespace(name="p", area="area-x", type="dev", boundary=None, commit=False))

    def test_open_without_boundary_is_external_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            readme = v / "areas/area-x/README.md"
            readme.write_text("---\nstatus: active\n---\n\n# x\n", encoding="utf-8")
            room.cmd_open(ctx_for(v), argparse.Namespace(name="p", area="area-x", type="dev", boundary=None, commit=False))
            self.assertNotIn("boundary", readme.read_text(encoding="utf-8"))

    def test_open_rejects_unknown_boundary_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            with self.assertRaises(room.RoomError):
                room.cmd_open(ctx_for(v), argparse.Namespace(name="p", area="area-x", type="dev", boundary="顧客A", commit=False))


class BoundaryGuardTest(unittest.TestCase):
    def test_normalize_defaults_to_external(self):
        for v in ("", None, "external", "顧客A", "Internal "):
            self.assertEqual(room.normalize_boundary(v), "external")
        self.assertEqual(room.normalize_boundary("internal"), "internal")

    def external_project(self, tmp):
        v, c = opened(tmp)
        readme = v / "areas/area-x/README.md"
        readme.write_text(readme.read_text(encoding="utf-8").replace("boundary: internal", "boundary: external"), encoding="utf-8")
        return v, c, v / "projects/proj-a"

    def test_clean_path_is_refused_for_external_area(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.external_project(tmp)
            with self.assertRaises(room.RoomError) as cm:
                room.cmd_clean(c, argparse.Namespace(name="proj-a", path=["x"], yes=True))
            self.assertIn("internal", str(cm.exception))


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

    def _plan(self, v, status="正式", approved="2026-11-03", body="本文\n"):
        f = v / "projects" / "proj-a" / "ai" / "work" / "plan" / "6r.md"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"---\nstatus: {status}\napproved: {approved}\n---\n{body}", encoding="utf-8")
        return f

    def _plans(self, v):
        mp = v / "projects/proj-a/ai/records/manifest.json"
        return json.loads(mp.read_text(encoding="utf-8")).get("plans", {}) if mp.exists() else {}

    def test_plan_approval_records_and_detects_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            f = self._plan(v)
            room.cmd_start(c, self.args())
            self.assertIn("ai/work/plan/6r.md", self._plans(v))
            room.cmd_start(c, self.args())
            self.assertEqual(room.read_frontmatter(f)["status"], "正式")
            f.write_text(f.read_text(encoding="utf-8") + "AI が足した\n", encoding="utf-8")
            room.cmd_start(c, self.args())
            self.assertEqual(room.read_frontmatter(f)["status"], "仮")
            self.assertTrue(any("変更されている" in m for m in c.msgs))
            self.assertNotIn("ai/work/plan/6r.md", self._plans(v))

    def test_plan_reapproval_by_new_date_rerecords(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            f = self._plan(v)
            room.cmd_start(c, self.args())
            self._plan(v, approved="2026-11-05", body="直した\n")
            room.cmd_start(c, self.args())
            self.assertEqual(room.read_frontmatter(f)["status"], "正式")
            self.assertEqual(self._plans(v)["ai/work/plan/6r.md"]["approved"], "2026-11-05")

    def test_plan_draft_is_not_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            self._plan(v, status="仮")
            room.cmd_start(c, self.args())
            self.assertEqual(self._plans(v), {})

    def test_start_sets_up_and_discards_room_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            room.cmd_start(c, self.args())
            texts = [s[1] for s in wsl.scripts if s[2]]
            setup = [t for t in texts if "git init" in t]
            self.assertEqual(len(setup), 1)
            self.assertIn("GIT_DIR=/home/ai/gitdirs/proj-a", setup[0])
            self.assertIn("GIT_WORK_TREE=/mnt/room/proj-a", setup[0])
            self.assertIn("runuser -u ai", setup[0])
            self.assertTrue(texts.index(setup[0]) > texts.index([t for t in texts if "mount -t drvfs" in t][0]), "マウントの後")
            self.assertTrue(any(t.startswith("rm -rf /home/ai/gitdirs/proj-a") for t in texts), "回収の後に捨てる")

    def test_start_continues_when_room_git_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            orig = wsl.script
            wsl.script = lambda d, t, root=False: (1, "", "boom") if "git init" in t else orig(d, t, root)
            v, c = opened(tmp, wsl)
            room.cmd_start(c, self.args())
            self.assertTrue(any("部屋の git を用意できなかった" in m for m in c.msgs))
            self.assertFalse(wsl.mounted)

    def test_start_commits_by_default(self):
        self.assertTrue(room.build_parser().parse_args(["start", "x"]).commit)
        self.assertFalse(room.build_parser().parse_args(["start", "x", "--no-commit"]).commit)

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

    def test_unmount_retries_and_reports_holders(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            p = room.Project.load(c, "proj-a")
            wsl.mounted = True
            wsl.script_orig = wsl.script
            # umount が効かない（busy）部屋を模す
            def busy(distro, text, root=False):
                rc, out, err = wsl.script_orig(distro, text, root)
                if "umount" in text:
                    wsl.mounted = True
                if "/proc/[0-9]*" in text:
                    return 0, "123 cwd zed-remote-server\n", ""
                return rc, out, err
            wsl.script = busy
            self.assertFalse(room.unmount(c, p))
            self.assertIn("seq 1 10", wsl.scripts[0][1])
            self.assertIn("zed-remote-server", p.holders)

    def test_start_blocked_by_existing_mount(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            wsl.mounted = True
            with self.assertRaises(room.RoomError) as cm:
                room.cmd_start(c, self.args())
            self.assertIn("マウントが残っている", str(cm.exception))
            self.assertEqual(wsl.interactive_calls, [])

    def test_start_allows_other_project_mounted_in_same_room(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            wsl.others = ["proj-b"]
            v, c = opened(tmp, wsl)
            room.cmd_start(c, self.args())
            self.assertEqual(len(wsl.interactive_calls), 1)
            self.assertTrue(any("proj-b" in m and "並行" in m for m in c.msgs))
            self.assertFalse(wsl.mounted)
            self.assertEqual(wsl.others, ["proj-b"], "ほかの Project のマウントは外さない")

    def test_start_does_not_fail_when_other_project_stays_mounted(self):
        # 自分のマウントだけを確認する（ほかの Project が動いていても「マウントが残っている」にならない）
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            wsl.others = ["proj-b", "proj-c"]
            v, c = opened(tmp, wsl)
            room.cmd_start(c, self.args())
            self.assertIn("proj-b", "".join(wsl.others))

    def test_stale_cleanup_spares_fresh_mountpoints(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            room.cmd_start(c, self.args())
            cleans = [s[1] for s in wsl.scripts if s[1].startswith("find /mnt/room") and "-empty" in s[1]]
            self.assertTrue(cleans and all("-mmin +1" in t for t in cleans))

    def test_close_ignores_other_project_mounts(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            wsl.others = ["proj-b"]
            v, c = opened(tmp, wsl)
            fill_readme(v / "projects/proj-a")
            (v / "projects/proj-a/ai/out/close.md").write_text("- 【案件】x\n", encoding="utf-8")
            # マウントの確認では止まらない（ほかの理由で止まっても、マウントの理由ではない）
            try:
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            except room.RoomError as e:
                self.assertNotIn("マウントが残っている", str(e))

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


class AllowlistGitignoreTest(unittest.TestCase):
    """works の .gitignore の雛形は許可リスト方式（2026-10-29）。追跡する・しないを、実際の git で確かめる。"""

    TRACKED = ("README.md", "AGENTS.md", "docs/log.md", "areas/.gitkeep", "areas/a/README.md", "archives/old/docs/design.md",
               "projects/p/README.md", "projects/p/ai/docs/log.md", "areas/a/ai/docs/inbox.md", ".gitattributes")
    IGNORED = ("projects/p/ai/out/x/report.xlsx", "projects/p/ai/records/replies/2026-10-29.md", "projects/p/ai/in/a.md",
               "projects/p/ai/work/t.py", "projects/p/_noai/raw/x.xlsx", "projects/p/ai/ctx/README.md", "archives/old/src/pool.c",
               "resources/x/README.md", "repos/r/README.md", ".claude/settings.local.json", "~$a.xlsx",
               "docs/~$a.xlsx", "projects/p/ai/docs/~$b.docx", "docs/Thumbs.db", "areas/a/docs/desktop.ini")

    def test_template_tracks_only_the_allowlist(self):
        tpl = (KIT_TEMPLATES / "workspace" / "gitignore.template").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp, gitignore=tpl)
            for rel in self.TRACKED + self.IGNORED:
                (v / rel).parent.mkdir(parents=True, exist_ok=True)
                (v / rel).write_text("x", encoding="utf-8")
            ignored = lambda rel: subprocess.run(["git", "-C", str(v), "check-ignore", "-q", rel]).returncode == 0
            self.assertEqual([r for r in self.TRACKED if ignored(r)], [])
            self.assertEqual([r for r in self.IGNORED if not ignored(r)], [])
            self.assertTrue(room.is_allowlist_vault(ctx_for(v)))

    def test_old_style_vault_is_not_allowlist(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(room.is_allowlist_vault(ctx_for(make_vault(tmp))))


class PullSourceTest(unittest.TestCase):
    MASK = '[terms.CUST]\nacme = ["アクメ商事株式会社", "アクメ商事"]\n'

    def setup_area(self, tmp, wsl=None):
        v, c = opened(tmp, wsl)
        p = v / "projects/proj-a"
        (p / "_noai/mask.toml").write_text(self.MASK, encoding="utf-8", newline="\n")
        k = v / "areas/area-x/_noai/knowledge"  # 知識の経路は外した（作られない）
        (v / "areas/area-x/_noai/deliverable").mkdir(parents=True, exist_ok=True)
        sd = v / "areas/area-x/_noai/source"
        sd.mkdir(parents=True, exist_ok=True)
        (sd / "議事録.md").write_text("アクメ商事の件。決定: 切替は11月\n", encoding="utf-8", newline="\n")
        return v, c, p, k

    def place_raw(self, p, v):
        """Project 固有の原本として、議事録.md を _noai/raw に直接置く。"""
        (p / "_noai/raw/議事録.md").write_bytes((v / "areas/area-x/_noai/source/議事録.md").read_bytes())

    def test_clean_path_needs_a_path_inside_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, k = self.setup_area(tmp)
            for bad in (None, ["../knowledge/*.md"], ["/etc/passwd"]):
                with self.assertRaises(room.RoomError):
                    room.cmd_clean(c, argparse.Namespace(name="proj-a", path=bad, yes=True)) if bad else room.pick_source_files(v / "areas/area-x/_noai/source", bad)

    def deliver(self, c, p):
        """close が Area へ渡す処理（点検 → 書き出し）。問題があれば何も書かず一覧を返す。"""
        pr = room.Project.load(c, p)
        items, problems = room.deliverable_items(pr)
        plans, errors, conflicts = room.deliver_plan(pr, items)
        problems = problems + errors + conflicts
        if not problems:
            room.deliver_write(c, pr, plans)
        return len(items), problems

    def test_deliverable_goes_to_area_as_is(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, _k = self.setup_area(tmp)
            d = p / "ai/out/deliverable"
            d.mkdir(parents=True)
            (d / "report.md").write_text("報告\n", encoding="utf-8", newline="\n")
            (p / "ai/out/tool.py").write_text("print(1)\n", encoding="utf-8", newline="\n")
            self.assertEqual(self.deliver(c, "proj-a"), (1, []))
            self.assertEqual((v / "areas/area-x/_noai/deliverable/proj-a/report.md").read_text(encoding="utf-8"), "報告\n")
            (d / "report.md").write_text("改訂\n", encoding="utf-8", newline="\n")
            self.assertEqual(self.deliver(c, "proj-a"), (1, []))
            (v / "areas/area-x/_noai/deliverable/proj-a/report.md").write_text("人の変更\n", encoding="utf-8", newline="\n")
            (d / "report.md").write_text("再改訂\n", encoding="utf-8", newline="\n")
            n, problems = self.deliver(c, "proj-a")
            self.assertTrue(problems)
            self.assertEqual((v / "areas/area-x/_noai/deliverable/proj-a/report.md").read_text(encoding="utf-8"), "人の変更\n")

    def test_deliverable_without_area_dir_stops_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, _k = self.setup_area(tmp)
            (v / "areas/area-x/_noai/deliverable").rmdir()
            d = p / "ai/out/deliverable"
            d.mkdir(parents=True)
            (d / "report.md").write_text("x\n", encoding="utf-8", newline="\n")
            n, problems = self.deliver(c, "proj-a")
            self.assertIn("成果物の置き場が無い", problems[0])
            self.assertFalse((v / "areas/area-x/_noai/deliverable").exists())


class NoDataModeTest(unittest.TestCase):
    """open が作るディレクトリと README。"""

    def open_with(self, tmp, wsl=None, **kw):
        v = make_vault(tmp)
        c = ctx_for(v, wsl)
        d = dict(name="proj-a", area="area-x", type="dev", boundary=None, commit=True)
        d.update(kw)
        room.cmd_open(c, argparse.Namespace(**d))
        return v, c, v / "projects/proj-a"

    def args(self, **kw):
        d = dict(name="proj-a", cmd="claude", no_launch=False, adopt=False, commit=False, yes=True)
        d.update(kw)
        return argparse.Namespace(**d)

    def test_open_creates_every_noai_dir(self):
        for t in ("dev", "inv"):
            with tempfile.TemporaryDirectory() as tmp:
                _v, c, p = self.open_with(tmp, type=t)
                for d in ("raw", "map", "user"):
                    self.assertTrue((p / "_noai" / d).is_dir(), (t, d))
                self.assertFalse((p / "_noai/final").exists())
                self.assertIn(f"type: {t}\n", (p / "README.md").read_text(encoding="utf-8"))
                self.assertFalse(any("警告" in m for m in c.msgs))

    def test_open_writes_a_valid_terms_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            _v, _c, p = self.open_with(tmp)
            self.assertEqual((p / "_noai/mask.toml").read_text(encoding="utf-8"), room.MASK_TOML_TEMPLATE)
            self.assertEqual(room.cleankit.load_terms(p / "_noai/mask.toml"), [])

    def test_type_is_dev_or_inv_and_defaults_to_dev(self):
        parse = room.build_parser().parse_args
        self.assertEqual(parse(["open", "x", "--area", "a"]).type, "dev")
        self.assertEqual(parse(["open", "x", "--area", "a", "--type", "inv"]).type, "inv")
        for old in ("doc", "dev-env", "dev-test", "research"):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                parse(["open", "x", "--area", "a", "--type", old])

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
            self.assertIn("flock 9", script, "並行 start の送付を直列にする")
            self.assertIn('mv "$HOME/shared.new" "$HOME/shared"', script, "横で展開してから置き換える（読む最中に無い時間を作らない）")
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



class StockAreaTest(unittest.TestCase):
    def setup(self, tmp, boundary="external"):
        v, c = opened(tmp)
        ar = v / "areas/area-x/README.md"
        ar.write_text(ar.read_text(encoding="utf-8").replace("boundary: internal", f"boundary: {boundary}"), encoding="utf-8", newline="\n")
        return v, c, v / "projects/proj-a"

    def ns(self, **kw):
        d = dict(name="proj-a", yes=True, dst="area")
        d.update(kw)
        return argparse.Namespace(**d)

    def put(self, p, name, text, scope="area", dest=None):
        f = p / "ai/out/stock" / name
        f.parent.mkdir(parents=True, exist_ok=True)
        fm = f"---\nscope: {scope}\n" + (f"dest: {dest}\n" if dest else "") + "---\n"
        f.write_text(fm + text, encoding="utf-8", newline="\n")

    def test_delivers_by_dest_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "a.md", "# 決定\n理由と経緯\n")
            self.put(p, "b.md", "# 経緯\n", dest="docs")
            room.cmd_stock(c, self.ns())
            self.assertIn("理由と経緯", (v / "areas/area-x/ai/knowledge/a.md").read_text(encoding="utf-8"))
            self.assertTrue((v / "areas/area-x/ai/docs/b.md").exists())
            self.assertEqual(list((p / "ai/out/stock").glob("*.md")), [])  # move: 元は消える
            man = json.loads((p / "ai/records/manifest.json").read_text(encoding="utf-8"))
            self.assertIn("knowledge/a.md", man["area_stock"])  # 元が無くても、運んだ記録は残る
            c.msgs.clear()
            room.cmd_stock(c, self.ns())
            self.assertIn("運ぶ下書きは無い", c.msgs[-1])

    def test_not_delivered_drafts_stay(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "pub.md", "公開向け\n", scope="public")
            self.put(p, "a.md", "v1\n")
            room.cmd_stock(c, self.ns())
            dst = v / "areas/area-x/ai/knowledge/a.md"
            dst.write_text("人が直した\n", encoding="utf-8")
            self.put(p, "a.md", "v2\n")
            room.cmd_stock(c, self.ns())
            self.assertTrue((p / "ai/out/stock/pub.md").exists())  # scope 違いは運ばず残す
            self.assertTrue((p / "ai/out/stock/a.md").exists())  # 衝突で運ばなかったものは残す

    def test_no_prompt_and_table_after_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "a.md", "x\n")
            self.put(p, "b.md", "y\n", dest="docs")
            with mock.patch("builtins.input", side_effect=AssertionError("確認を聞かない")):
                room.cmd_stock(c, self.ns(yes=False))
            self.assertFalse((p / "ai/out/stock/a.md").exists())
            self.assertIn("| a.md | areas/area-x/ai/knowledge/a.md |  |", c.msgs)
            self.assertIn("| b.md | areas/area-x/ai/docs/b.md |  |", c.msgs)

    def test_leftover_already_in_area_is_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "a.md", "x\n")
            src = (p / "ai/out/stock/a.md").read_bytes()
            room.cmd_stock(c, self.ns())
            (p / "ai/out/stock/a.md").write_bytes(src)  # copy 時代に残った元（同じ内容が Area にある）
            room.cmd_stock(c, self.ns())
            self.assertFalse((p / "ai/out/stock/a.md").exists())

    def test_source_kept_when_destination_does_not_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "a.md", "x\n")
            real = Path.write_bytes
            def broken(self_, data):
                return real(self_, data + b"!" if "areas" in str(self_) else data)
            with mock.patch.object(Path, "write_bytes", broken):
                room.cmd_stock(c, self.ns())
            self.assertTrue((p / "ai/out/stock/a.md").exists())
            self.assertTrue(any("元は消していない" in m for m in c.msgs))

    def test_unlink_failure_warns_and_next_run_removes(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "a.md", "x\n")
            with mock.patch.object(Path, "unlink", side_effect=PermissionError("locked")):
                room.cmd_stock(c, self.ns())
            self.assertTrue((p / "ai/out/stock/a.md").exists())
            self.assertTrue((v / "areas/area-x/ai/knowledge/a.md").exists())
            room.cmd_stock(c, self.ns())
            self.assertFalse((p / "ai/out/stock/a.md").exists())

    def test_public_scope_is_not_delivered_to_area(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "pub.md", "公開向け\n", scope="public")
            room.cmd_stock(c, self.ns())
            self.assertFalse((v / "areas/area-x/ai").exists())

    def test_bad_dest_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "a.md", "x\n", dest="../etc")
            with self.assertRaises(room.RoomError):
                room.cmd_stock(c, self.ns())

    def test_sensitive_hit_stops_everything(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "ok.md", "# 決定\n")
            self.put(p, "ng.md", "予算は 1,200,000 円、連絡は a@example.com\n")
            with self.assertRaises(room.RoomError) as e:
                room.cmd_stock(c, self.ns())
            self.assertIn("金額", str(e.exception))
            self.assertFalse((v / "areas/area-x/ai").exists())

    def test_mask_toml_terms_stop(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            (p / "_noai").mkdir(exist_ok=True)
            (p / "_noai/mask.toml").write_text('[terms.CUST]\nnames = ["株式会社テスト"]\n', encoding="utf-8")
            self.put(p, "x.md", "株式会社テストとの経緯\n", dest="docs")
            with self.assertRaises(room.RoomError):
                room.cmd_stock(c, self.ns())

    def test_internal_area_without_terms_delivers_by_shape_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp, boundary="internal")
            self.put(p, "a.md", "x\n")
            room.cmd_stock(c, self.ns())
            self.assertTrue(any((v / "areas/area-x/ai").rglob("a.md")))

    def test_internal_area_delivers_with_terms_and_term_hit_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp, boundary="internal")
            (p / "_noai").mkdir(exist_ok=True)
            (p / "_noai/mask.toml").write_text('[terms.CUST]\nnames = ["株式会社テスト"]\n', encoding="utf-8")
            self.put(p, "ok.md", "# 決定\n")
            room.cmd_stock(c, self.ns())
            self.assertTrue((v / "areas/area-x/ai/knowledge/ok.md").exists())
            self.put(p, "ng.md", "株式会社テストの件\n")
            with self.assertRaises(room.RoomError):
                room.cmd_stock(c, self.ns())

    def test_human_edited_destination_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "a.md", "v1\n")
            room.cmd_stock(c, self.ns())
            dst = v / "areas/area-x/ai/knowledge/a.md"
            dst.write_text("人が直した\n", encoding="utf-8")
            self.put(p, "a.md", "v2\n")
            room.cmd_stock(c, self.ns())
            self.assertEqual(dst.read_text(encoding="utf-8"), "人が直した\n")

    def test_updates_when_destination_is_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            self.put(p, "a.md", "v1\n")
            room.cmd_stock(c, self.ns())
            self.put(p, "a.md", "v2\n")
            room.cmd_stock(c, self.ns())
            self.assertIn("v2", (v / "areas/area-x/ai/knowledge/a.md").read_text(encoding="utf-8"))

    def test_kit_skips_scope_area(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self.setup(tmp)
            (v / "resources/exmem/inbox").mkdir(parents=True)
            self.put(p, "a.md", "x\n")
            room.cmd_stock(c, self.ns(dst="kit"))
            self.assertEqual(list((v / "resources/exmem/inbox").glob("*.md")), [])


class AreaAiSnapshotTest(unittest.TestCase):
    def setup(self, tmp, boundary="external"):
        v, c = opened(tmp)
        ar = v / "areas/area-x/README.md"
        ar.write_text(ar.read_text(encoding="utf-8").replace("boundary: internal", f"boundary: {boundary}"), encoding="utf-8", newline="\n")
        base = v / "areas/area-x/ai"
        (base / "knowledge").mkdir(parents=True)
        (base / "docs").mkdir(parents=True)
        return v, c, room.Project.load(c, "proj-a"), base

    def test_copies_knowledge_and_docs_read_only_and_skips_inbox_and_hits(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, base = self.setup(tmp)
            (base / "knowledge/k.md").write_text("知識\n", encoding="utf-8")
            (base / "docs/decisions.md").write_text("決定\n", encoding="utf-8")
            (base / "docs/inbox.md").write_text("仮置き\n", encoding="utf-8")
            (base / "docs/leak.md").write_text("連絡は a@example.com\n", encoding="utf-8")
            n = room.snapshot_area_ai(c, p)
            self.assertEqual(n, 2)
            out = p.ai / "ctx/area"
            self.assertTrue((out / "knowledge/k.md").exists())
            self.assertTrue((out / "docs/decisions.md").exists())
            self.assertFalse((out / "docs/inbox.md").exists())
            self.assertFalse((out / "docs/leak.md").exists())
            self.assertFalse(os.access(out / "knowledge/k.md", os.W_OK) and os.geteuid() != 0)

    def test_internal_area_without_terms_still_copies(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, base = self.setup(tmp, boundary="internal")
            (base / "knowledge/k.md").write_text("知識\n", encoding="utf-8")
            self.assertEqual(room.snapshot_area_ai(c, p), 1)

    def test_internal_area_with_terms_copies_and_skips_term_hits(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, base = self.setup(tmp, boundary="internal")
            (p.dir / "_noai").mkdir(exist_ok=True)
            (p.dir / "_noai/mask.toml").write_text('[terms.CUST]\nnames = ["株式会社テスト"]\n', encoding="utf-8")
            (base / "knowledge/k.md").write_text("知識\n", encoding="utf-8")
            (base / "knowledge/leak.md").write_text("株式会社テストの件\n", encoding="utf-8")
            self.assertEqual(room.snapshot_area_ai(c, p), 1)

    def test_size_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p, base = self.setup(tmp)
            (base / "knowledge/a.md").write_text("あ" * 200000, encoding="utf-8")
            (base / "knowledge/b.md").write_text("い" * 200000, encoding="utf-8")
            self.assertEqual(room.snapshot_area_ai(c, p), 1)


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
        d = dict(name="proj-a", yes=True, dst="kit")
        d.update(kw)
        return argparse.Namespace(**d)

    def test_dst_is_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, r, base = self.setup(tmp)
            p = v / "projects/proj-a"
            (p / "ai/out/stock").mkdir(parents=True)
            (p / "ai/out/stock/nos.md").write_text("---\ntitle: x\n---\nx\n", encoding="utf-8")
            with self.assertRaises(room.RoomError):  # scope: が無い下書きがあれば、何も運ばず止まる
                room.cmd_stock(c, self.ns(dst=None))
            self.assertTrue((p / "ai/out/stock/nos.md").exists())

    def test_omitted_dst_follows_scope_and_never_commits(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, r, base = self.setup(tmp)
            p = v / "projects/proj-a"
            (p / "ai/out/stock").mkdir(parents=True)
            pub = self.DRAFT.format(base=base).replace("type: inbox\n", "type: inbox\nscope: public\n")
            (p / "ai/out/stock/2026-10-12-topic-a.md").write_text(pub, encoding="utf-8")
            (p / "ai/out/stock/area-note.md").write_text("---\nscope: area\n---\n# 決定\n", encoding="utf-8")
            head = subprocess.run(["git", "-C", str(r), "rev-parse", "HEAD"], capture_output=True, text=True).stdout
            room.cmd_stock(c, self.ns(dst=None))
            self.assertEqual(len(list((r / "exmem/inbox").glob("*.md"))), 1)
            self.assertTrue((v / "areas/area-x/ai/knowledge/area-note.md").exists())
            self.assertEqual(list((p / "ai/out/stock").glob("*.md")), [])
            self.assertEqual(head, subprocess.run(["git", "-C", str(r), "rev-parse", "HEAD"], capture_output=True, text=True).stdout)

    def test_delivers_without_stale_mark_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, r, base = self.setup(tmp)
            p = v / "projects/proj-a"
            (p / "ai/out/stock").mkdir(parents=True)
            (p / "ai/out/stock/2026-10-12-topic-a.md").write_text(self.DRAFT.format(base=base), encoding="utf-8")
            room.cmd_stock(c, self.ns())
            got = (r / "exmem/inbox/2026-10-12-topic-a.md").read_text(encoding="utf-8")
            self.assertNotIn("base_stale", got)
            self.assertFalse((p / "ai/out/stock/2026-10-12-topic-a.md").exists())  # move: 元は消える
            room.cmd_stock(c, self.ns())
            self.assertEqual(len(list((r / "exmem/inbox").glob("*.md"))), 1)
            # copy 時代に残った元（同じ内容を運んだ記録がある）は、運び直さずに消す
            (p / "ai/out/stock/2026-10-12-topic-a.md").write_text(self.DRAFT.format(base=base), encoding="utf-8")
            room.cmd_stock(c, self.ns())
            self.assertEqual(len(list((r / "exmem/inbox").glob("*.md"))), 1)
            self.assertFalse((p / "ai/out/stock/2026-10-12-topic-a.md").exists())

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

    def test_scope_area_is_not_delivered(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, r, base = self.setup(tmp)
            p = v / "projects/proj-a"
            (p / "ai/out/stock").mkdir(parents=True)
            draft = self.DRAFT.format(base=base).replace("type: inbox\n", "type: inbox\nscope: area\n")
            (p / "ai/out/stock/2026-10-12-topic-a.md").write_text(draft, encoding="utf-8")
            room.cmd_stock(c, self.ns())
            self.assertEqual(list((r / "exmem/inbox").glob("*.md")), [])

    def test_refuses_missing_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, r, base = self.setup(tmp)
            p = v / "projects/proj-a"
            (p / "ai/out/stock").mkdir(parents=True)
            (p / "ai/out/stock/no-header.md").write_text("---\ntype: inbox\ntitle: x\n---\nx\n", encoding="utf-8")
            room.cmd_stock(c, self.ns())
            self.assertEqual(list((r / "exmem/inbox").glob("*.md")), [])
            self.assertTrue((p / "ai/out/stock/no-header.md").exists())  # 運ばなかったものは残る


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


def tty(answer=None):
    """close の y/N を、端末からの実行として答える（answer が None なら非対話）。"""
    stdin = mock.MagicMock()
    stdin.isatty.return_value = answer is not None
    patches = [mock.patch.object(room.sys, "stdin", stdin)]
    if answer is not None:
        patches.append(mock.patch("builtins.input", return_value=answer))
    stack = contextlib.ExitStack()
    for pt in patches:
        stack.enter_context(pt)
    return stack


class StockPublicScopeTest(unittest.TestCase):
    def test_room_guide_tells_public_drafts_to_write_scope(self):
        # scope: public が無いと room stock（--dst なし）が宛先不明で止まる（2026-11-05）
        public = next(l for l in room.ROOM_GUIDE.splitlines() if l.startswith("- `public`"))
        rest = room.ROOM_GUIDE.split(public, 1)[1].split("\n- `area`", 1)[0]
        self.assertIn("exmem/inbox/", public)
        self.assertIn("`scope: public`", rest)


class OpenFromTest(unittest.TestCase):
    """room open --from: 閉じた Project の成果物・close.md・正式な計画を、新しい Project の ai/in/from-<P1>/ に写す。"""

    def archived(self, tmp, boundary="internal"):
        v = make_vault(tmp)
        (v / "areas/area-x/README.md").write_text(AREA_README.replace("boundary: internal", f"boundary: {boundary}"), encoding="utf-8", newline="\n")
        a = v / "archives" / "old"
        for d in ("ai/out/tool", "ai/out/stock", "ai/work/plan", "ai/ctx"):
            (a / d).mkdir(parents=True)
        (a / "README.md").write_text("---\nstatus: done\narea: area-x\n---\n\n# old\n", encoding="utf-8", newline="\n")
        (a / "ai/out/tool/main.py").write_text("print(1)\n", encoding="utf-8")
        (a / "ai/out/close.md").write_text("- 【案件】x\n", encoding="utf-8")
        (a / "ai/out/readme-draft.md").write_text("draft\n", encoding="utf-8")
        (a / "ai/out/stock/s.md").write_text("s\n", encoding="utf-8")
        (a / "ai/work/plan/6r.md").write_text("---\nstatus: 正式\napproved: 2026-10-01\n---\n\n6R\n", encoding="utf-8")
        (a / "ai/work/plan/draft.md").write_text("---\nstatus: 仮\n---\n\nd\n", encoding="utf-8")
        (a / "ai/ctx/README.md").write_text("ctx\n", encoding="utf-8")
        return v

    def open_from(self, v, src="old", name="new"):
        c = ctx_for(v)
        room.cmd_open(c, argparse.Namespace(name=name, area="area-x", type="dev", boundary=None, commit=False, from_project=src))
        return c

    def test_copies_outputs_close_and_formal_plan_with_provenance(self):
        for boundary in ("internal", "external"):  # external でも使える（AI の側から AI の側への写し）
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as tmp:
                v = self.archived(tmp, boundary)
                self.open_from(v)
                base = v / "projects/new/ai/in/from-old"
                got = sorted(f.relative_to(base).as_posix() for f in base.rglob("*") if f.is_file())
                self.assertEqual(got, ["out/close.md", "out/tool/main.py", "work/plan/6r.md"])
                p = room.Project.load(ctx_for(v), "new")
                self.assertEqual(room.check_provenance(p), [])
                e = room.load_manifest(p)["files"]["in/from-old/out/tool/main.py"]
                self.assertEqual(e["origin"]["project"], "old")
                self.assertEqual(e["origin"]["path"], "archives/old/ai/out/tool/main.py")
                self.assertIn("from: old", (v / "projects/new/README.md").read_text(encoding="utf-8"))
                self.assertIn("archives/old/README", (v / "areas/area-x/README.md").read_text(encoding="utf-8"))

    def test_copied_files_are_not_a_plan_of_the_new_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = self.archived(tmp)
            c = self.open_from(v)
            p = room.Project.load(c, "new")
            self.assertEqual(room.check_plan_approval(c, p), 0)

    def test_no_plan_still_copies_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:  # 小さな Project は計画が無い（2026-11-05）
            v = self.archived(tmp)
            shutil.rmtree(v / "archives/old/ai/work")
            self.open_from(v)
            base = v / "projects/new/ai/in/from-old"
            got = sorted(f.relative_to(base).as_posix() for f in base.rglob("*") if f.is_file())
            self.assertEqual(got, ["out/close.md", "out/tool/main.py"])

    def test_nothing_to_copy_opens_with_provenance_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = self.archived(tmp)
            shutil.rmtree(v / "archives/old/ai/out")
            shutil.rmtree(v / "archives/old/ai/work")
            c = self.open_from(v)
            self.assertTrue(any("写すものが無い" in m for m in c.msgs))
            self.assertFalse((v / "projects/new/ai/in/from-old").exists())
            self.assertIn("from: old", (v / "projects/new/README.md").read_text(encoding="utf-8"))
            self.assertIn("archives/old/README", (v / "areas/area-x/README.md").read_text(encoding="utf-8"))

    def test_refuses_and_creates_nothing(self):
        cases = {
            "not archived": lambda v: shutil.rmtree(v / "archives/old"),
            "not done": lambda v: (v / "archives/old/README.md").write_text("---\nstatus: active\narea: area-x\n---\n", encoding="utf-8"),
            "other area": lambda v: (v / "archives/old/README.md").write_text("---\nstatus: done\narea: area-y\n---\n", encoding="utf-8"),
        }
        for label, mutate in cases.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as tmp:
                v = self.archived(tmp)
                mutate(v)
                with self.assertRaises(room.RoomError):
                    self.open_from(v)
                self.assertFalse((v / "projects/new").exists())


class CloseAreaTest(unittest.TestCase):
    def args(self, area="area-x", commit=False):
        return argparse.Namespace(name=None, area=area, commit=commit)

    def empty_area(self, tmp):
        v = make_vault(tmp)
        (v / "areas/area-x/ai").mkdir()
        (v / "areas/area-x/ai/k.md").write_text("知識\n", encoding="utf-8")
        (v / "areas/area-x/_noai").mkdir()
        (v / "areas/area-x/_noai/s.txt").write_text("追跡外\n", encoding="utf-8")
        return v, ctx_for(v, FakeWsl())

    def test_moves_area_to_archives_on_y(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = self.empty_area(tmp)
            with tty("y"):
                room.cmd_close(c, self.args(commit=True))
            self.assertFalse((v / "areas/area-x").exists())
            d = v / "archives/areas/area-x"
            self.assertTrue((d / "ai/k.md").exists())
            self.assertTrue((d / "_noai/s.txt").exists())
            self.assertIn("status: closed", (d / "README.md").read_text(encoding="utf-8"))

    def test_n_and_noninteractive_change_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = self.empty_area(tmp)
            with tty("n"), self.assertRaisesRegex(room.RoomError, "中止"):
                room.cmd_close(c, self.args())
            with tty(), self.assertRaisesRegex(room.RoomError, "非対話"):
                room.cmd_close(c, self.args())
            self.assertTrue((v / "areas/area-x/README.md").exists())

    def test_stops_with_active_project_or_pending_area_stock(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            with tty("y"), self.assertRaisesRegex(room.RoomError, "進行中の Project がある: proj-a"):
                room.cmd_close(c, self.args())
            (v / "projects/proj-a").rename(v / "archives/proj-a")
            s = v / "archives/proj-a/ai/out/stock"
            s.mkdir(parents=True)
            (s / "d.md").write_text("---\nscope: area\n---\nx\n", encoding="utf-8")
            with tty("y"), self.assertRaisesRegex(room.RoomError, "scope: area が未処理"):
                room.cmd_close(c, self.args())
            (s / "d.md").unlink()
            with tty("y"):
                room.cmd_close(c, self.args())
            self.assertTrue((v / "archives/areas/area-x/README.md").exists())


class RmTest(unittest.TestCase):
    def args(self, names=(), area=None, yes=True, commit=False):
        return argparse.Namespace(names=list(names), area=area, yes=yes, commit=commit)

    def test_rm_project_removes_dir_area_entry_and_room_traces(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            readme = v / "areas/area-x/README.md"
            self.assertIn("projects/proj-a/README", readme.read_text(encoding="utf-8"))
            room.cmd_rm(c, self.args(["proj-a"], commit=True))
            self.assertFalse((v / "projects/proj-a").exists())
            self.assertNotIn("proj-a", readme.read_text(encoding="utf-8"))
            self.assertTrue(any("rm -rf" in s[1] and "-mnt-room-proj-a" in s[1] for s in wsl.scripts))
            self.assertEqual(subprocess.run(["git", "-C", str(v), "status", "--porcelain"], capture_output=True, text=True).stdout.strip(), "")

    def test_rm_archived_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            (v / "projects/proj-a").rename(v / "archives/proj-a")
            room.cmd_rm(c, self.args(["proj-a"]))
            self.assertFalse((v / "archives/proj-a").exists())

    def test_rm_without_distro_still_removes(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            c.wsl._distros.clear()
            room.cmd_rm(c, self.args(["proj-a"]))
            self.assertFalse((v / "projects/proj-a").exists())

    def test_stops_when_mounted_unknown_or_noninteractive_and_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            wsl.mounted = True
            with self.assertRaisesRegex(room.RoomError, "マウントが残っている"):
                room.cmd_rm(c, self.args(["proj-a"]))
            wsl.mounted = False
            with self.assertRaisesRegex(room.RoomError, "Project が無い"):
                room.cmd_rm(c, self.args(["nope"]))
            with tty(), self.assertRaisesRegex(room.RoomError, "非対話"):
                room.cmd_rm(c, self.args(["proj-a"], yes=False))
            with tty("n"), self.assertRaisesRegex(room.RoomError, "中止"):
                room.cmd_rm(c, self.args(["proj-a"], yes=False))
            self.assertTrue((v / "projects/proj-a/README.md").exists())

    def test_rm_area_stops_while_projects_remain_then_removes(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            with self.assertRaisesRegex(room.RoomError, "Project が残っている"):
                room.cmd_rm(c, self.args(area="area-x"))
            room.cmd_rm(c, self.args(["proj-a"]))
            room.cmd_rm(c, self.args(area="area-x", commit=True))
            self.assertFalse((v / "areas/area-x").exists())
            self.assertTrue(any("wsl --unregister room-area-x" in m for m in c.msgs))

    def test_rm_rejects_area_with_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            with self.assertRaisesRegex(room.RoomError, "同時"):
                room.cmd_rm(c, self.args(["proj-a"], area="area-x"))
            with self.assertRaisesRegex(room.RoomError, "指定する"):
                room.cmd_rm(c, self.args())


class CloseTest(unittest.TestCase):
    def test_close_warns_and_proceeds_on_y_with_template_readme_and_no_close_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            room.scaffold_area(c, "area-x")
            with tty("y"):
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            self.assertFalse((v / "projects/proj-a").exists())
            self.assertTrue((v / "archives/proj-a/README.md").exists())
            self.assertIn("status: done", (v / "archives/proj-a/README.md").read_text(encoding="utf-8"))

    def test_close_warning_n_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            room.scaffold_area(c, "area-x")
            with tty("n"), self.assertRaisesRegex(room.RoomError, "中止"):
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            self.assertTrue((v / "projects/proj-a").exists())

    def test_close_refuses_template_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            p = v / "projects/proj-a"
            (p / "ai/out/close.md").write_text("- 【案件】x\n", encoding="utf-8")
            with tty(), self.assertRaisesRegex(room.RoomError, "非対話.*\n.*ひな形のまま"):
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            self.assertTrue(p.exists())

    def test_close_requires_close_md_and_unmounted(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            fill_readme(v / "projects/proj-a")
            with tty(), self.assertRaisesRegex(room.RoomError, "close.md が無い"):
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            (v / "projects/proj-a/ai/out/close.md").write_text("- 【案件】x\n", encoding="utf-8")
            wsl.mounted = True
            with self.assertRaises(room.RoomError):
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))

    def test_close_warns_on_stray_out_folder_and_n_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            p = v / "projects/proj-a"
            fill_readme(p)
            (p / "ai/out/close.md").write_text("- 【案件】x\n", encoding="utf-8")
            (p / "ai/out/stock").mkdir()
            (p / "ai/out/proj-a").mkdir()
            (p / "ai/out/final-report").mkdir()
            with tty("n"), self.assertRaisesRegex(room.RoomError, "中止"):
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            self.assertTrue(p.exists())
            self.assertEqual(room.stray_out_dirs(room.Project.load(c, "proj-a")), ["final-report"])

    def test_close_no_stray_warning_for_project_name_stock_and_deliverable(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp, FakeWsl())
            p = v / "projects/proj-a"
            fill_readme(p)
            (p / "ai/out/close.md").write_text("- 【案件】x\n", encoding="utf-8")
            for d in ("stock", "proj-a", "deliverable"):
                (p / "ai/out" / d).mkdir()
            self.assertEqual(room.stray_out_dirs(room.Project.load(c, "proj-a")), [])

    def test_close_moves_to_archives_and_hands_over(self):
        with tempfile.TemporaryDirectory() as tmp:
            wsl = FakeWsl()
            v, c = opened(tmp, wsl)
            p = v / "projects/proj-a"
            fill_readme(p)
            room.scaffold_area(c, "area-x")
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
            self.assertFalse((v / "areas/area-x/ai/docs/inbox.md").exists(), "close は Area の inbox を作らない・足さない")
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

    def _decision_project(self, tmp, close_text):
        v, c = opened(tmp, FakeWsl())
        p = v / "projects/proj-a"
        fill_readme(p)
        room.scaffold_area(c, "area-x")
        (p / "ai/docs").mkdir(parents=True, exist_ok=True)
        (p / "ai/docs/decisions.md").write_text("# decisions\n\n## 列は固定にする\n理由A\n\n## 別の項\n理由B\n", encoding="utf-8")
        (p / "ai/out/close.md").write_text(close_text, encoding="utf-8")
        return v, c, p

    def test_close_delivers_deliverable_to_area_without_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self._decision_project(tmp, "- 【案件】x\n")
            (p / "ai/out/deliverable").mkdir(parents=True)
            (p / "ai/out/deliverable/report.md").write_text("報告\n", encoding="utf-8", newline="\n")
            room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            self.assertEqual((v / "areas/area-x/_noai/deliverable/proj-a/report.md").read_text(encoding="utf-8"), "報告\n")
            self.assertTrue((v / "archives/proj-a").is_dir())

    def test_close_delivers_out_project_name_dir_as_is_under_project_name(self):
        with tempfile.TemporaryDirectory() as tmp:  # 成果物の塊は ai/out/<Project 名>/。Area では <Project 名>/ の直下に置く（2026-11-05）
            v, c, p = self._decision_project(tmp, "- 【案件】x\n")
            (p / "ai/out/proj-a/sub").mkdir(parents=True)
            (p / "ai/out/proj-a/report.md").write_text("報告\n", encoding="utf-8", newline="\n")
            (p / "ai/out/proj-a/sub/x.md").write_text("x\n", encoding="utf-8", newline="\n")
            (p / "ai/out/other.md").write_text("対象外\n", encoding="utf-8", newline="\n")
            room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            base = v / "areas/area-x/_noai/deliverable/proj-a"
            self.assertEqual((base / "report.md").read_text(encoding="utf-8"), "報告\n")
            self.assertTrue((base / "sub/x.md").exists())
            self.assertFalse((base / "other.md").exists())
            self.assertFalse((base / "proj-a").exists())

    def test_close_stops_before_any_change_when_area_deliverable_was_edited(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self._decision_project(tmp, "- 【案件】x\n")
            dst = v / "areas/area-x/_noai/deliverable/proj-a"
            dst.mkdir(parents=True)
            (dst / "report.md").write_text("人が書いた\n", encoding="utf-8", newline="\n")
            (p / "ai/out/deliverable").mkdir(parents=True)
            (p / "ai/out/deliverable/report.md").write_text("報告\n", encoding="utf-8", newline="\n")
            with self.assertRaisesRegex(room.RoomError, "Area に渡せない"):
                room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            self.assertTrue(p.exists())
            self.assertEqual((dst / "report.md").read_text(encoding="utf-8"), "人が書いた\n")

    def test_close_does_not_write_area_inbox_and_trace_searches_archives(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c, p = self._decision_project(tmp, "- 【案件】x\n- 【決定】列を固定する（根拠: 列は固定）\n")
            room.cmd_close(c, argparse.Namespace(name="proj-a", commit=False))
            self.assertFalse((v / "areas/area-x/ai/docs/inbox.md").exists())
            c.msgs.clear()
            room.cmd_trace(c, argparse.Namespace(area="area-x", word="理由A"))
            out = "\n".join(c.msgs)
            self.assertIn("archives/proj-a/ai/docs/decisions.md", out)
            self.assertIn("理由A", out)
            self.assertNotIn("理由B", out)
            with self.assertRaisesRegex(room.RoomError, "節が無い"):
                room.cmd_trace(c, argparse.Namespace(area="area-x", word="存在しない語zzz"))
            with self.assertRaisesRegex(room.RoomError, "Area が無い"):
                room.cmd_trace(c, argparse.Namespace(area="area-none", word="x"))

    def test_init_scaffolds_area_dirs_without_inbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            room.cmd_init(ctx_for(v, FakeWsl(distros=())), argparse.Namespace(area="area-y", resume=False, boundary="internal", commit=False))
            self.assertFalse((v / "areas/area-y/_noai/knowledge").exists())
            self.assertTrue((v / "areas/area-y/_noai/source").is_dir())
            self.assertTrue((v / "areas/area-y/_noai/deliverable").is_dir())
            self.assertFalse((v / "areas/area-y/ai/docs/inbox.md").exists())

    def test_scaffold_warns_about_old_knowledge_dir_and_does_not_move_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            old = v / "areas/area-x/knowledge"
            old.mkdir()
            (old / "a.md").write_text("x\n", encoding="utf-8")
            c = ctx_for(v, FakeWsl())
            room.scaffold_area(c, "area-x")
            self.assertTrue(any("knowledge/ がある" in m for m in c.msgs))
            self.assertTrue((old / "a.md").exists())
            self.assertFalse((v / "areas/area-x/_noai/knowledge").exists())

    def test_init_scaffolds_existing_area_even_when_room_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_vault(tmp)
            with self.assertRaises(room.RoomError):
                room.cmd_init(ctx_for(v, FakeWsl()), argparse.Namespace(area="area-x", resume=False))
            self.assertFalse((v / "areas/area-x/_noai/knowledge").exists())


class RoomGitWrapperTest(unittest.TestCase):
    """/usr/local/bin/git のラッパーを、/mnt/room と /usr/bin/git を一時ディレクトリの偽物に差し替えて sh で動かす。"""

    def setUp(self):
        self.sh = shutil.which("sh")
        if not self.sh:
            self.skipTest("sh が無い")
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = self.posix(tmp.name)
        self.root, self.src, self.home = f"{base}/room", f"{base}/src/repo", f"{base}/home"
        for d in ("room/proj-a/sub", "room/proj-b", "src/repo", "home", "bin"):
            os.makedirs(os.path.join(tmp.name, d))
        fake = os.path.join(tmp.name, "bin", "fakegit")
        Path(fake).write_text('#!/bin/sh\necho "GIT_DIR=${GIT_DIR-unset} GIT_WORK_TREE=${GIT_WORK_TREE-unset}"\n', encoding="utf-8", newline="\n")
        os.chmod(fake, 0o755)
        self.wrapper = os.path.join(tmp.name, "bin", "git")
        text = room.ROOM_GIT_WRAPPER.replace("/mnt/room", self.root).replace("/usr/bin/git", f"{base}/bin/fakegit")
        Path(self.wrapper).write_text(text, encoding="utf-8", newline="\n")

    def posix(self, path):
        return subprocess.run([self.sh, "-c", 'cd "$1" && pwd', "_", path], capture_output=True, text=True, check=True).stdout.strip()

    def run_git(self, cwd, *args, env=None):
        e = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE")}
        e.update(HOME=self.home, **(env or {}))
        r = subprocess.run([self.sh, "-c", 'cd "$1" && shift && exec sh "$@"', "_", cwd, self.wrapper, *args], env=e, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout.strip()

    def room_of(self, name):
        return f"GIT_DIR={self.home}/gitdirs/{name} GIT_WORK_TREE={self.root}/{name}"

    def test_room_git_follows_the_git_target(self):
        unset = "GIT_DIR=unset GIT_WORK_TREE=unset"
        a = f"{self.root}/proj-a"
        cases = [
            (a, ["status"], self.room_of("proj-a")),
            (f"{a}/sub", ["log"], self.room_of("proj-a")),
            (a, ["-c", "a=b", "status"], self.room_of("proj-a")),
            (a, ["-C", "sub", "status"], self.room_of("proj-a")),
            (a, ["-C", "../proj-b", "status"], self.room_of("proj-b")),
            (self.src, ["-C", a, "status"], self.room_of("proj-a")),
            (a, ["-C", self.src, "log"], unset),
            (a, ["-C", self.src, "-C", a, "log"], self.room_of("proj-a")),
            (a, ["-C", f"{a}/nothing", "log"], unset),
            (a, ["-C"], self.room_of("proj-a")),
            (a, ["clone", "url", "x"], unset),
            (a, ["--git-dir=x", "status"], unset),
            (a, ["--work-tree", "x", "status"], unset),
            (self.root, ["status"], unset),
            (self.src, ["status"], unset),
        ]
        for cwd, args, want in cases:
            with self.subTest(cwd=cwd.replace(self.root, "ROOM").replace(self.src, "SRC"), args=args):
                self.assertEqual(self.run_git(cwd, *args), want)

    def test_preset_git_dir_is_kept(self):
        self.assertEqual(self.run_git(f"{self.root}/proj-a", "status", env={"GIT_DIR": "/x"}), "GIT_DIR=/x GIT_WORK_TREE=unset")


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
            for rel in ("room/README.md", "room/room.py", "room/pyproject.toml", "room/tests/test_x.py"):
                (kit / rel).write_text("x", encoding="utf-8")
            with tarfile.open(fileobj=io.BytesIO(__import__("gzip").decompress(room.build_share_tar(root))), mode="r") as tf:
                names = set(tf.getnames())
        self.assertIn("workflow-kit/hooks.md", names)
        self.assertIn("workflow-kit/room/README.md", names)
        self.assertNotIn("workflow-kit/room/room.py", names)
        self.assertNotIn("workflow-kit/room/pyproject.toml", names)
        self.assertNotIn("workflow-kit/room/tests", names)
        self.assertNotIn("workflow-kit/room/tests/test_x.py", names)


KIT_TEMPLATES = Path(room.__file__).resolve().parent.parent / "templates"
IDENT = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.org", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.org"}


def make_works(tmp, with_resources=True, origin="https://github.com/yuzucha16/workbase.git"):
    """mkworks 用: 空の works に、雛形を持つ resources/（git）を置く。"""
    v = Path(tmp) / "works"
    v.mkdir()
    if with_resources:
        res = v / "resources"
        shutil.copytree(KIT_TEMPLATES, res / "workflow-kit" / "templates")
        sh(res, "init", "-q", "-b", "main")
        sh(res, "remote", "add", "origin", origin)
        sh(res, "add", "-A")
        sh(res, "-c", "user.name=t", "-c", "user.email=t@example.org", "commit", "-qm", "kit")
    return v


def kit_commit(v, rel, text):
    res = v / "resources"
    f = res / "workflow-kit" / "templates" / "workspace" / rel
    f.write_text(text, encoding="utf-8", newline="\n")
    sh(res, "add", "-A")
    sh(res, "-c", "user.name=t", "-c", "user.email=t@example.org", "commit", "-qm", f"kit {rel}")


def mkw_args(**kw):
    d = dict(update=False, role="業務用", remote="none", base=None, yes=True, commit=True)
    d.update(kw)
    return argparse.Namespace(**d)


def last_commit(v):
    return subprocess.run(["git", "-C", str(v), "log", "-1", "--format=%B"], capture_output=True, text=True, encoding="utf-8").stdout


class MkworksTest(unittest.TestCase):
    def setUp(self):
        self._old = {k: os.environ.get(k) for k in IDENT}
        os.environ.update(IDENT)

    def tearDown(self):
        for k, val in self._old.items():
            if val is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = val

    def create(self, tmp, **kw):
        v = make_works(tmp)
        c = ctx_for(v)
        room.cmd_mkworks(c, mkw_args(**kw))
        return v, c

    def test_create_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, _c = self.create(tmp)
            for rel in (".gitignore", ".ignore", ".gitattributes", ".claude/settings.json", "README.md", "AGENTS.md", "CLAUDE.md",
                        "docs/log.md", "docs/decisions.md", "areas/.gitkeep", "projects/.gitkeep", "archives/.gitkeep", ".git/hooks/pre-push"):
                self.assertTrue((v / rel).exists(), rel)
            self.assertTrue((v / "resources_p").is_dir())
            agents = (v / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("業務用 PC の作業場", agents)
            self.assertNotIn("<この works", agents)
            self.assertNotIn("<remote の方針", agents)
            self.assertIn("remote: なし", agents)
            self.assertNotIn("<決めたこと>", (v / "docs" / "decisions.md").read_text(encoding="utf-8"))
            self.assertEqual("@AGENTS.md\n", (v / "CLAUDE.md").read_text(encoding="utf-8"))
            tracked = subprocess.run(["git", "-C", str(v), "ls-files"], capture_output=True, text=True).stdout.splitlines()
            self.assertFalse([t for t in tracked if t.startswith("resources")], tracked)
            msg = last_commit(v)
            self.assertIn("[works] initial commit", msg)
            self.assertIn("Room-Op: mkworks", msg)
            self.assertIn("Room-Rev: ", msg)
            self.assertNotIn("Agent:", msg)

    def test_create_with_remote_has_no_prepush(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = self.create(tmp, remote="https://example.org/me/works.git", role="個人用")
            self.assertFalse((v / ".git" / "hooks" / "pre-push").exists())
            self.assertIn("個人用 PC", (v / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertIn("origin", subprocess.run(["git", "-C", str(v), "remote"], capture_output=True, text=True).stdout)
            self.assertTrue(any("push は人が行う" in m for m in c.msgs))

    def test_existing_file_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_works(tmp)
            (v / "README.md").write_text("mine\n", encoding="utf-8")
            room.cmd_mkworks(ctx_for(v), mkw_args())
            self.assertEqual("mine\n", (v / "README.md").read_text(encoding="utf-8"))

    def test_existing_work_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, _c = self.create(tmp)
            with self.assertRaises(room.RoomError):
                room.cmd_mkworks(ctx_for(v), mkw_args())

    def test_resources_must_be_workbase_clone(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_works(tmp, with_resources=False)
            with self.assertRaises(room.RoomError):
                room.cmd_mkworks(ctx_for(v), mkw_args())
        with tempfile.TemporaryDirectory() as tmp:
            v = make_works(tmp, origin="https://example.org/other.git")
            with self.assertRaises(room.RoomError):
                room.cmd_mkworks(ctx_for(v), mkw_args())

    def test_update_merges_and_keeps_local_fill(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, _c = self.create(tmp)
            kit_commit(v, "gitignore.template", (KIT_TEMPLATES / "workspace" / "gitignore.template").read_text(encoding="utf-8") + "\n*.bak\n")
            c = ctx_for(v)
            room.cmd_mkworks(c, mkw_args(update=True))
            self.assertIn("*.bak", (v / ".gitignore").read_text(encoding="utf-8"))
            self.assertIn("業務用 PC の作業場", (v / "AGENTS.md").read_text(encoding="utf-8"))
            msg = last_commit(v)
            self.assertIn("Room-Op: mkworks-update", msg)
            self.assertIn("Room-Rev: " + room.resources_rev(c), msg)

    def test_sub_numbers_from_one_next_to_works(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_works(tmp)
            for n in (1, 2):
                c = ctx_for(v)
                room.cmd_mkworks(c, mkw_args(sub=True, role=None))
                sub = Path(tmp) / f"works_sub{n}"
                self.assertTrue((sub / "AGENTS.md").exists(), sub)
                self.assertTrue((sub / ".git" / "hooks" / "pre-push").exists())
                self.assertIn("個人用 PC", (sub / "AGENTS.md").read_text(encoding="utf-8"))
                origin = subprocess.run(["git", "-C", str(sub / "resources"), "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
                self.assertIn("workbase", origin)
                self.assertIn("Room-Op: mkworks", last_commit(sub))
            self.assertFalse((v / "AGENTS.md").exists())  # 本物の works には触らない
            self.assertFalse((Path(tmp) / "works_sub3").exists())

    def test_sub_rev_then_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_works(tmp)
            old = room.resources_rev(ctx_for(v))
            kit_commit(v, "gitignore.template", (KIT_TEMPLATES / "workspace" / "gitignore.template").read_text(encoding="utf-8") + "\n*.bak\n")
            room.cmd_mkworks(ctx_for(v), mkw_args(sub=True, rev=old))
            sub = Path(tmp) / "works_sub1"
            self.assertNotIn("*.bak", (sub / ".gitignore").read_text(encoding="utf-8"))
            sh(sub / "resources", "checkout", "-q", "main")
            room.cmd_mkworks(ctx_for(sub), mkw_args(update=True))
            self.assertIn("*.bak", (sub / ".gitignore").read_text(encoding="utf-8"))

    def test_sub_rejects_update_and_rev_needs_sub(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_works(tmp)
            for kw in (dict(sub=True, update=True), dict(sub=True, remote="git@example:x.git"), dict(rev="HEAD")):
                with self.assertRaises(room.RoomError, msg=kw):
                    room.cmd_mkworks(ctx_for(v), mkw_args(**kw))
            self.assertFalse((Path(tmp) / "works_sub1").exists())

    def test_sub_parses_from_command_line(self):
        a = room.build_parser().parse_args(["mkworks", "--sub", "--rev", "abc"])
        self.assertTrue(a.sub)
        self.assertEqual(a.rev, "abc")
        self.assertIsNone(a.role)  # 既定は cmd_mkworks で決める（--sub は個人用）

    def test_update_nothing_to_do(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, _c = self.create(tmp)
            before = last_commit(v)
            c = ctx_for(v)
            room.cmd_mkworks(c, mkw_args(update=True))
            self.assertEqual(before, last_commit(v))
            self.assertTrue(any("反映するものなし" in m for m in c.msgs))

    def test_update_conflict_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, _c = self.create(tmp)
            tpl = (KIT_TEMPLATES / "workspace" / "gitignore.template").read_text(encoding="utf-8")
            first = next(l for l in tpl.splitlines() if l.startswith("/resources/"))
            kit_commit(v, "gitignore.template", tpl.replace(first, "/resources-new/"))
            local = (v / ".gitignore").read_text(encoding="utf-8").replace(first, "/resources-mine/")
            (v / ".gitignore").write_text(local, encoding="utf-8", newline="\n")
            sh(v, "add", ".gitignore")
            sh(v, "commit", "-qm", "local edit")
            with self.assertRaises(room.RoomError) as cm:
                room.cmd_mkworks(ctx_for(v), mkw_args(update=True))
            self.assertIn(".gitignore", str(cm.exception))
            self.assertEqual(local, (v / ".gitignore").read_text(encoding="utf-8"))

    def test_update_refuses_uncommitted_local_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, _c = self.create(tmp)
            kit_commit(v, "gitignore.template", (KIT_TEMPLATES / "workspace" / "gitignore.template").read_text(encoding="utf-8") + "\n*.bak\n")
            (v / ".gitignore").write_text((v / ".gitignore").read_text(encoding="utf-8") + "# mine\n", encoding="utf-8", newline="\n")
            with self.assertRaises(room.RoomError):
                room.cmd_mkworks(ctx_for(v), mkw_args(update=True))
            self.assertNotIn("*.bak", (v / ".gitignore").read_text(encoding="utf-8"))

    def test_update_adds_deny_and_never_removes(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c0 = self.create(tmp)
            old = json.loads((KIT_TEMPLATES / "workspace" / "claude-settings.template.json").read_text(encoding="utf-8"))
            new = json.loads(json.dumps(old))
            gone = new["permissions"]["deny"].pop(0)
            new["permissions"]["deny"].append("Read(./extra/**)")
            kit_commit(v, "claude-settings.template.json", json.dumps(new, ensure_ascii=False, indent=2) + "\n")
            c = ctx_for(v)
            room.cmd_mkworks(c, mkw_args(update=True))
            deny = json.loads((v / ".claude" / "settings.json").read_text(encoding="utf-8"))["permissions"]["deny"]
            self.assertIn("Read(./extra/**)", deny)
            self.assertIn(gone, deny)
            self.assertTrue(any(gone in m for m in c.msgs))

    def test_update_needs_base_when_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, _c = self.create(tmp, commit=False)
            with self.assertRaises(room.RoomError):
                room.cmd_mkworks(ctx_for(v), mkw_args(update=True))

    def test_update_reads_legacy_template_rev(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = make_works(tmp)
            base = room.resources_rev(ctx_for(v))
            room.cmd_mkworks(ctx_for(v), mkw_args(commit=False))
            sh(v, "add", "-A", "--", ".gitignore", ".ignore", ".gitattributes", "README.md", "AGENTS.md", "CLAUDE.md", "docs")
            sh(v, "commit", "-qm", "init", "--trailer", f"Template-Rev: {base}")
            self.assertEqual((base, "Template-Rev"), room.mkworks_base(ctx_for(v)))


class CleanTest(unittest.TestCase):
    def test_clean_writes_strict_output_pending_and_adopt_passes(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import dummy_fixture
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            p = v / "projects/proj-a"
            ar = v / "areas/area-x/README.md"
            self.assertIn("boundary: internal", ar.read_text(encoding="utf-8"))
            raw = p / "_noai/raw/area/dummy.xlsx"
            raw.parent.mkdir(parents=True, exist_ok=True)
            raw.write_bytes(dummy_fixture.build_xlsx())
            room.cmd_clean(c, argparse.Namespace(name="proj-a"))
            self.assertTrue((p / "ai/in/area/dummy.xlsx").exists())
            self.assertTrue((p / "_noai/raw/tmp/area/dummy.xlsx-report.md").exists())
            man = room.load_manifest(room.Project.load(c, "proj-a"))
            self.assertTrue(man["files"]["in/area/dummy.xlsx"]["pending"])
            self.assertTrue(room.check_provenance(room.Project.load(c, "proj-a")))
            room.adopt_in(c, room.Project.load(c, "proj-a"))
            self.assertEqual(room.check_provenance(room.Project.load(c, "proj-a")), [])
            room.cmd_clean(c, argparse.Namespace(name="proj-a"))  # 変更が無ければ作り直さない

    def test_clean_path_reads_source_directly_keeping_relative_name(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import dummy_fixture
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            p = v / "projects/proj-a"
            src = v / "areas/area-x/_noai/source/顧客共通/一覧.xlsx"
            src.parent.mkdir(parents=True, exist_ok=True)
            src.write_bytes(dummy_fixture.build_xlsx())
            room.cmd_clean(c, argparse.Namespace(name="proj-a", path=["顧客共通/*.xlsx"], yes=True))
            self.assertTrue((p / "ai/in/area/顧客共通/一覧.xlsx").exists())
            self.assertFalse((p / "_noai/raw/area").exists())  # raw に写さない
            self.assertTrue((v / "areas/area-x/_noai/source/tmp/顧客共通/一覧.xlsx-report.md").exists())  # 報告は原本の隣
            self.assertFalse((p / "_noai/raw/tmp").exists())
            man = room.load_manifest(room.Project.load(c, "proj-a"))
            e = man["files"]["in/area/顧客共通/一覧.xlsx"]
            self.assertTrue(e["pending"])
            self.assertEqual(e["masked_from"], "areas/area-x/_noai/source/顧客共通/一覧.xlsx")

    def test_clean_path_stops_on_sensitive_file_name(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import dummy_fixture
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            src = v / "areas/area-x/_noai/source/taro@example.com.xlsx"
            src.parent.mkdir(parents=True, exist_ok=True)
            src.write_bytes(dummy_fixture.build_xlsx())
            with self.assertRaises(room.RoomError):
                room.cmd_clean(c, argparse.Namespace(name="proj-a", path=["*.xlsx"], yes=True))
            self.assertFalse((v / "projects/proj-a/ai/in/area").exists())

    def test_clean_refuses_external_area(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = opened(tmp)
            ar = v / "areas/area-x/README.md"
            ar.write_text(ar.read_text(encoding="utf-8").replace("boundary: internal", "boundary: external"), encoding="utf-8", newline="\n")
            raw = v / "projects/proj-a/_noai/raw/area/a.xlsx"
            raw.parent.mkdir(parents=True, exist_ok=True)
            raw.write_bytes(b"x")
            with self.assertRaises(room.RoomError):
                room.cmd_clean(c, argparse.Namespace(name="proj-a"))


class DummyProjectTest(unittest.TestCase):
    """myinv*・mydev* はダミー Project。git 追跡の対象外で、Area の一覧とコミットに触れない（WSL は本物と同じ）。"""
    IGNORE = GITIGNORE + "/projects/myinv*/\n/projects/mydev*/\n/archives/myinv*/\n/archives/mydev*/\n"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.v = make_vault(self.tmp.name, self.IGNORE)
        self.c = ctx_for(self.v, FakeWsl())
        self.readme = self.v / "areas/area-x/README.md"
        self.readme_before = self.readme.read_text(encoding="utf-8")
        self.head = self.log()

    def log(self):
        return subprocess.run(["git", "-C", str(self.v), "log", "--oneline"], capture_output=True, text=True, encoding="utf-8").stdout

    def status(self):
        return subprocess.run(["git", "-C", str(self.v), "status", "--porcelain"], capture_output=True, text=True, encoding="utf-8").stdout.strip()

    def open(self, name):
        room.cmd_open(self.c, argparse.Namespace(name=name, area="area-x", type="dev", boundary=None, commit=True))

    def test_is_dummy(self):
        for n in ("myinv", "myinv1", "mydev", "mydev_aaa"):
            self.assertTrue(room.is_dummy(n), n)
        for n in ("proj-a", "my-inv", "xmyinv", "", None):
            self.assertFalse(room.is_dummy(n), n)

    def test_open_leaves_commits_area_readme_and_git_status_untouched(self):
        self.open("myinv1")
        self.assertTrue((self.v / "projects/myinv1/README.md").is_file())
        self.assertEqual(self.readme.read_text(encoding="utf-8"), self.readme_before)
        self.assertEqual(self.log(), self.head)
        self.assertEqual(self.status(), "")

    def test_real_project_is_still_committed_and_listed(self):
        self.open("proj-a")
        self.assertIn("projects/proj-a/README", self.readme.read_text(encoding="utf-8"))
        self.assertNotEqual(self.log(), self.head)

    def test_start_does_not_commit(self):
        self.open("mydev_aaa")
        room.cmd_start(self.c, argparse.Namespace(name="mydev_aaa", cmd="claude", no_launch=False, adopt=False, commit=True, yes=False))
        self.assertEqual(self.log(), self.head)
        self.assertEqual(self.status(), "")

    def test_close_moves_to_archives_without_area_readme_or_commit(self):
        self.open("myinv")
        fill_readme(self.v / "projects/myinv")
        (self.v / "projects/myinv/ai/out/close.md").write_text("- 【案件】x\n", encoding="utf-8")
        room.cmd_close(self.c, argparse.Namespace(name="myinv", commit=True))
        self.assertFalse((self.v / "projects/myinv").exists())
        self.assertTrue((self.v / "archives/myinv/README.md").is_file())
        self.assertEqual(self.readme.read_text(encoding="utf-8"), self.readme_before)
        self.assertEqual(self.log(), self.head)
        self.assertEqual(self.status(), "")

    def test_rm_dummy_removes_without_commit_and_mixed_commits_only_real(self):
        self.open("myinv2")
        self.open("proj-a")
        after_open = self.log()
        room.cmd_rm(self.c, argparse.Namespace(names=["myinv2"], area=None, yes=True, commit=True))
        self.assertFalse((self.v / "projects/myinv2").exists())
        self.assertEqual(self.log(), after_open)
        self.open("mydev3")
        room.cmd_rm(self.c, argparse.Namespace(names=["mydev3", "proj-a"], area=None, yes=True, commit=True))
        self.assertFalse((self.v / "projects/proj-a").exists())
        self.assertNotEqual(self.log(), after_open)
        self.assertEqual(self.status(), "")


if __name__ == "__main__":
    unittest.main()
