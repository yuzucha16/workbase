"""room: AI 作業部屋の操作（open / start / close / umount / mask / restore / readme / stock）。

人が Windows で実行する。AI には実行させない（原本と対応表を読む工程を含むため）。
設計は guides/explain/ai-room-why.md、手作業の手順は guides/howto/ai-room-setup.md。
標準ライブラリだけで動く。起動は `uv run room.py <command>`。
"""
import argparse
import datetime
import getpass
import gzip
import hashlib
import io
import json
import os
import re
import shlex
import shutil
import ssl
import stat
import subprocess
import sys
import tarfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import maskkit  # noqa: E402

MOUNT_ROOT = "/mnt/room"
ROOM_UID = 1000
REAP_DAYS_DEFAULT = 14
GITIGNORE_REQUIRED = ("**/_noai/", "!**/ai/out/")
AI_DIRS = ("ai/docs", "ai/in", "ai/work", "ai/out", "ai/records")
# data: データの扱い。none = マスクしない / mask = マスクだけ（復元しない）/ restore = マスクして復元する。
# user/ は、人だけが使う仮置き（予約名。room は触らない）。
DATA_MODES = ("none", "mask", "restore")
NOAI_DIRS = {
    "none": ("_noai/user",),
    "mask": ("_noai/raw", "_noai/map", "_noai/user"),
    "restore": ("_noai/raw", "_noai/map", "_noai/final", "_noai/user"),
}
AI_KEEP = ("ai/in", "ai/work", "ai/records")


class RoomError(Exception):
    pass


# ---------- 外部コマンド ----------

def wsl_env():
    """wsl.exe に渡す環境。WSLENV を外す（部屋へ Windows の環境変数を渡さない。automount を切った部屋では、/p 付きのパスが変換できず、壊れた SSL_CERT_FILE などが残って curl が証明書エラー（60）になる）。"""
    return {k: v for k, v in os.environ.items() if k.upper() != "WSLENV"}


class Wsl:
    """wsl.exe の呼び出し。コマンドは標準入力で、LF 固定で渡す（CRLF だと umount などが壊れる）。"""

    def distros(self):
        raw = subprocess.run(["wsl.exe", "-l", "-q"], capture_output=True, env=wsl_env()).stdout
        text = raw.replace(b"\x00", b"").decode("utf-8", "ignore")
        return [l.strip() for l in text.splitlines() if l.strip()]

    def script(self, distro, text, root=False):
        cmd = ["wsl.exe", "-d", distro] + (["-u", "root"] if root else []) + ["--", "sh", "-s"]
        r = subprocess.run(cmd, input=text.replace("\r\n", "\n").encode("utf-8"), capture_output=True, env=wsl_env())
        return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")

    def push(self, distro, data, script):
        """data（バイト列）を標準入力で渡して、script を一般ユーザーで実行する（共有知の写しを送る）。"""
        cmd = ["wsl.exe", "-d", distro, "--", "sh", "-c", script]
        r = subprocess.run(cmd, input=data, capture_output=True, env=wsl_env())
        return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")

    def install(self, distro, base):
        """base（例: Ubuntu-26.04）から、名前 distro のディストリビューションを作る（起動しない）。"""
        return subprocess.run(["wsl.exe", "--install", base, "--name", distro, "--no-launch"], env=wsl_env()).returncode

    def terminate(self, distro):
        return subprocess.run(["wsl.exe", "--terminate", distro], capture_output=True, env=wsl_env()).returncode

    def shell(self, distro):
        """部屋に入る（対話）。WSLENV を外すので、起動のたびの「failed to translate」が出ない。"""
        return subprocess.run(["wsl.exe", "-d", distro], env=wsl_env()).returncode

    def keepalive(self, distro):
        """部屋のディストリビューションが、wsl.exe のセッションが無いまま止まらないように、長く動くプロセスを1つ起こす。止めるには .terminate()。"""
        # コンソールから切り離す（同じコンソールにつながると、待ちの input() に Enter が届かないことがある。2026-10-18 に実機で、切り離すと Enter で戻ることを確認）
        flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
        return subprocess.Popen(["wsl.exe", "-d", distro, "--", "sleep", "infinity"],
                                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                creationflags=flags, env=wsl_env())

    def interactive(self, distro, command):
        """端末をつないだまま、一般ユーザーで実行する。"""
        return subprocess.run(["wsl.exe", "-d", distro, "--", "bash", "-ic", command], env=wsl_env()).returncode


def git(vault, *args, check=True):
    r = subprocess.run(["git", "-C", str(vault), *args], capture_output=True)
    out = r.stdout.decode("utf-8", "replace")
    if check and r.returncode != 0:
        raise RoomError(f"git {' '.join(args)} が失敗した: {r.stderr.decode('utf-8', 'replace').strip()}")
    return out


class Ctx:
    def __init__(self, vault, wsl=None, today=None, now=None, say=print, reap_days=REAP_DAYS_DEFAULT, settle=3,
                 ask=input, ask_secret=getpass.getpass):
        self.vault = Path(vault)
        self.wsl = wsl or Wsl()
        self._today = today
        self._now = now
        self.say = say
        self.reap_days = reap_days
        self.ask = ask
        self.ask_secret = ask_secret  # 入力を画面に出さない
        self.settle = settle  # アンマウント直後は、マウントが残って見えることがあるので待つ秒数

    def today(self):
        return self._today or datetime.date.today().isoformat()

    def now(self):
        return self._now or datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


# ---------- frontmatter ----------

def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text
    return text[4:end], text[end + 5:]


def read_frontmatter(path):
    text = Path(path).read_text(encoding="utf-8")
    fm, _ = split_frontmatter(text)
    data = {}
    for line in (fm or "").split("\n"):
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*?)\s*$", line)
        if m:
            data[m.group(1)] = re.sub(r"\s+#.*$", "", m.group(2))
    return data


def update_frontmatter(text, updates, remove=()):
    fm, body = split_frontmatter(text)
    if fm is None:
        raise RoomError("frontmatter が無い")
    lines = fm.split("\n")
    out, seen = [], set()
    for line in lines:
        m = re.match(r"^([A-Za-z0-9_]+):", line)
        key = m.group(1) if m else None
        if key in remove:
            continue
        if key in updates:
            out.append(f"{key}: {updates[key]}")
            seen.add(key)
        else:
            out.append(line)
    for key, val in updates.items():
        if key not in seen:
            # updated の前に、それ以外は末尾に足す
            out.append(f"{key}: {val}")
    return "---\n" + "\n".join(out) + "\n---\n" + body


# ---------- プロジェクト ----------

class Project:
    def __init__(self, ctx, name):
        self.ctx, self.name = ctx, name
        self.dir = ctx.vault / "projects" / name
        self.readme = self.dir / "README.md"
        self.ai = self.dir / "ai"
        self.fm = {}
        self.area = None

    @classmethod
    def load(cls, ctx, name):
        p = cls(ctx, name)
        if not p.readme.exists():
            raise RoomError(f"Project が無い: {p.dir}")
        p.fm = read_frontmatter(p.readme)
        p.data = p.fm.get("data") or "restore"  # data: が無い既存の Project は、今までどおり復元する
        if p.data not in DATA_MODES:
            raise RoomError(f"{p.readme} の data: が不正: {p.data!r}（{' / '.join(DATA_MODES)}）")
        p.area = p.fm.get("area")
        if not p.area:
            raise RoomError(f"{p.readme} の frontmatter に area: が無い")
        return p

    def type_is_dev_nonnone(self):
        return self.fm.get("type") == "dev" and self.data != "none"

    @property
    def distro(self):
        return f"room-{self.area}"

    @property
    def mount_point(self):
        return f"{MOUNT_ROOT}/{self.name}"

    @property
    def area_dir(self):
        return self.ctx.vault / "areas" / self.area

    @property
    def log_path(self):
        return self.ai / "records" / "room-log.md"


def check_gitignore(ctx):
    path = ctx.vault / ".gitignore"
    have = {l.strip() for l in path.read_text(encoding="utf-8").splitlines()} if path.exists() else set()
    missing = [x for x in GITIGNORE_REQUIRED if x not in have]
    if missing:
        raise RoomError(f".gitignore に必須の行が無い: {missing}（guides/howto/ai-room-setup.md の 2.1）")


def check_area(p):
    if not p.area_dir.exists():
        raise RoomError(f"Area が無い: {p.area_dir}")
    boundary = read_frontmatter(p.area_dir / "README.md").get("boundary", "")
    if not boundary:
        raise RoomError(f"Area の README.md に boundary: が無い（顧客・機密度の印）: {p.area_dir / 'README.md'}")
    return boundary


def check_distro(ctx, p):
    if p.distro not in ctx.wsl.distros():
        raise RoomError(f"部屋（ディストロ）が無い: {p.distro}。guides/howto/ai-room-setup.md の 3 章で作る")


def room_mounts(ctx, distro):
    rc, out, _ = ctx.wsl.script(distro, f"grep ' {MOUNT_ROOT}/' /proc/mounts || true\n")
    return [l for l in out.splitlines() if l.strip()]


# ---------- manifest（来歴） ----------

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_path(p):
    return p.ai / "records" / "manifest.json"


def load_manifest(p):
    path = manifest_path(p)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"version": 1, "files": {}}


def in_files(p):
    base = p.ai / "in"
    if not base.exists():
        return []
    return sorted(f for f in base.rglob("*") if f.is_file() and f.name != ".gitkeep")


