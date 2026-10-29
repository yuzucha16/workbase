---
type: explain
title: なぜ Python の版を uv 管理にそろえるのか（OS 管理との違いと、落ちたときの考え方）（理解ガイド）
tags:
  - python
  - tool/uv
triggers: [Python の版, OS の Python, uv の Python, 版をそろえる, python3 と python, uv が止まる, python が使えない, requires-python]
---

# なぜ Python の版を uv 管理にそろえるのか（理解ガイド）

workbase の .py を、Windows・WSL・クラウドで動かしていると、「ある場所では動くが別の場所では動かない」が起きる。原因の多くは Python の版の違いなので、版を 1 か所にそろえる。その理由と、uv が使えないときの考え方。

## 2 種類の Python

| 種類 | 例 | 版が変わる時 |
|---|---|---|
| OS 管理 | WSL の `python3`（apt）、Windows の `python` | OS の更新で、気づかないうちに |
| uv 管理 | `uv run room.py`、`uv run --script` が使う Python | `.python-version` や `requires-python` を書き換えたとき |

OS 管理の Python は、入れた覚えのない版が使われる。uv 管理は、書いた版が使われ、戻せる。

## 正本は 1 か所

`workflow-kit/room/.python-version`（今は 3.13.14）が正本。WSL の `python3` も、`room init` で同じ版を uv で入れて合わせる（案。未実装）。各 .py の `requires-python` は `==3.13.*` にする。

## 落ちたとき

- uv が止まった（Windows が実行を一時的に止める、ネットワークで取得できない）: 標準ライブラリだけの .py は、OS の `python` で動かしてよい。版は近いので、たいてい動く。揃っていないことは承知の上の緊急用。
- 依存つき（`pywin32` など）の .py は、代替が無い。uv の復旧を待つ。
- 古い版が要るモジュールがある: そのスクリプトだけ、先頭の `requires-python` に別の版を書く。

## 迷ったら

- 版の違いを疑う前に、`python --version`（WSL は `python3 --version`）と `.python-version` を見比べる。
- 規則の表は `workflow-kit/script-guide.md` の「Python の版と呼び方」、判断の根拠は `docs/decisions.md`（2026-10-29）、ナレッジは [[python-version-uv-canonical]]。
