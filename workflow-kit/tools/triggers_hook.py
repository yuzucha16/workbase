#!/usr/bin/env python3
"""UserPromptSubmit フック用: 依頼文に当たる知識（triggers:）を、作業中の AI の文脈に出す。

Claude Code が標準入力に渡す JSON の "prompt" を読み、`find_knowledge.py --triggers` と同じ照合をして、
当たったノートの一覧を標準出力へ出す（標準出力は AI の文脈に足される）。当たらないとき・読めないときは何も出さず、常に終了コード 0。
配線（settings.json の hooks）は dotfiles 側。このリポジトリは、このスクリプトと点検だけを持つ。

試験: echo '{"prompt":".bat を作りたい"}' | python -I workflow-kit/tools/triggers_hook.py
"""
import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path

MAX_PROMPT = 4000  # 先頭だけ照合する


def main():
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        prompt = str(json.load(sys.stdin).get("prompt", ""))[:MAX_PROMPT]
        if len(prompt.strip()) < 4:
            return 0
        here = Path(__file__).resolve().parent
        spec = importlib.util.spec_from_file_location("find_knowledge", here / "find_knowledge.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            mod.lookup_triggers(here.parent.parent, prompt, 5)
        out = buf.getvalue().strip()
        if out and not out.startswith("該当なし"):
            print("[作業の言葉の索引] 依頼文に当たる知識（作業の前に読む。語は triggers: との一致）:\n" + out)
    except Exception:
        pass  # 失敗しても依頼を止めない
    return 0


if __name__ == "__main__":
    sys.exit(main())