def check_provenance(p):
    """ai/in の各ファイルの由来（Area と Project とハッシュ）が manifest と一致するか。問題の一覧を返す。"""
    man, problems = load_manifest(p), []
    for f in in_files(p):
        rel = f.relative_to(p.ai).as_posix()
        e = man["files"].get(rel)
        if e is None:
            problems.append(f"{rel}: 由来の記録が無い")
        elif (e.get("area"), e.get("project")) != (p.area, p.name):
            problems.append(f"{rel}: 由来が違う（{e.get('area')}/{e.get('project')}）")
        elif e.get("sha256") != sha256(f):
            problems.append(f"{rel}: 記録のあとで変更されている（ハッシュが違う）")
    return problems


def adopt_in(ctx, p):
    """人が『この Project の入力だ』と確認したファイルを、manifest に記録する。"""
    man = load_manifest(p)
    for f in in_files(p):
        rel = f.relative_to(p.ai).as_posix()
        man["files"][rel] = {"sha256": sha256(f), "area": p.area, "project": p.name, "added": ctx.now()}
    manifest_path(p).parent.mkdir(parents=True, exist_ok=True)
    manifest_path(p).write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return len(man["files"])


# ---------- 記録 ----------

LOG_HEADER = (
    "# 部屋の記録（room-log）\n\n"
    "`room start` / `room close` の実行ごとに追記する（`room.py` が書く）。\n\n"
    "| 日時 | 操作 | Area | ディストロ | マウント点 | チェック | 結果 |\n"
    "|---|---|---|---|---|---|---|\n"
)


def log_room(ctx, p, op, checks, result):
    p.log_path.parent.mkdir(parents=True, exist_ok=True)
    if not p.log_path.exists():
        p.log_path.write_text(LOG_HEADER, encoding="utf-8", newline="\n")
    row = f"| {ctx.now()} | {op} | {p.area} | {p.distro} | {p.mount_point} | {checks} | {result} |\n"
    with open(p.log_path, "a", encoding="utf-8", newline="\n") as f:
        f.write(row)


# ---------- マウント ----------

def mount(ctx, p):
    ai_win = str(p.ai)
    mp = shlex.quote(p.mount_point)
    script = (
        "set -e\n"
        f"mkdir -p {mp}\n"
        f"mount -t drvfs -o metadata,uid={ROOM_UID},gid={ROOM_UID} {shlex.quote(ai_win)} {mp}\n"
        f"find {mp}/in -type f -exec chmod a-w {{}} +\n"
    )
    rc, out, err = ctx.wsl.script(p.distro, script, root=True)
    if rc != 0:
        raise RoomError(f"マウントに失敗した: {err.strip() or out.strip()}")


def unmount(ctx, p):
    """アンマウントし、マウント点を消し、残りを確認する。残っていれば False。"""
    mp = shlex.quote(p.mount_point)
    script = (
        f"for i in 1 2 3 4 5; do umount {mp} 2>/dev/null || break; done\n"
        f"rmdir {mp} 2>/dev/null || true\n"
    )
    ctx.wsl.script(p.distro, script, root=True)
    time.sleep(ctx.settle)
    left = room_mounts(ctx, p.distro)
    # 入力の読み取り専用を、Windows 側で戻す（人が差し替えられるように）
    # （マウント時は .gitkeep も含めて in/ の全ファイルを読み取り専用にするので、戻すのも全ファイル）
    base = p.ai / "in"
    for f in (base.rglob("*") if base.exists() else []):
        if f.is_file():
            os.chmod(f, os.stat(f).st_mode | stat.S_IWRITE)
    return not left


def clean_stale_mountpoints(ctx, distro):
    ctx.wsl.script(distro, f"find {MOUNT_ROOT} -mindepth 1 -maxdepth 1 -type d -empty -exec rmdir {{}} + 2>/dev/null || true\n", root=True)


# ---------- git ----------

def unexpected_ignored(ctx, p):
    """追跡されずに、無視されているファイル（成果物が黙って漏れていないかの点検）。"""
    out = git(ctx.vault, "ls-files", "-o", "-i", "--exclude-standard", "-z", "--", f"projects/{p.name}/ai")
    res = []
    for f in out.split("\0"):
        if not f or "/ai/ctx/" in f or os.path.basename(f).startswith("~$"):
            continue
        res.append(f)
    return res


def commit_paths(ctx, paths, message, extra_allowed=(), only=False):
    """paths をステージしてコミットする。対象外のステージ済みの変更があるときは、既定では止まる。
    only=True は、止まらずに、対象のパスだけをコミットする（対象外の変更はステージに残る。init と open の初期状態用）。"""
    git(ctx.vault, "add", "-A", "--", *paths)
    staged = [l for l in git(ctx.vault, "diff", "--cached", "--name-only").splitlines() if l]
    if not staged:
        ctx.say("コミットする変更が無い")
        return
    allowed = tuple(p.rstrip("/") + "/" for p in (*paths, *extra_allowed))
    exact = {p.rstrip("/") for p in (*paths, *extra_allowed)}  # ファイルそのものを指すパス
    stray = [f for f in staged if f not in exact and not f.startswith(allowed)]
    if stray and not only:  # 並行する作業のステージ済みの変更を、巻き込まない
        raise RoomError("対象外のファイルがステージされている。コミットしない:\n  " + "\n  ".join(stray))
    if stray:
        ctx.say("注意: 対象外のステージ済みの変更は、コミットに含めない（ステージに残す）:\n  " + "\n  ".join(stray))
        ctx.say("ステージ済み（対象）: " + str(len(staged) - len(stray)) + " ファイル")
        git(ctx.vault, "commit", "-m", message, "--", *paths, *extra_allowed)
    else:
        ctx.say("ステージ済み: " + str(len(staged)) + " ファイル")
        git(ctx.vault, "commit", "-m", message)
    ctx.say("コミットした: " + git(ctx.vault, "log", "--oneline", "-1").strip())


# ---------- open ----------

README_TEMPLATE = """---
status: active
area: {area}
type: {type}
data: {data}
review: 仮置き（未承認）
created: {today}
updated: {today}
---

# {name}

<目的を1〜2文。所属 Area: [[areas/{area}/README|{area}]]>

## 完了条件

<1文。ユーザーが承認してから書く（承認の前に「ユーザー承認: 日付」を書かない）>

## 成果物

- `ai/out/<最終成果物>`: <成果物>

## 範囲外

- <やらないこと>

## Open Questions

- <未決の事項>
"""


def section_bounds(lines, heading):
    start = next((i for i, l in enumerate(lines) if l.strip() == heading), None)
    if start is None:
        return None, None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, end


def add_area_entry(text, heading, entry):
    lines = text.split("\n")
    s, e = section_bounds(lines, heading)
    if s is None:
        lines = lines + ["", heading, "", entry, ""]
        return "\n".join(lines)
    body = [l for l in lines[s + 1:e] if l.strip() and l.strip() != "なし。"]
    new = [heading, ""] + body + [entry, ""]
    return "\n".join(lines[:s] + new + lines[e:])


def move_area_entry(text, name, date):
    """進行中の一覧から Project の行を外し、完了した Project に、archives のリンクで移す。"""
    lines = text.split("\n")
    s, e = section_bounds(lines, "## 進行中の Project")
    marker = f"[[projects/{name}/README"
    found = None
    if s is not None:
        for i in range(s + 1, e):
            if marker in lines[i]:
                found = lines[i]
                del lines[i]
                break
        s, e = section_bounds(lines, "## 進行中の Project")
        if not any(l.strip().startswith("- ") for l in lines[s + 1:e]):
            lines[s + 1:e] = ["", "なし。", ""]
    if found is None:
        found = f"- [[projects/{name}/README|{name}]]"
    entry = found.replace(marker, f"[[archives/{name}/README")
    entry = entry[:-1] + f"、{date} 完了）" if entry.endswith("）") else entry + f"（{date} 完了）"
    return add_area_entry("\n".join(lines), "## 完了した Project", entry)


def cmd_open(ctx, a):
    check_gitignore(ctx)
    area_dir = ctx.vault / "areas" / a.area
    if not area_dir.exists():
        raise RoomError(f"Area が無い: {area_dir}")
    area_readme = area_dir / "README.md"
    boundary = read_frontmatter(area_readme).get("boundary", "")
    if not boundary:
        if not a.boundary:
            raise RoomError("Area に boundary: が無い。--boundary <印> で付ける（例: internal、顧客を表す名前）")
        area_readme.write_text(
            update_frontmatter(area_readme.read_text(encoding="utf-8"), {"boundary": a.boundary}),
            encoding="utf-8", newline="\n")
        ctx.say(f"Area に boundary: {a.boundary} を付けた")
    for top in ("projects", "archives"):
        if (ctx.vault / top / a.name).exists():
            raise RoomError(f"同名がすでにある: {top}/{a.name}")
    p = Project(ctx, a.name)
    p.area = a.area
    p.dir.mkdir(parents=True)
    data = getattr(a, "data", None) or "none"
    if a.type == "dev" and data != "none":
        ctx.say(f"警告: type: dev で data: {data} は仕様外（dev は data: none だけ）。作るが、動作は保証しない")
    for d in AI_DIRS + NOAI_DIRS[data]:
        (p.dir / d).mkdir(parents=True, exist_ok=True)
    for d in AI_KEEP:
        (p.dir / d / ".gitkeep").write_text("", encoding="utf-8")
    p.readme.write_text(README_TEMPLATE.format(area=a.area, type=a.type, data=data, today=ctx.today(), name=a.name),
                        encoding="utf-8", newline="\n")
    entry = f"- [[projects/{a.name}/README|{a.name}]]（{ctx.today()} 開始）"
    area_readme.write_text(add_area_entry(area_readme.read_text(encoding="utf-8"), "## 進行中の Project", entry),
                           encoding="utf-8", newline="\n")
    log_room(ctx, p, "open", "area 一致、boundary あり", "ひな形を作成")
    if p.distro not in ctx.wsl.distros():
        ctx.say(f"注意: 部屋（{p.distro}）がまだ無い。guides/howto/ai-room-setup.md の 3 章で作る")
    ctx.say(f"作った: projects/{a.name}（ai/ と _noai/）。README の <...> を埋める")
    if a.commit:  # 初期状態を、戻る起点としてコミットする（既定。--no-commit で省く）
        commit_paths(ctx, [f"projects/{a.name}", f"areas/{a.area}/README.md"], f"[room] {a.name} を open（Area {a.area}）", only=True)


