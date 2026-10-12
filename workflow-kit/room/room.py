"""room: AI 作業部屋の操作（open / start / close / umount）。

人が Windows で実行する。AI には実行させない（原本と対応表を読む工程を含むため）。
設計は guides/explain/ai-room-why.md、手作業の手順は guides/howto/ai-room-setup.md。
標準ライブラリだけで動く。起動は `uv run room.py <command>`。
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path

MOUNT_ROOT = "/mnt/room"
ROOM_UID = 1000
REAP_DAYS_DEFAULT = 14
GITIGNORE_REQUIRED = ("**/_noai/", "!**/ai/out/")
AI_DIRS = ("ai/docs", "ai/in", "ai/work", "ai/out", "ai/records", "_noai/raw", "_noai/map", "_noai/final")
AI_KEEP = ("ai/in", "ai/work", "ai/records")


class RoomError(Exception):
    pass


# ---------- 外部コマンド ----------

class Wsl:
    """wsl.exe の呼び出し。コマンドは標準入力で、LF 固定で渡す（CRLF だと umount などが壊れる）。"""

    def distros(self):
        raw = subprocess.run(["wsl.exe", "-l", "-q"], capture_output=True).stdout
        text = raw.replace(b"\x00", b"").decode("utf-8", "ignore")
        return [l.strip() for l in text.splitlines() if l.strip()]

    def script(self, distro, text, root=False):
        cmd = ["wsl.exe", "-d", distro] + (["-u", "root"] if root else []) + ["--", "sh", "-s"]
        r = subprocess.run(cmd, input=text.replace("\r\n", "\n").encode("utf-8"), capture_output=True)
        return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")

    def interactive(self, distro, command):
        """端末をつないだまま、一般ユーザーで実行する。"""
        return subprocess.run(["wsl.exe", "-d", distro, "--", "bash", "-ic", command]).returncode


def git(vault, *args, check=True):
    r = subprocess.run(["git", "-C", str(vault), *args], capture_output=True)
    out = r.stdout.decode("utf-8", "replace")
    if check and r.returncode != 0:
        raise RoomError(f"git {' '.join(args)} が失敗した: {r.stderr.decode('utf-8', 'replace').strip()}")
    return out


class Ctx:
    def __init__(self, vault, wsl=None, today=None, now=None, say=print, reap_days=REAP_DAYS_DEFAULT, settle=3):
        self.vault = Path(vault)
        self.wsl = wsl or Wsl()
        self._today = today
        self._now = now
        self.say = say
        self.reap_days = reap_days
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
        p.area = p.fm.get("area")
        if not p.area:
            raise RoomError(f"{p.readme} の frontmatter に area: が無い")
        return p

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


def commit_paths(ctx, paths, message, extra_allowed=()):
    git(ctx.vault, "add", "-A", "--", *paths)
    staged = [l for l in git(ctx.vault, "diff", "--cached", "--name-only").splitlines() if l]
    if not staged:
        ctx.say("コミットする変更が無い")
        return
    allowed = tuple(p.rstrip("/") + "/" for p in (*paths, *extra_allowed))
    stray = [f for f in staged if not f.startswith(allowed)]
    if stray:  # 並行する作業のステージ済みの変更を、巻き込まない
        raise RoomError("対象外のファイルがステージされている。コミットしない:\n  " + "\n  ".join(stray))
    ctx.say("ステージ済み: " + str(len(staged)) + " ファイル")
    git(ctx.vault, "commit", "-m", message)
    ctx.say("コミットした: " + git(ctx.vault, "log", "--oneline", "-1").strip())


# ---------- open ----------

README_TEMPLATE = """---
status: active
area: {area}
type: {type}
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
    for d in AI_DIRS:
        (p.dir / d).mkdir(parents=True, exist_ok=True)
    for d in AI_KEEP:
        (p.dir / d / ".gitkeep").write_text("", encoding="utf-8")
    p.readme.write_text(README_TEMPLATE.format(area=a.area, type=a.type, today=ctx.today(), name=a.name),
                        encoding="utf-8", newline="\n")
    entry = f"- [[projects/{a.name}/README|{a.name}]]（{ctx.today()} 開始）"
    area_readme.write_text(add_area_entry(area_readme.read_text(encoding="utf-8"), "## 進行中の Project", entry),
                           encoding="utf-8", newline="\n")
    log_room(ctx, p, "open", "area 一致、boundary あり", "ひな形を作成")
    if p.distro not in ctx.wsl.distros():
        ctx.say(f"注意: 部屋（{p.distro}）がまだ無い。guides/howto/ai-room-setup.md の 3 章で作る")
    ctx.say(f"作った: projects/{a.name}（ai/ と _noai/）。README の <...> を埋める")
    if a.commit:
        commit_paths(ctx, [f"projects/{a.name}", f"areas/{a.area}"], f"[room] {a.name} を open（Area {a.area}）")


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


