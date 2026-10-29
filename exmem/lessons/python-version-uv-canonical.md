---
type: knowledge
title: Python の版は uv 管理を正本にして揃える（呼び方と落ち方）
status: active
tags:
  - tool/uv
  - python
  - windows
aliases:
  - python-version-uv-canonical
triggers: [Python の版, python3, uv run, uv python, requires-python, .python-version, 版の固定, uv が使えない, python が使えない, 呼び方]
created: 2026-10-29
updated: 2026-10-29
sources:
  - Claude Code conversation "Count python and uv run calls in workbase" (2026-10-29)
---

# Python の版は uv 管理を正本にして揃える（呼び方と落ち方）

## Principles

- Python は版に敏感なので、版は uv 管理の 1 か所（`workflow-kit/room/.python-version`）を正本にする。トラブル時に「版の違いが原因か」を疑う段を減らし、ダウンタイムを短くする。
- OS 管理の Python（WSL の `python3`、Windows の素の `python`）は、更新で気づかないうちに版が変わる。戻せない。uv の固定は、書き換えたときだけ変わり、戻せる。
- 揃える範囲は、差が出やすいもの（依存つき、文字コード、room 本体）だけ。標準ライブラリだけの .py に厳密さは求めない。

## Decisions

- 呼び方（`docs/decisions.md` 2026-10-29）: Windows は依存つき `uv run --script`、room は `uv run room.py`。uv が止まったときだけ OS の `python`（標準ライブラリだけの .py。版は保証しない）。WSL は `python3`（正本と同じ版を uv で入れる。`room init` の段は未実装）。PC2・クラウドの AI は `python -I`（対象外）。
- 各 `.py` の `requires-python` は `==3.13.*`。下限指定（`>=`）だと、uv が新しい版を選んで正本とずれる。
- 古い版が要るモジュールを使うスクリプトだけ、`requires-python` に別の版を書く（スクリプトごとに選ばれる）。

## Gotchas

- 【汎用】`uv python install` は uv の置き場に入れるだけで、`python3` の名前では呼べない。呼ぶには別名（`--default`）か PATH が要る（実機で未確認）。Ubuntu のシステムの `python3` は apt の道具が使うので上書きしない。
- 【汎用】`python -I` は PYTHONIOENCODING を無視するので、Windows で人が叩く手順には付けない。
- 【汎用】`uv run`（プロジェクト内）は近くの `pyproject.toml` の環境を使い、`uv run --script` は .py の先頭の依存情報だけを使う。
- 【汎用】Windows の `python3` はストアの代替実行（スタブ）に当たることがある。Windows の手順は `python` にする。
- 【この件】uv の Python の取得は、ネットワークと社内の証明書に依存する（未確認）。止まったら、標準ライブラリだけの .py は OS の `python` で動かす。

## Open Questions

- WSL で uv の Python を `python3` として呼ぶ方法（`--default` か `~/.local/bin`）。
- 勤務先のネットワークで `uv python install` が通るか。