# ---------- init（部屋を作る。手順は ai-room-setup.md の 3〜4 章） ----------

ROOM_BASE = "Ubuntu-26.04"
WSL_CONF = """[automount]
enabled=false
mountFsTab=false

[interop]
enabled=false
appendWindowsPath=false

[user]
default=ai
"""
ROOM_PATH_LINE = 'export PATH="$HOME/.local/bin:$PATH"'


def step_script(ctx, distro, title, text, root=False):
    ctx.say(f"  {title}")
    rc, out, err = ctx.wsl.script(distro, text, root=root)
    if rc != 0:
        raise RoomError(f"{title} が失敗した（終了コード {rc}）: {(err or out).strip()[-400:]}")
    return out


# Node.js: apt の版は古いことがある（Ubuntu 24.04 は 18）。Zed の ACP エージェント（npx）が 22 以上を要る。公式の tarball を、チェックサムを確かめて /usr/local へ展開する（取得したスクリプトは実行しない）
NODE_INSTALL = r"""set -e
if command -v node >/dev/null 2>&1 && node -v | grep -qE '^v(2[2-9]|[3-9][0-9])\.'; then node -v; exit 0; fi
case "$(uname -m)" in x86_64) A=x64;; aarch64) A=arm64;; *) echo "未対応のアーキテクチャ" >&2; exit 1;; esac
D=$(mktemp -d); cd "$D"
B=https://nodejs.org/dist/latest-v24.x
curl -fsSLO "$B/SHASUMS256.txt"
F=$(grep -o "node-v24[^ ]*-linux-$A.tar.xz" SHASUMS256.txt | head -1)
[ -n "$F" ]
curl -fsSLO "$B/$F"
grep " $F\$" SHASUMS256.txt | sha256sum -c -
tar -xJf "$F" -C /usr/local --strip-components=1 --exclude='*.md' --exclude=LICENSE
cd /; rm -rf "$D"
"""
NPM_CAFILE = "npm config set cafile /etc/ssl/certs/ca-certificates.crt\n"  # npm は証明書ストアを見ない。システムのバンドル（入れた勤務先の証明書を含む）を指す

CA_MAX_CERTS = 5  # need to know: 勤務先のルート証明書など、少数だけ。OS の証明書ストア丸ごとは入れない
CA_DEST = "/usr/local/share/ca-certificates/room-extra-ca.crt"


def load_ca_cert(path):
    """--ca-cert のファイルを検査して、(PEM テキスト, [(SHA-256, ...)]) を返す。秘密鍵が混ざる・多すぎる・証明書が無いときは止まる。"""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise RoomError(f"--ca-cert を読めない（{path}）: {e}")
    if "PRIVATE KEY" in text:
        raise RoomError("--ca-cert に秘密鍵が混ざっている。証明書だけのファイルを指定する")
    blocks = re.findall(r"-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----", text, re.S)
    if not blocks:
        raise RoomError("--ca-cert に PEM 形式の証明書が無い（.cer が DER 形式なら、PEM に変換する）")
    if len(blocks) > CA_MAX_CERTS:
        raise RoomError(f"--ca-cert の証明書が {len(blocks)} 枚ある（上限 {CA_MAX_CERTS}）。必要な勤務先のルート証明書だけのファイルにする")
    prints = [hashlib.sha256(ssl.PEM_cert_to_DER_cert(b)).hexdigest() for b in blocks]
    return "\n".join(blocks) + "\n", prints


AREA_README_TEMPLATE = """---
status: active
boundary: {boundary}
updated: {today}
---

# {area}
"""


def cmd_init(ctx, a):
    """Area の部屋（専用ディストロ）を作り、道具を入れる。ログインは人が行う。"""
    boundary_arg = getattr(a, "boundary", None)
    area_readme = ctx.vault / "areas" / a.area / "README.md"
    if not area_readme.exists():
        if not boundary_arg:
            raise RoomError(f"Area が無い: areas/{a.area}。作るなら --boundary <印> を付ける（例: internal、顧客を表す名前。既定値は無い）")
        area_readme.parent.mkdir(parents=True, exist_ok=True)
        area_readme.write_text(AREA_README_TEMPLATE.format(area=a.area, boundary=boundary_arg, today=ctx.today()),
                               encoding="utf-8", newline="\n")
        ctx.say(f"Area を作った: areas/{a.area}（boundary: {boundary_arg}）")
    elif not read_frontmatter(area_readme).get("boundary"):
        if not boundary_arg:
            raise RoomError("Area に boundary: が無い。--boundary <印> で付ける（README の frontmatter でもよい）")
        area_readme.write_text(update_frontmatter(area_readme.read_text(encoding="utf-8"), {"boundary": boundary_arg}),
                               encoding="utf-8", newline="\n")
        ctx.say(f"Area に boundary: {boundary_arg} を付けた")
    ca_cert = getattr(a, "ca_cert", None)
    ca_pem, ca_prints = load_ca_cert(ca_cert) if ca_cert else (None, [])  # 部屋を触る前に、検査で止める
    distro = f"room-{a.area}"
    exists = distro in ctx.wsl.distros()
    if exists and not a.resume:
        raise RoomError(f"部屋がすでにある: {distro}。作りかけの続きなら --resume（設定と道具の入れ直しだけを行う）")
    if not exists:
        if a.resume:
            raise RoomError(f"--resume だが部屋が無い: {distro}")
        ctx.say(f"部屋を作る: {distro}（{ROOM_BASE}。ダウンロードに数分かかる）")
        if ctx.wsl.install(distro, ROOM_BASE) != 0 or distro not in ctx.wsl.distros():
            raise RoomError("wsl --install が失敗した（古い WSL は --name が使えない可能性がある。ai-room-setup.md の 3 章）")
    ctx.say("設定する（一般ユーザーを先に作る。root のままだと C: をマウントできてしまう）")
    step_script(ctx, distro, "一般ユーザー ai", "id ai >/dev/null 2>&1 || useradd -m -u 1000 -s /bin/bash ai\nid ai\n", root=True)
    step_script(ctx, distro, "/etc/wsl.conf", "cat > /etc/wsl.conf <<'EOF'\n" + WSL_CONF + "EOF\n", root=True)
    ctx.wsl.terminate(distro)
    out = step_script(ctx, distro, "分離の確認",
                      "echo user=$(id -un)\necho c=$(ls /mnt/c 2>/dev/null | wc -l)\n"
                      "command -v cmd.exe >/dev/null 2>&1 && echo cmd=yes || echo cmd=no\n"
                      "sudo -n true >/dev/null 2>&1 && echo sudo=yes || echo sudo=no\n")
    got = dict(l.strip().split("=", 1) for l in out.splitlines() if "=" in l)
    if got != {"user": "ai", "c": "0", "cmd": "no", "sudo": "no"}:
        raise RoomError(f"分離の確認が目安と違う（{got}）。user=ai, c=0, cmd=no, sudo=no が目安。道具は入れていない")
    ctx.say("道具を入れる（curl、rg、Node.js、uv、Claude Code。配布元のスクリプトをそのまま実行する）")
    step_script(ctx, distro, "apt（curl, ca-certificates, ripgrep）",
                "apt-get update -qq && apt-get install -y -qq curl ca-certificates ripgrep\n", root=True)
    if ca_pem:
        ctx.say("証明書を入れる（root 所有。ai は読めるが書き換えられない）")
        for p in ca_prints:
            ctx.say(f"  SHA-256 {p}")
        step_script(ctx, distro, "update-ca-certificates",
                    f"cat > {CA_DEST} <<'EOF'\n{ca_pem}EOF\nchmod 644 {CA_DEST}\nupdate-ca-certificates\n", root=True)
    step_script(ctx, distro, "Node.js 24（公式の tarball、チェックサム確認つき）", NODE_INSTALL, root=True)
    step_script(ctx, distro, "npm の証明書", NPM_CAFILE)
    step_script(ctx, distro, "uv", "curl -LsSf https://astral.sh/uv/install.sh | sh\n")
    step_script(ctx, distro, "Claude Code", "curl -fsSL https://claude.ai/install.sh | bash\n")
    step_script(ctx, distro, "PATH",
                f"grep -qxF '{ROOM_PATH_LINE}' \"$HOME/.bashrc\" 2>/dev/null || echo '{ROOM_PATH_LINE}' >> \"$HOME/.bashrc\"\n")
    ver = step_script(ctx, distro, "道具の確認",
                      'export PATH="$HOME/.local/bin:$PATH"\nclaude --version\nuv --version\nnode --version\nrg --version | head -1\n')
    ctx.say(ver.rstrip())
    ctx.say(f"部屋ができた: {distro}。残りは人の操作（ログイン）:\n"
            f"  room shell {a.area}  →  claude  →  表示された URL をブラウザで開いてログイン  →  /exit\n"
            f"  Bedrock を使うなら: room aws-key {a.area} --profile <名前>（キーを入れる）\n"
            f"  確認: wsl -d {distro} -- bash -ic 'cd ~ && claude -p \"Reply with exactly: ok\"'")
    rel = f"areas/{a.area}/README.md"
    if getattr(a, "commit", False) and git(ctx.vault, "status", "--porcelain", "--", rel).strip():
        commit_paths(ctx, [rel], f"[room] init {a.area}（Area の作成、boundary: {read_frontmatter(area_readme).get('boundary')}）", only=True)