def snapshot_readme(p):
    ctx_dir = p.ai / "ctx"
    ctx_dir.mkdir(parents=True, exist_ok=True)
    dst = ctx_dir / "README.md"
    if dst.exists():
        os.chmod(dst, stat.S_IWRITE | stat.S_IREAD)
    shutil.copyfile(p.readme, dst)
    os.chmod(dst, stat.S_IREAD)


def cmd_start(ctx, a):
    p = Project.load(ctx, a.name)
    boundary = preflight(ctx, p)
    if a.adopt:
        n = adopt_in(ctx, p)
        ctx.say(f"ai/in の {n} ファイルを、この Project の入力として manifest に記録した")
    problems = check_provenance(p)
    if problems:
        raise RoomError("来歴チェックに失敗した:\n  " + "\n  ".join(problems)
                        + "\n（人が確認したファイルなら、--adopt で記録する）")
    checks = f"area 一致、boundary={boundary}、in {len(in_files(p))} 件の来歴 OK"
    snapshot_readme(p)
    ctx.say(f"チェック OK（{checks}）")
    result = "不明"
    try:
        mount(ctx, p)
        ctx.say(f"マウントした: {p.mount_point}")
        if a.no_launch:
            ctx.say("--no-launch: ここで AI を起動しない。Zed などで WSL リモート接続し、終わったら Enter")
            input()
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
    if a.commit:
        commit_paths(ctx, [f"projects/{p.name}"], f"[room] {p.name}: start {ctx.now()}")


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


def cmd_close(ctx, a):
    p = Project.load(ctx, a.name)
    if p.fm.get("status") != "active":
        raise RoomError(f"Project が active でない: status={p.fm.get('status')}")
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
    if a.commit:
        # projects/<名> の削除は、git mv でステージ済み（消えたパスは pathspec にできない）
        commit_paths(ctx, [f"archives/{p.name}", f"areas/{p.area}"], f"[room] {p.name} を close し archives へ移動",
                     extra_allowed=(f"projects/{p.name}",))


# ---------- main ----------

def build_parser():
    ap = argparse.ArgumentParser(prog="room", description="AI 作業部屋の操作（人が実行する。AI には実行させない）")
    ap.add_argument("--vault", default=os.environ.get("ROOM_VAULT") or str(Path.home() / "works"),
                    help="Vault のトップ（既定: $ROOM_VAULT か ~/works）")
    ap.add_argument("--reap-days", type=int, default=int(os.environ.get("ROOM_REAP_DAYS") or REAP_DAYS_DEFAULT),
                    help="close から reap までの日数（既定 14）")
    sub = ap.add_subparsers(dest="command", required=True)
    o = sub.add_parser("open", help="Project のひな形を作る")
    o.add_argument("name"); o.add_argument("--area", required=True)
    o.add_argument("--type", default="doc", choices=["doc", "dev", "research"])
    o.add_argument("--boundary", help="Area に boundary: が無いときに付ける印")
    o.add_argument("--commit", action="store_true")
    s = sub.add_parser("start", help="チェック → マウント → AI を起動 → アンマウント → 回収")
    s.add_argument("name")
    s.add_argument("--cmd", default="claude", help="部屋で実行するコマンド（既定: claude）")
    s.add_argument("--no-launch", action="store_true", help="起動せず、マウントしたまま待つ（Zed などで使う）")
    s.add_argument("--adopt", action="store_true", help="ai/in の現在のファイルを、この Project の入力として記録する")
    s.add_argument("--commit", action="store_true")
    c = sub.add_parser("close", help="Area へ渡し、archives へ移す（ai/out/close.md が要る）")
    c.add_argument("name"); c.add_argument("--commit", action="store_true")
    u = sub.add_parser("umount", help="部屋に残ったマウントを外す")
    u.add_argument("--area", required=True)
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    sys.stdout.reconfigure(line_buffering=True)  # wsl の出力と、順序が前後しないように
    ctx = Ctx(a.vault, reap_days=a.reap_days)
    try:
        {"open": cmd_open, "start": cmd_start, "close": cmd_close, "umount": cmd_umount}[a.command](ctx, a)
    except RoomError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
