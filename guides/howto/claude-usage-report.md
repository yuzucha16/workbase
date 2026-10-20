---
type: howto
title: Claude Code の使用量を週次・月次で振り返る（usage_report）
tags:
  - ai/claude
  - windows
---

# Claude Code の使用量を週次・月次で振り返る（`usage_report`）

Claude Code のセッションログ（JSONL）から、トークン使用量と概算費用($)を集計する手順書。ターミナルに出す `usage_report.py` と、1枚の HTML にする `usage_report_html.py` がある。どちらも読み取り専用で、外部には通信しない。

- **ゴール（完了の目安）**: 週次または月次の合計・1セッション当たりの平均/最大/最小・上位セッションが見え、HTML をブラウザで開ける
- 範囲: 実行のしかた、見方、単価表の足し方、突合。設計の経緯は `topics/usage-viz/records/usage-viz-*.md`
- 置き場: `workflow-kit/tools/`（`usage_report.py`、`usage_report_html.py`、`usage_prices.json`）。Python 3 の標準ライブラリだけで動く
## 対応バージョン表

| 項目 | 確認したもの | 確認日 |
|---|---|---|
| 実機 | Windows 11、Python 3.13、Claude Code 2.1.300、ccusage（`@latest`） | 2026-10-20 |
| ログの形式 | `~/.claude/projects/**/*.jsonl` の `message.usage`（Claude Code 内部の形式。変わる可能性があり、公式に固定されていない） | 2026-10-20 |
| 単価 | 公式の料金ページ（4章） | 2026-10-20 |

## 1. 測定（ターミナルに表示）

リポジトリのルート（`$HOME\works\resources`）で実行する。

```powershell
# 週次、直近4週、上位5件（トークン数のみ）
python workflow-kit/tools/usage_report.py

# 月次、直近3か月、上位10件、費用つき
python workflow-kit/tools/usage_report.py --by month --last 3 --top 10 --prices workflow-kit/tools/usage_prices.json

# 費用の高い順に並べる（--prices が必須）
python workflow-kit/tools/usage_report.py --sort cost --prices workflow-kit/tools/usage_prices.json

# 出力トークン（実際に書かせた量）の多い順に並べる
python workflow-kit/tools/usage_report.py --sort output
```

| オプション | 意味 | 既定 |
|---|---|---|
| `--by week\|month` | 期間の単位（週は月曜始まり、ローカル時刻） | week |
| `--last N` | 直近 N 期間だけ出す | 4 |
| `--top N` | 期間ごとのランキング件数 | 5 |
| `--sort total\|output\|cost` | ランキングの基準 | total |
| `--prices FILE` | 単価表（JSON）。渡したときだけ費用を出す | なし |
| `--root DIR` | ログの場所 | `~/.claude/projects` |

## 2. HTML 化

単価表は、スクリプトの隣の `usage_prices.json` を自動で読む（`--prices` は不要）。

```powershell
# 週次、直近4週、上位10件 → ~/usage-report.html
python workflow-kit/tools/usage_report_html.py

# 月次、直近6か月
python workflow-kit/tools/usage_report_html.py --by month --last 6

# 出力先を指定して、ブラウザで開く
python workflow-kit/tools/usage_report_html.py --out $HOME/usage-weekly.html
Invoke-Item $HOME/usage-weekly.html
```

- 内容は2部。**概要**（最新の期間のカード、期間ごとの推移、気づき）と、**詳細・分析**（トークン種別の内訳と費用、1件当たりの平均/中央値/最大/最小、セッションの大きさの分布、モデル別、プロジェクト別、上位セッション）。
- 出力先の既定は `~/usage-report.html`。**リポジトリの中に置かない。** 題名（最初の発言）とプロジェクト名に作業内容の断片が入るので、公開リポジトリに載せない。

## 3. 見方

- トークンの合計は、**キャッシュ読取が9割以上**を占める。`--sort total` は、長く続いた会話が上位になる。
- 実際に書かせた量は `--sort output`、お金の重さは `--sort cost`。費用ではキャッシュ読取より、キャッシュ作成と出力が効く（2026-10-19 の週は、作成44%、読取29%、出力27%）。
- キャッシュ読取率 = 読取 ÷（入力 + 読取 + 作成）。低いセッションは、キャッシュが効いていない。
- 最新の期間は集計の途中なので、前の期間より少なく出る。ログは使っている間も増え続ける。

## 4. 単価表を足す・更新する

単価表は `workflow-kit/tools/usage_prices.json`。単価は改定されるので、使う前に取得日を見る。

1. 公式の料金ページ（<https://platform.claude.com/docs/en/about-claude/pricing>）の表を開く。単位は USD / 100万トークン。
2. モデル ID の行を足す。キーはログの `model` の**前方一致**（例: `claude-sonnet-5-5`）。

   ```json
   "claude-sonnet-5-5": {"input": 2, "output": 10, "cache_read": 0.1, "cache_write": 2.5, "cache_write_1h": 4}
   ```

   | キー | 公式の表の列 |
   |---|---|
   | `input` | Base input tokens |
   | `output` | Output tokens |
   | `cache_read` | Cache hits and refreshes |
   | `cache_write` | 5m cache writes |
   | `cache_write_1h` | 1h cache writes |

3. `_source`（出典 URL）と `_retrieved`（取得日）を更新する。`_` で始まるキーは注記で、集計には使わない。
4. 単価表に無いモデルは、費用が 0 として扱われる（トークンは数える）。新しいモデルを使い始めたら足す。
5. 注意: Haiku 5.5 は、10万トークン超のプロンプトが別単価（表には10万以下の値を入れている）。US 限定の推論（`inference_geo`）は全体が1.1倍になるが、表には反映していない。

別の単価表で試すときは `--prices 別のファイル.json` を渡す。

## 5. 突合（ccusage と比べる）

```powershell
npx --yes ccusage@latest daily --json --since 20261019
```

2026-10-20 の確認では、10-19 以降の合計トークンが 79,675,204 で完全に一致し、概算費用は $26.17（ccusage は $26.175）だった。差が出るときは、次のどれかを疑う。

- 集計した時刻が違う（ログが増えている）。同じ時点で2つとも実行する。
- 期間の切り方が違う。ccusage の `daily` は日単位。
- 単価表が古い。

## 6. 数え方

- 1つの API 応答は JSONL の複数行に同じ usage で繰り返される。`message.id` と `requestId` で1回だけ数える。
- サブエージェントのログ（`subagents/`）は、親と同じ `sessionId` に含める。
- 期間は各応答の時刻で決める。期間をまたぐセッションは、期間ごとに分かれて数える。

## 7. うまくいかないとき

| 症状 | 原因と対処 |
|---|---|
| 日本語が文字化けする | `$env:PYTHONIOENCODING='utf-8'` を設定する。`python -I` は環境変数を無視するので付けない |
| `ログの場所が無い` | `--root` で `.claude/projects` の場所を渡す（WSL なら `/mnt/c/Users/<ユーザー名>/.claude/projects`） |
| 費用が `—` や 0 になる | `--prices` を付けたか、単価表にそのモデルがあるかを見る |
| `--sort cost には --prices が要る` | `--prices workflow-kit/tools/usage_prices.json` を付ける |