# ---------- start ----------

def preflight(ctx, p):
    if p.fm.get("status") != "active":
        raise RoomError(f"Project が active でない: status={p.fm.get('status')}")
    check_gitignore(ctx)
    boundary = check_area(p)
    check_distro(ctx, p)
    mounts = room_mounts(ctx, p.distro)
    if mounts:
        raise RoomError("部屋にマウントが残っている（同時に開かない）。`room umount --area "
                        f"{p.area}` で外す:\n  " + "\n  ".join(mounts))
    clean_stale_mountpoints(ctx, p.distro)
    return boundary


def rmtree_force(path):
    """Windows の読み取り専用ファイルも消す。"""
    def onerror(func, p, _exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)
    shutil.rmtree(path, onerror=onerror) if Path(path).exists() else None


AREA_README_WARN_BYTES = 16 * 1024  # Area の README の写しは、AI が開始時に読む。大きくなったら知らせる


def _snapshot(src, dst):
    if dst.exists():
        os.chmod(dst, stat.S_IWRITE | stat.S_IREAD)
    shutil.copyfile(src, dst)
    os.chmod(dst, stat.S_IREAD)


def snapshot_readme(p):
    """Project の README と、所属する Area の README（Area の共通ルール）を `ai/ctx/` に写す。Area の README の大きさを返す。"""
    ctx_dir = p.ai / "ctx"
    ctx_dir.mkdir(parents=True, exist_ok=True)
    _snapshot(p.readme, ctx_dir / "README.md")
    area_readme = p.area_dir / "README.md"
    _snapshot(area_readme, ctx_dir / "area-README.md")
    return area_readme.stat().st_size


# ---------- 共有知の写し（方式 A。考え方は guides/explain/ai-room-why.md の「共有知との行き来」） ----------

SHARE_PATHS = ("AGENTS.md", "workflow-kit", "exmem/AGENTS.md", "exmem/README.md", "exmem/exmem-index.md", "exmem/tags.md", "exmem/lessons", "guides")
SHARE_SKIP = {".git", ".venv", "__pycache__", "node_modules"}
# 部屋の AI に送らない: room 自身のコード・テスト・設定（人の側の道具）。README.md だけ、参照が切れないよう送る
SHARE_ROOM_DIR = "workflow-kit/room"
SHARE_ROOM_KEEP = {"workflow-kit/room/README.md"}


def share_skipped(arc):
    return arc.startswith(SHARE_ROOM_DIR + "/") and arc not in SHARE_ROOM_KEEP
SHARE_DEST = "shared"  # 部屋の一般ユーザーの ~/shared

ROOM_GUIDE = """# 共有知の写し（読み取り専用）

この `~/shared` は、`room start` が送った workbase（共有知）の写し。セッションの途中では更新されない。書き込めない。

- 基準コミット: {commit}{dirty}
- 送った日時: {now}

読むところ:
- 合言葉と手順書: `~/shared/workflow-kit/hooks.md`（表）、`~/shared/workflow-kit/*-hook.md`
- 共通規約: `~/shared/AGENTS.md`、`~/shared/exmem/AGENTS.md`
- 知識: `~/shared/exmem/exmem-index.md`→ `~/shared/exmem/lessons/*.md`
- 手順書・理解ガイド: `~/shared/guides/guides-index.md`

共有知へ戻したい知見（`stock`）は、直接書かず、`ai/out/stock/` に下書きを書く。下書きの frontmatter に次を足す:

- `base_commit: {commit}`
- `observed: 書いた日（YYYY-MM-DD）`

人が確認して `exmem/inbox/` へ運ぶ。

`ai/out/` の文書に、`⟦` と `⟧` を、マスクの記号以外の用途で書かない。説明文でプレースホルダーの形を示すときは、「CUST_001 の形」のように括弧なしで書く（`⟦CUST_nnn⟧` のような書き方は、復元が壊れた記号として止まる）。
"""


def share_root(ctx):
    return ctx.vault / "resources"


def build_share_tar(root, extra=None):
    """共有知の写しを tar.gz にする（順序と時刻を固定して、同じ内容なら同じバイト列）。"""
    raw_tar = io.BytesIO()
    with tarfile.open(fileobj=raw_tar, mode="w", format=tarfile.PAX_FORMAT) as tf:
        def add(path, arc):
            ti = tf.gettarinfo(str(path), arcname=arc)
            ti.mtime, ti.uid, ti.gid, ti.uname, ti.gname = 0, 0, 0, "", ""
            ti.mode = 0o755 if path.is_dir() else (0o755 if ti.mode & 0o100 else 0o644)
            if path.is_dir():
                tf.addfile(ti)
                for ch in sorted(path.iterdir()):
                    child = f"{arc}/{ch.name}"
                    if ch.name not in SHARE_SKIP and not share_skipped(child):
                        add(ch, child)
            else:
                with open(path, "rb") as f:
                    tf.addfile(ti, f)
        for rel in SHARE_PATHS:
            src = root / rel
            if src.exists():
                add(src, rel)
        for name, text in sorted((extra or {}).items()):
            raw = text.encode("utf-8")
            ti = tarfile.TarInfo(name)
            ti.size, ti.mode = len(raw), 0o644
            tf.addfile(ti, io.BytesIO(raw))
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="wb", compresslevel=6, mtime=0) as gz:  # gzip ヘッダーの時刻も固定する
        gz.write(raw_tar.getvalue())
    return out.getvalue()


def share_state(ctx, root):
    """(コミット, 未コミットの変更があるか)。git でなければ ('不明', False)。"""
    r = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True)
    if r.returncode != 0:
        return "不明", False
    commit = r.stdout.decode().strip()
    dirty = bool(git(root, "status", "--porcelain", "--", *[x for x in SHARE_PATHS if (root / x).exists()], check=False).strip())
    return commit, dirty


POINTER_BEGIN = "<!-- room-shared:begin（room start が管理する。この範囲は書き換えられる） -->"
POINTER_END = "<!-- room-shared:end -->"
POINTER_TEXT = """共有知（読み取り専用の写し）が `~/shared` にある。作業の前に `~/shared/ROOM.md` を読む。
合言葉（`start` `wrap` など）を言われたら、`~/shared/workflow-kit/hooks.md` の表に従って手順書を読む。`~/shared` には書かない。"""


def install_guide_pointer(ctx, p):
    """部屋の一般ユーザーの ~/.claude/CLAUDE.md（Claude Code が、作業ディレクトリによらず読む）に、~/shared/ROOM.md への案内を入れる。
    目印で囲んだ範囲だけを入れ替え、ほかの内容は変えない。"""
    block = f"{POINTER_BEGIN}\n{POINTER_TEXT}\n{POINTER_END}\n"
    # ここは標準入力から渡す sh -s なので、変数を使ってよい（wsl.exe の `sh -c` の二重解釈を受けない）
    script = (
        "set -e\n"
        "f=\"$HOME/.claude/CLAUDE.md\"\n"
        "mkdir -p \"$HOME/.claude\"\n"
        "touch \"$f\"\n"
        "sed -i '/^<!-- room-shared:begin/,/^<!-- room-shared:end -->/d' \"$f\"\n"
        "if [ -s \"$f\" ] && [ -n \"$(tail -c1 \"$f\")\" ]; then echo >> \"$f\"; fi\n"
        "cat >> \"$f\" <<'ROOM_POINTER_EOF'\n"
        f"{block}"
        "ROOM_POINTER_EOF\n"
    )
    rc, out, err = ctx.wsl.script(p.distro, script)
    if rc != 0:
        raise RoomError(f"部屋の ~/.claude/CLAUDE.md に案内を入れられなかった: {err.strip() or out.strip()}")


SHARED_RULE = "Read(~/shared/**)"
SHARED_RULE_PY = """import json, os
f = os.path.expanduser("~/.claude/settings.json")
d = {}
if os.path.exists(f) and os.path.getsize(f) > 0:
    with open(f, encoding="utf-8") as fh:
        d = json.load(fh)
allow = d.setdefault("permissions", {}).setdefault("allow", [])
if "Read(~/shared/**)" not in allow:
    allow.append("Read(~/shared/**)")
os.makedirs(os.path.dirname(f), exist_ok=True)
with open(f, "w", encoding="utf-8", newline="\\n") as fh:
    json.dump(d, fh, ensure_ascii=False, indent=2)
    fh.write("\\n")
"""


def install_shared_permission(ctx, p):
    """部屋の一般ユーザーの ~/.claude/settings.json に、~/shared の読み取りだけの許可を足す（既存の項目は残す。毎回の確認を無くす）。
    `Read(~/shared/**)` は読み取りだけを許す。`~/.claude/.credentials.json` など、ほかの場所は許さない。"""
    script = ("set -e\n"
              "python3 - <<'ROOM_PERM_EOF'\n"
              f"{SHARED_RULE_PY}"
              "ROOM_PERM_EOF\n")
    rc, out, err = ctx.wsl.script(p.distro, script)
    if rc != 0:
        raise RoomError(f"部屋の ~/.claude/settings.json に ~/shared の許可を足せなかった: {err.strip() or out.strip()}")


TRUST_PY = """import json, os
f = os.path.expanduser("~/.claude.json")
d = {{}}
if os.path.exists(f) and os.path.getsize(f) > 0:
    with open(f, encoding="utf-8") as fh:
        d = json.load(fh)
d.setdefault("projects", {{}}).setdefault({path}, {{}})["hasTrustDialogAccepted"] = True
with open(f, "w", encoding="utf-8", newline="\\n") as fh:
    json.dump(d, fh, ensure_ascii=False, indent=2)
    fh.write("\\n")
"""


def install_project_trust(ctx, p):
    """部屋の一般ユーザーの ~/.claude.json で、この Project のマウント先を信頼済みにする（新しい Project のたびの「信頼しますか」を省く。
    部屋の ai/ は AI が書く領域で、人が持ち込んだ設定ファイルは来歴チェックを通ったものだけ）。"""
    script = ("set -e\n"
              "python3 - <<'ROOM_TRUST_EOF'\n"
              f"{TRUST_PY.format(path=json.dumps(p.mount_point))}"
              "ROOM_TRUST_EOF\n")
    rc, out, err = ctx.wsl.script(p.distro, script)
    if rc != 0:
        raise RoomError(f"部屋の ~/.claude.json に信頼の記録を足せなかった: {err.strip() or out.strip()}")


def push_shared(ctx, p):
    """workbase の写しを、部屋の ~/shared に読み取り専用で送り、基準コミットを manifest に記録する。送ったら True。"""
    root = share_root(ctx)
    if not root.is_dir():
        ctx.say(f"共有知の写しは送らない（{root} が無い）")
        return False
    commit, dirty = share_state(ctx, root)
    guide = ROOM_GUIDE.format(commit=commit, dirty="（未コミットの変更を含む）" if dirty else "", now=ctx.now())
    data = build_share_tar(root, {"ROOM.md": guide})
    ctx_dir = p.ai / "ctx"
    ctx_dir.mkdir(parents=True, exist_ok=True)
    (ctx_dir / "SHARED.md").write_text(guide, encoding="utf-8", newline="\n")
    # wsl.exe は `sh -c` の引数を、部屋の側の外側のシェルでもう一度解釈する。スクリプト内で代入した変数（$d など）は
    # 外側で空に展開されるので、変数を使わず $HOME/<dest> を直接書く（$HOME は外側でも定義されている）。
    d = f"\"$HOME/{SHARE_DEST}\""
    script = (f"set -e; if [ -e {d} ]; then chmod -R u+w {d}; rm -rf {d}; fi; "
              f"mkdir -p {d} && tar xzf - -C {d}; "
              f"chmod -R a-w {d}")
    rc, _o, err = ctx.wsl.push(p.distro, data, script)
    if rc != 0:
        raise RoomError(f"共有知の写しを送れなかった: {err.strip()}")
    install_guide_pointer(ctx, p)
    install_shared_permission(ctx, p)
    man = load_manifest(p)
    man["shared"] = {"commit": commit, "dirty": dirty, "pushed": ctx.now(), "paths": [x for x in SHARE_PATHS if (root / x).exists()],
                     "tar_sha256": hashlib.sha256(data).hexdigest()}
    manifest_path(p).parent.mkdir(parents=True, exist_ok=True)
    manifest_path(p).write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    ctx.say(f"共有知の写しを送った: ~/{SHARE_DEST}（基準コミット {commit[:10]}{'、未コミットの変更あり' if dirty else ''}）")
    return True


def cmd_start(ctx, a):
    p = Project.load(ctx, a.name)
    boundary = preflight(ctx, p)
    if p.data == "none":
        if maskkit.list_files(noai_dir(p) / "raw"):
            raise RoomError("data: none だが _noai/raw に原本がある。README の data: を mask か restore にする")
        masked = 0
    else:
        masked = mask_project(ctx, p, yes=a.yes)
    if p.type_is_dev_nonnone():
        ctx.say(f"警告: type: dev で data: {p.data} は仕様外（dev は data: none だけ）")
    if a.adopt:
        n = adopt_in(ctx, p)
        ctx.say(f"ai/in の {n} ファイルを、この Project の入力として manifest に記録した")
    problems = check_provenance(p)
    if problems:
        raise RoomError("来歴チェックに失敗した:\n  " + "\n  ".join(problems)
                        + "\n（人が確認したファイルなら、--adopt で記録する）")
    checks = f"area 一致、boundary={boundary}、in {len(in_files(p))} 件の来歴 OK" + (f"、マスク {masked} 件" if masked else "")
    area_size = snapshot_readme(p)
    if area_size > AREA_README_WARN_BYTES:
        ctx.say(f"注意: Area の README が大きい（{area_size // 1024} KiB）。部屋の AI が開始時に読むので、"
                "完了した Project の一覧などを畳むことを検討する")
    if push_shared(ctx, p):
        checks += "、共有知の写し送付"
    install_project_trust(ctx, p)
    ctx.say(f"チェック OK（{checks}）")
    result = "不明"
    try:
        mount(ctx, p)
        ctx.say(f"マウントした: {p.mount_point}")
        if a.no_launch:
            ctx.say("--no-launch: ここで AI を起動しない。Zed などで WSL リモート接続し、終わったら Enter")
            keep = ctx.wsl.keepalive(p.distro)  # セッションが無くなって部屋が止まると、マウントも消える（仮説。実機で確認する）
            try:
                input()
            finally:
                keep.terminate()
            rc = 0
        else:
            ctx.say(f"起動: {a.cmd}")
            rc = ctx.wsl.interactive(p.distro, f"cd {shlex.quote(p.mount_point)} && {a.cmd}")
        result = f"終了コード {rc}"
    finally:
        ok = unmount(ctx, p)
        rmtree_force(p.ai / "ctx")
    if not ok:
        log_room(ctx, p, "start", checks, result + "、**マウントが残っている**")
        raise RoomError("アンマウントを確認できなかった。`room umount --area " + p.area + "` で外し、/proc/mounts を確認する")
    restored, restore_problems = restore_project(ctx, p) if p.data == "restore" else (0, [])
    if restored:
        ctx.say(f"復元した: {restored} ファイル → _noai/final")
    ignored = unexpected_ignored(ctx, p)
    status = [l for l in git(ctx.vault, "status", "--porcelain", "-uall", "--", f"projects/{p.name}").splitlines() if l]
    log_room(ctx, p, "start", checks, f"{result}、変更 {len(status)} 件")
    ctx.say(f"回収: 変更 {len(status)} 件")
    for l in status:
        ctx.say("  " + l)
    if ignored:
        ctx.say("警告: 追跡されずに無視されているファイル（成果物が漏れている可能性）:")
        for f in ignored:
            ctx.say("  " + f)
    if restore_problems:
        raise RoomError("復元を止めた（_noai/final は変更していない。ai/out は回収済み）:\n  " + "\n  ".join(restore_problems)
                        + "\n（直して `room restore " + p.name + "` を再実行する。コミットはしていない）")
    if a.commit:
        commit_paths(ctx, [f"projects/{p.name}"], f"[room] {p.name}: start {ctx.now()}")


# ---------- マスクと復元（maskkit。仕様は mask-spec.md） ----------

def noai_dir(p):
    return p.dir / "_noai"


def write_bytes(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def mask_project(ctx, p, yes=False):
    """_noai/raw の新しい・変わった原本を、マスクして ai/in へ。点検に通らなければ止める。作った件数を返す。"""
    n = noai_dir(p)
    raw = maskkit.list_files(n / "raw")
    if not raw:
        return 0
    conf_path = n / "mask.toml"
    if not conf_path.exists():
        raise RoomError(f"_noai/raw に原本があるが、{conf_path} が無い（マスクの指定を人が書く）")
    try:
        config = maskkit.load_config(conf_path)
        mapping = maskkit.Mapping.load(n / "map" / "mapping.json")
        conf_hash = maskkit.sha256_bytes(conf_path.read_bytes())
        man = load_manifest(p)
        todo, rebuild = set(), False
        for rel, data in raw.items():
            e = man["files"].get(f"in/{rel}")
            if e is None or e.get("raw_sha256") != maskkit.sha256_bytes(data) or not (p.ai / "in" / rel).exists():
                todo.add(rel)
            elif e.get("mask_sha256") != conf_hash:
                rebuild = True
        if rebuild:
            ctx.say("mask.toml が変わった。ai/in の全ファイルを作り直す")
            if not yes and input("作り直してよいか [y/N]: ").strip().lower() != "y":
                raise RoomError("作り直しを中止した")
            todo = set(raw)
        if not todo:
            return 0
        res = maskkit.mask_files(raw, config, mapping, only=todo)
    except maskkit.MaskError as e:
        raise RoomError(f"マスクを止めた（ai/in は変更していない）:\n{e}")
    version = sum(mapping.data["counters"].values())
    for rel, data in res["outputs"].items():
        write_bytes(p.ai / "in" / rel, data)
        man["files"][f"in/{rel}"] = {
            "sha256": maskkit.sha256_bytes(data), "area": p.area, "project": p.name, "added": ctx.now(),
            "raw_sha256": maskkit.sha256_bytes(raw[rel]), "mask_sha256": conf_hash, "mapping_version": version,
            "masked_from": f"_noai/raw/{rel}",
        }
    mapping.save(n / "map" / "mapping.json")
    manifest_path(p).parent.mkdir(parents=True, exist_ok=True)
    manifest_path(p).write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    ctx.say(f"マスクした: {len(res['outputs'])} ファイル → ai/in（対応表の版 {version}）")
    for w in res["warnings"]:
        ctx.say("  注意: " + w)
    if res["hints"]:
        ctx.say("  対応表に無い固有名詞の候補（必要なら mask.toml に足す。止めない）:")
        for h in res["hints"]:
            ctx.say("    " + h)
    return len(res["outputs"])


def restore_project(ctx, p, force=False):
    """ai/out を復元して _noai/final へ。戻らないもの、または人が変えた final があれば（force 以外は）何も書かずに問題の一覧を返す。"""
    n = noai_dir(p)
    out = maskkit.list_files(p.ai / "out")
    if not out:
        return 0, []
    mapping = maskkit.Mapping.load(n / "map" / "mapping.json")
    try:
        restored, problems = maskkit.restore_files(out, mapping)
    except maskkit.MaskError as e:
        return 0, [str(e)]
    if problems:
        return 0, problems
    mf = n / "map" / "final-manifest.json"
    written = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {}
    if not force:
        changed = []
        for rel, data in restored.items():
            dest = n / "final" / rel
            if dest.exists():
                cur = dest.read_bytes()
                if cur != data and written.get(rel) != maskkit.sha256_bytes(cur):
                    changed.append(f"{rel}: _noai/final が、前回の復元から変わっている（人の変更を上書きしてしまう）")
        if changed:
            return 0, changed + ["（確認して、上書きしてよければ `room restore " + p.name + " --force`。人の変更は先に退避する）"]
    for rel, data in restored.items():
        write_bytes(n / "final" / rel, data)
        written[rel] = maskkit.sha256_bytes(data)
    write_bytes(mf, json.dumps(written, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8"))
    return len(restored), []


def cmd_mask(ctx, a):
    p = Project.load(ctx, a.name)
    preflight(ctx, p)
    if p.data == "none":
        raise RoomError("data: none の Project はマスクしない（README の data: を mask か restore にする）")
    k = mask_project(ctx, p, yes=a.yes)
    if k == 0:
        ctx.say("マスクするものは無い（原本が無いか、変更が無い）")


def cmd_restore(ctx, a):
    p = Project.load(ctx, a.name)
    if p.data != "restore":
        raise RoomError(f"data: {p.data} の Project は復元しない（復元するなら README の data: を restore にする）")
    k, problems = restore_project(ctx, p, force=a.force)
    if problems:
        raise RoomError("復元を止めた（_noai/final は変更していない）:\n  " + "\n  ".join(problems))
    ctx.say(f"復元した: {k} ファイル → _noai/final")


def cmd_readme(ctx, a):
    """部屋の AI が書いた ai/out/readme-draft.md（本文だけ）を、Project の README.md の本文に反映する。frontmatter は変えない（updated だけ今日にする）。"""
    p = Project.load(ctx, a.name)
    draft = p.ai / "out" / "readme-draft.md"
    if not draft.exists():
        raise RoomError(f"下書きが無い: {draft}（部屋の AI に ai/out/readme-draft.md を書かせる）")
    body = draft.read_text(encoding="utf-8").replace("\r\n", "\n")
    if split_frontmatter(body)[0] is not None:
        raise RoomError("下書きに frontmatter がある。本文だけにする（frontmatter は README.md のものを使う）")
    if not body.strip():
        raise RoomError("下書きが空")
    old = p.readme.read_text(encoding="utf-8")
    _fm, old_body = split_frontmatter(old)
    new = update_frontmatter(old, {"updated": ctx.today()})
    new = new[:len(new) - len(old_body)] + body.rstrip("\n") + "\n"
    if new == old:
        ctx.say("README.md は下書きと同じ。変更なし")
        return
    ctx.say("README.md の本文を、下書きに置き換える（frontmatter は変えない）")
    if not a.yes and input("反映してよいか [y/N]: ").strip().lower() != "y":
        raise RoomError("反映を中止した")
    p.readme.write_text(new, encoding="utf-8", newline="\n")
    ctx.say("反映した。確認して、コミットする（`git diff projects/" + p.name + "/README.md`）")
    if a.commit:
        commit_paths(ctx, [f"projects/{p.name}/README.md"], f"[room] {p.name}: README を更新 {ctx.now()}")


# ---------- 【汎用】の下書きの回収（stock） ----------

def stock_staleness(ctx, base):
    """(基準コミットが有効か, lessons で基準以降に変わったファイルの一覧)。"""
    root = share_root(ctx)
    if not base or subprocess.run(["git", "-C", str(root), "cat-file", "-e", f"{base}^{{commit}}"], capture_output=True).returncode != 0:
        return False, []
    out = git(root, "diff", "--name-only", base, "HEAD", "--", "exmem/lessons", check=False)
    return True, [l.strip().removeprefix("exmem/") for l in out.splitlines() if l.strip()]


def cmd_stock(ctx, a):
    """ai/out/stock/*.md（部屋の AI の【汎用】の下書き）を、人の確認を経て resources/exmem/inbox/ に運ぶ。コミットしない（stock-hook.md の方針）。"""
    p = Project.load(ctx, a.name)
    src = p.ai / "out" / "stock"
    drafts = sorted(f for f in src.glob("*.md")) if src.exists() else []
    if not drafts:
        ctx.say("運ぶ下書きは無い（ai/out/stock/*.md）")
        return
    inbox = share_root(ctx) / "exmem" / "inbox"
    if not inbox.is_dir():
        raise RoomError(f"運び先が無い: {inbox}")
    n = p.dir / "_noai" / "map" / "mapping.json"
    table = maskkit.Table(maskkit.Mapping.load(n)) if n.exists() else None
    man = load_manifest(p)
    sent = man.setdefault("stock", {})
    delivered = 0
    for f in drafts:
        raw = f.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if sent.get(f.name, {}).get("sha256") == digest:
            ctx.say(f"  済み（同じ内容を運んだ）: {f.name}")
            continue
        text = raw.decode("utf-8").replace("\r\n", "\n")
        fm = split_frontmatter(text)[0]
        if fm is None:
            ctx.say(f"  運ばない（frontmatter が無い）: {f.name}")
            continue
        meta = read_frontmatter(f)
        base, observed = meta.get("base_commit", ""), meta.get("observed", "")
        if not base or not observed:
            ctx.say(f"  運ばない（frontmatter に base_commit と observed が要る）: {f.name}")
            continue
        if table is not None and table.search(text):
            ctx.say(f"  運ばない（対応表の語が含まれている。公開されうる workbase に入れない）: {f.name}: {table.search(text).group(0)}")
            continue
        valid, changed = stock_staleness(ctx, base)
        cands = set(re.findall(r"lessons/([^\s）)、,]+?\.md)", text.split("\n## Principles")[0]))
        hit = sorted(c for c in cands if f"lessons/{c}" in changed)
        if not valid:
            stale = "基準コミットを確認できない"
        elif hit:
            stale = "統合先の lessons が基準以降に変わった: " + ", ".join(hit)
        elif cands:
            stale = ""
        else:
            stale = f"統合先の候補が特定できない（lessons の変更 {len(changed)} 件）" if changed else ""
        title = meta.get("title", f.name)
        ctx.say(f"  {f.name}: {title}" + (f"\n    印: 基準が古い可能性 — {stale}" if stale else ""))
        if not a.yes and input("    exmem/inbox に運ぶか [y/N]: ").strip().lower() != "y":
            ctx.say("    運ばなかった")
            continue
        if stale:
            text = update_frontmatter(text, {"base_stale": f'"{stale}"'})
        dst = inbox / f.name
        k = 2
        while dst.exists():
            dst = inbox / f"{f.stem}-{k}{f.suffix}"
            k += 1
        dst.write_text(text, encoding="utf-8", newline="\n")
        sent[f.name] = {"sha256": digest, "delivered": ctx.now(), "inbox": dst.name, "base_commit": base, "stale": bool(stale)}
        delivered += 1
        ctx.say(f"    運んだ: exmem/inbox/{dst.name}（未追跡のまま。点検: check-inbox.ps1）")
    manifest_path(p).parent.mkdir(parents=True, exist_ok=True)
    manifest_path(p).write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    ctx.say(f"{delivered} 件を運んだ")


# ---------- umount ----------

def cmd_umount(ctx, a):
    distro = f"room-{a.area}"
    if distro not in ctx.wsl.distros():
        raise RoomError(f"部屋が無い: {distro}")
    ctx.wsl.script(distro, f"for m in $(grep ' {MOUNT_ROOT}/' /proc/mounts | cut -d' ' -f2); do "
                           "for i in 1 2 3 4 5; do umount \"$m\" 2>/dev/null || break; done; rmdir \"$m\" 2>/dev/null; done\n", root=True)
    clean_stale_mountpoints(ctx, distro)
    left = room_mounts(ctx, distro)
    ctx.say("マウントは残っていない" if not left else "残っている:\n  " + "\n  ".join(left))
    if left:
        raise RoomError("アンマウントできなかった")


# ---------- close ----------

INBOX_NEW = (
    "# inbox（Project から Area への郵便受け）\n\n"
    "Project の `room start` / `room close` の回収が、【案件】の項目をここへ追記する。Area の AI が、次に Area の部屋を開いたとき（`start`）に読み、"
    "取り込んだら「取り込み済み」に移す。同じ項目は二度送らない（識別子 = Project 名 + 連番）。\n\n"
    "## 未取り込み\n\n## 取り込み済み\n\nなし。\n"
)


def parse_cases(close_md):
    return [m.group(1).strip() for m in re.finditer(r"^\s*-\s*【案件】(.+)$", close_md, re.M)]


def append_inbox(text, name, date, items, source):
    existing = {m.group(2).strip(): int(m.group(1))
                for m in re.finditer(rf"`{re.escape(name)}#(\d+)`\s*(.+)$", text, re.M)}
    top = max(existing.values(), default=0)
    new = [t for t in items if t not in existing]
    if not new:
        return text, 0
    block = [f"### {name}（{date}、close で渡した）", ""]
    for i, t in enumerate(new, start=top + 1):
        block.append(f"- `{name}#{i}` {t}")
    block += ["", f"出典: `{source}`", ""]
    lines = text.split("\n")
    idx = next((i for i, l in enumerate(lines) if l.strip() == "## 取り込み済み"), None)
    if idx is None:
        return text.rstrip("\n") + "\n\n" + "\n".join(block), len(new)
    lines[idx:idx] = block
    return "\n".join(lines), len(new)


README_PLACEHOLDERS = ("<目的を1〜2文", "<1文。ユーザーが承認", "<最終成果物>", "<やらないこと>")


def readme_placeholders(text):
    """README に残っている、ひな形（README_TEMPLATE）の <...> の行。"""
    return [line.strip() for line in text.splitlines() if any(m in line for m in README_PLACEHOLDERS)]


def cmd_close(ctx, a):
    p = Project.load(ctx, a.name)
    if p.fm.get("status") != "active":
        raise RoomError(f"Project が active でない: status={p.fm.get('status')}")
    left = readme_placeholders(p.readme.read_text(encoding="utf-8"))
    if left:
        raise RoomError("README がひな形のまま（<...> が残っている）。埋めてから close する:\n  " + "\n  ".join(left))
    check_gitignore(ctx)
    check_area(p)
    check_distro(ctx, p)
    mounts = room_mounts(ctx, p.distro)
    if mounts:
        raise RoomError("マウントが残っている。先に外す（`room umount --area " + p.area + "`）:\n  " + "\n  ".join(mounts))
    close_md = p.ai / "out" / "close.md"
    if not close_md.exists():
        raise RoomError("ai/out/close.md が無い。部屋の AI に close の判断を行わせて、書かせる")
    problems = check_provenance(p)
    if problems:
        raise RoomError("来歴チェックに失敗した:\n  " + "\n  ".join(problems))
    cases = parse_cases(close_md.read_text(encoding="utf-8"))
    today = ctx.today()
    reap = (datetime.date.fromisoformat(today) + datetime.timedelta(days=ctx.reap_days)).isoformat()
    # 1. Area の inbox
    inbox = p.area_dir / "ai" / "docs" / "inbox.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    text = inbox.read_text(encoding="utf-8") if inbox.exists() else INBOX_NEW
    text, n = append_inbox(text, p.name, today, cases, f"archives/{p.name}/ai/out/close.md")
    inbox.write_text(text, encoding="utf-8", newline="\n")
    ctx.say(f"Area の inbox に【案件】{n} 件を追記した（{len(cases) - n} 件は送信済み）")
    # 2. README の状態
    p.readme.write_text(
        update_frontmatter(p.readme.read_text(encoding="utf-8"),
                           {"status": "done", "updated": today, "closed": today, "reap_after": reap},
                           remove=("review",)),
        encoding="utf-8", newline="\n")
    # 3. Area の一覧
    ar = p.area_dir / "README.md"
    ar.write_text(move_area_entry(ar.read_text(encoding="utf-8"), p.name, today), encoding="utf-8", newline="\n")
    log_room(ctx, p, "close", f"area 一致、案件 {len(cases)} 件", f"archives へ移動、reap_after {reap}")
    rmtree_force(p.ai / "ctx")
    # 4. archives へ（追跡するファイルは、ファイル単位の git mv）
    git(ctx.vault, "add", "-A", "--", f"projects/{p.name}", f"areas/{p.area}")
    files = [f for f in git(ctx.vault, "ls-files", "-z", "--", f"projects/{p.name}").split("\0") if f]
    for f in files:
        to = "archives/" + f[len("projects/"):]
        (ctx.vault / to).parent.mkdir(parents=True, exist_ok=True)
        git(ctx.vault, "mv", f, to)
    dest = ctx.vault / "archives" / p.name
    for f in sorted(p.dir.rglob("*")):
        if f.is_file():  # 追跡外（_noai など）
            to = dest / f.relative_to(p.dir)
            to.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(to))
    for d in sorted((x for x in p.dir.rglob("*") if x.is_dir()), key=lambda x: len(str(x)), reverse=True):
        os.rmdir(d)
    os.rmdir(p.dir)
    ctx.say(f"archives/{p.name} へ移した（追跡 {len(files)} ファイル）。reap_after: {reap}")
    ctx.say(f"部屋の会話履歴（{p.distro} の ~/.claude/projects/-mnt-room-{p.name}/）は、reap_after まで残す")
    offer_reap(ctx, interactive=sys.stdin.isatty())
    if a.commit:
        # projects/<名> の削除は、git mv でステージ済み（消えたパスは pathspec にできない）
        commit_paths(ctx, [f"archives/{p.name}", f"areas/{p.area}"], f"[room] {p.name} を close し archives へ移動",
                     extra_allowed=(f"projects/{p.name}",))


# ---------- reap（閉じた Project が部屋に残した跡を、期限で片付ける） ----------

REAP_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")
HOME_HISTORY = "-home-ai"  # /home/ai を作業ディレクトリにしたときの会話履歴の名前


def find_reapable(ctx, today=None):
    """archives/ の Project のうち、reap_after が今日以前で、まだ reaped でないもの。[(名前, Area, reap_after)]。"""
    today = today or ctx.today()
    found = []
    for readme in sorted((ctx.vault / "archives").glob("*/README.md")):
        fm = read_frontmatter(readme)
        due = fm.get("reap_after", "")
        if fm.get("status") == "done" and due and due <= today and not fm.get("reaped"):
            found.append((readme.parent.name, fm.get("area", ""), due))
    return found


def reap_project(ctx, name, area):
    """部屋の中の、その Project の会話履歴と ~/tmp/<名> を消し、archives の README に reaped を付ける。消した、または対象が無ければ True。"""
    readme = ctx.vault / "archives" / name / "README.md"
    if not readme.exists():
        raise RoomError(f"archives/{name} が無い")
    if not REAP_NAME_RE.match(name):
        raise RoomError(f"{name}: 名前が英数字・_・- だけでないので、会話履歴のディレクトリ名を決められない。部屋の ~/.claude/projects/ と ~/tmp/ を手で確認して消す")
    distro = f"room-{area}"
    if distro not in ctx.wsl.distros():
        ctx.say(f"  {name}: 部屋 {distro} が無い。消すものは無いとして、reaped を付ける")
    else:
        hist, tmp = f"-mnt-room-{name}", name
        # Zed などで /home/ai を開くと、履歴は Project に紐づかない -home-ai に残る。どの Project のものか分からないので消さず、知らせる
        _rc, left, _err = ctx.wsl.script(distro, f'test -d "$HOME/.claude/projects/{HOME_HISTORY}" && echo remain || true\n')
        if left.strip():
            ctx.say(f"  警告: 部屋に {HOME_HISTORY}（/home/ai を開いたときの会話履歴）が残っている。Project に紐づかないので消さない。"
                    "内容を確認して、手で消す")
        script = (f'rm -rf -- "$HOME/.claude/projects/{hist}" "$HOME/tmp/{tmp}"\n'
                  f'ls -d "$HOME/.claude/projects/{hist}" "$HOME/tmp/{tmp}" 2>/dev/null || true\n')
        rc, out, err = ctx.wsl.script(distro, script)
        if rc != 0 or out.strip():
            raise RoomError(f"{name}: 消せなかった（{(err or out).strip()[-300:]}）")
    readme.write_text(update_frontmatter(readme.read_text(encoding="utf-8"), {"reaped": ctx.today()}),
                      encoding="utf-8", newline="\n")
    return True


def offer_reap(ctx, yes=False, interactive=True):
    due = find_reapable(ctx)
    if not due:
        return 0
    ctx.say(f"reap の期限が来ている Project（部屋の会話履歴と ~/tmp/<名> を消す。{len(due)} 件）:")
    for name, area, d in due:
        ctx.say(f"  {name}（room-{area}、期限 {d}）")
    if not yes:
        if not interactive:
            ctx.say("  → `room reap` で承認して実行する")
            return 0
        if input("消してよいか [y/N]: ").strip().lower() != "y":
            ctx.say("  → 見送った。`room reap` でいつでも実行できる")
            return 0
    done = 0
    for name, area, _d in due:
        reap_project(ctx, name, area)
        ctx.say(f"  消した: {name}")
        done += 1
    return done


def cmd_reap(ctx, a):
    if a.name:
        readme = ctx.vault / "archives" / a.name / "README.md"
        if not readme.exists():
            raise RoomError(f"archives/{a.name} が無い")
        fm = read_frontmatter(readme)
        if fm.get("status") != "done":
            raise RoomError(f"{a.name} は close されていない（status={fm.get('status')}）")
        if fm.get("reaped"):
            raise RoomError(f"{a.name} は reap 済み（{fm.get('reaped')}）")
        due = fm.get("reap_after", "")
        if due > ctx.today() and not a.force:
            raise RoomError(f"{a.name} の期限は {due}。前倒しなら --force")
        if not a.yes and input(f"{a.name} の会話履歴と ~/tmp を消してよいか [y/N]: ").strip().lower() != "y":
            raise RoomError("中止した")
        reap_project(ctx, a.name, fm.get("area", ""))
        ctx.say(f"消した: {a.name}")
        return
    if offer_reap(ctx, yes=a.yes) == 0:
        ctx.say("期限が来ていて、まだ消していない Project は無い")


# ---------- aws-key（部屋の ~/.aws/credentials に、Bedrock 用のキーを入れる） ----------

AWS_PROFILE_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
AWS_KEY_ID_RE = re.compile(r"^[A-Z0-9]{16,128}$")
AWS_SECRET_RE = re.compile(r"^\S{20,}$")
AWS_TOKEN_RE = re.compile(r"^\S{20,}$")


def aws_credentials_script(profile, body):
    """body（[profile] の節）で、~/.aws/credentials の同名の節を置き換える（ほかの節は残す。権限 600）。
    スクリプトは標準入力（sh -s）で渡し、body は引用つきのヒアドキュメントに埋める。引数で渡す（sh -c）と、wsl.exe の側のシェルが、スクリプト内で代入した変数（$f $x $t）を先に展開して空にし、touch "" で失敗する（$HOME は外側でも定義されているので展開される）。"""
    p = shlex.quote(f"[{profile}]")
    return (f"f=\"$HOME/.aws/credentials\"\n"
            "for x in \"$HOME/.aws\" \"$f\"; do [ ! -e \"$x\" ] || [ -O \"$x\" ] || "
            "{ echo \"所有者が一般ユーザーではない: $x（root のシェルで作った可能性。wsl -d <部屋> -u root -- chown -R ai:ai /home/ai/.aws で直す）\" >&2; exit 3; }; done\n"
            f"umask 077; mkdir -p \"$HOME/.aws\"; touch \"$f\"; chmod 600 \"$f\"\n"
            f"t=$(mktemp)\ncat > \"$t\" <<'ROOM_AWS_EOF'\n{body}ROOM_AWS_EOF\n"
            f"awk -v p={p} '/^\\[/{{s=($0==p)}} !s' \"$f\" > \"$f.new\" && cat \"$t\" >> \"$f.new\" && "
            f"mv \"$f.new\" \"$f\"; rm -f \"$t\"; chmod 600 \"$f\"")


def cmd_aws_key(ctx, a):
    """部屋の ~/.aws/credentials に、プロファイルのキーを入れる。秘密は画面に出さず、標準入力で部屋へ渡す（コマンドラインにも履歴にも残さない）。"""
    distro = f"room-{a.area}"
    if distro not in ctx.wsl.distros():
        raise RoomError(f"部屋が無い: {distro}。先に room init {a.area}")
    if not AWS_PROFILE_RE.match(a.profile):
        raise RoomError(f"プロファイル名が不正: {a.profile}（英数字、_ . - だけ）")
    key = ctx.ask("AWS_ACCESS_KEY_ID: ").strip()
    secret = ctx.ask_secret("AWS_SECRET_ACCESS_KEY（画面に出ない）: ").strip()
    token = ctx.ask_secret("AWS_SESSION_TOKEN（一時キーのときだけ。長期キーなら空のまま Enter）: ").strip()
    if not AWS_KEY_ID_RE.match(key):
        raise RoomError("AWS_ACCESS_KEY_ID の形が違う（英大文字と数字だけ、16 字以上）。何も書き込んでいない")
    if not AWS_SECRET_RE.match(secret):
        raise RoomError("AWS_SECRET_ACCESS_KEY の形が違う（空白なし、20 字以上）。何も書き込んでいない")
    if token and not AWS_TOKEN_RE.match(token):
        raise RoomError("AWS_SESSION_TOKEN の形が違う。何も書き込んでいない")
    body = f"[{a.profile}]\naws_access_key_id={key}\naws_secret_access_key={secret}\n" + (f"aws_session_token={token}\n" if token else "")
    rc, _out, err = ctx.wsl.script(distro, aws_credentials_script(a.profile, body))
    if rc != 0:
        raise RoomError(f"~/.aws/credentials に書けなかった（終了コード {rc}）: {err.strip()[-300:]}")
    ctx.say(f"書いた: {distro} の ~/.aws/credentials の [{a.profile}]（権限 600、{'一時キー' if token else '長期キー'}）。AI からは読める場所なので、"
            "Bedrock の権限だけのユーザーにし、予算アラートを置く。環境変数側は AWS_PROFILE=" + a.profile)


def cmd_shell(ctx, a):
    """部屋に入る。Windows の WSLENV に /p 付きのパスがあると、automount を切った部屋では、入るたびに「failed to translate」が出る。WSLENV を外して入る。"""
    distro = f"room-{a.area}"
    if distro not in ctx.wsl.distros():
        raise RoomError(f"部屋が無い: {distro}。先に room init {a.area}")
    ctx.wsl.shell(distro)


# ---------- main ----------

def build_parser():
    ap = argparse.ArgumentParser(prog="room", description="AI 作業部屋の操作（人が実行する。AI には実行させない）")
    ap.add_argument("--vault", default=os.environ.get("ROOM_VAULT") or str(Path.home() / "works"),
                    help="ワークスペースのルート（既定: $ROOM_VAULT か ~/works）")
    ap.add_argument("--reap-days", type=int, default=int(os.environ.get("ROOM_REAP_DAYS") or REAP_DAYS_DEFAULT),
                    help="close から reap までの日数（既定 14）")
    sub = ap.add_subparsers(dest="command", required=True)
    o = sub.add_parser("open", help="Project のひな形を作る")
    o.add_argument("name"); o.add_argument("--area", required=True)
    o.add_argument("--type", default="doc", choices=["doc", "dev", "dev-env", "dev-test", "research"])
    o.add_argument("--data", choices=DATA_MODES, help="データの扱い: none（マスクしない）/ mask（マスクだけ）/ restore（マスクして復元）。既定は none")
    o.add_argument("--boundary", help="Area に boundary: が無いときに付ける印")
    o.add_argument("--commit", action="store_true", default=True, help=argparse.SUPPRESS)  # 既定になったので不要（互換のため残す）
    o.add_argument("--no-commit", dest="commit", action="store_false", help="初期状態をコミットしない（既定はコミットする）")
    s = sub.add_parser("start", help="チェック → マウント → AI を起動 → アンマウント → 回収")
    s.add_argument("name")
    s.add_argument("--cmd", default="claude", help="部屋で実行するコマンド（既定: claude）")
    s.add_argument("--no-launch", action="store_true", help="起動せず、マウントしたまま待つ（Zed などで使う）")
    s.add_argument("--adopt", action="store_true", help="ai/in の現在のファイルを、この Project の入力として記録する")
    s.add_argument("--yes", action="store_true", help="mask.toml が変わったときの作り直しを確認しない")
    s.add_argument("--commit", action="store_true")
    m = sub.add_parser("mask", help="_noai/raw の原本をマスクして ai/in へ（start でも自動で行う）")
    m.add_argument("name"); m.add_argument("--yes", action="store_true")
    r = sub.add_parser("restore", help="ai/out を復元して _noai/final へ（start の終わりでも自動で行う）")
    r.add_argument("name"); r.add_argument("--force", action="store_true", help="人が変えた _noai/final も上書きする")
    rd = sub.add_parser("readme", help="ai/out/readme-draft.md を README.md の本文に反映する")
    rd.add_argument("name"); rd.add_argument("--yes", action="store_true"); rd.add_argument("--commit", action="store_true")
    st = sub.add_parser("stock", help="ai/out/stock/ の【汎用】の下書きを、確認を経て exmem/inbox/ に運ぶ")
    st.add_argument("name"); st.add_argument("--yes", action="store_true", help="確認を省く（印と対応表の点検は行う）")
    c = sub.add_parser("close", help="Area へ渡し、archives へ移す（ai/out/close.md が要る）")
    c.add_argument("name"); c.add_argument("--commit", action="store_true")
    i = sub.add_parser("init", help="Area の部屋（専用ディストロ）を作り、道具を入れる（ログインは人）")
    i.add_argument("area"); i.add_argument("--resume", action="store_true", help="作りかけの部屋に、設定と道具を入れ直す")
    i.add_argument("--ca-cert", help="部屋に入れる勤務先のルート証明書（PEM、最大5枚）。TLS 検査のあるネットワークで curl が証明書エラー（60）になるときに指定する。既定は入れない")
    i.add_argument("--boundary", help="Area が無い（または boundary: が無い）ときに付ける印（例: internal、顧客を表す名前。既定値は無い）")
    i.add_argument("--no-commit", dest="commit", action="store_false", default=True, help="Area の作成をコミットしない（既定はコミットする）")
    ak = sub.add_parser("aws-key", help="部屋の ~/.aws/credentials に、Bedrock 用のキーを入れる（入力は画面に出ない）")
    ak.add_argument("area"); ak.add_argument("--profile", required=True, help="プロファイル名（例: n1-trial）。同名の節は置き換える")
    sh = sub.add_parser("shell", help="部屋に入る（WSLENV を外すので「failed to translate」が出ない）")
    sh.add_argument("area")
    rp = sub.add_parser("reap", help="close から期限が来た Project の、部屋の会話履歴と ~/tmp/<名> を消す")
    rp.add_argument("name", nargs="?"); rp.add_argument("--yes", action="store_true")
    rp.add_argument("--force", action="store_true", help="期限前でも消す（名前を指定したとき）")
    u = sub.add_parser("umount", help="部屋に残ったマウントを外す")
    u.add_argument("--area", required=True)
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    sys.stdout.reconfigure(line_buffering=True)  # wsl の出力と、順序が前後しないように
    ctx = Ctx(a.vault, reap_days=a.reap_days)
    try:
        {"init": cmd_init, "aws-key": cmd_aws_key, "shell": cmd_shell, "reap": cmd_reap, "open": cmd_open, "start": cmd_start, "close": cmd_close, "umount": cmd_umount,
         "mask": cmd_mask, "restore": cmd_restore, "readme": cmd_readme, "stock": cmd_stock}[a.command](ctx, a)
    except RoomError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
