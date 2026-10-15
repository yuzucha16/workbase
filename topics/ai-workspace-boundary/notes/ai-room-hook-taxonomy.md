# フックの整理: 運用コマンド（room）と AI 行動フック

- 作成: 2026-10-13（モバイルのセッションでの議論）。状態: **整理の提案**。ユーザーの課題認識: 「ルーム向けのフック（`room start`）と AI 行動のフック（`init` `start` など）がごっちゃになっている」。
- 前提: [[ai-room-handover]]、`docs/log.md`（決定は `docs/decisions.md`、経緯は `docs/log-history.md`）（決定4: 人が言うコマンドは `room open` / `room start` / `room close`）。

## 何がごっちゃか

1. **同じ名前が2つある**: `open` `start` `close` が、AI 行動フック（kit の手順書）と `room` のコマンドの両方にある。
2. **役割が重なる**: Project のひな形作りが、kit の `open`（AI が README などを作る）と `room open`（スクリプトが README と `ai/` を作る）の両方にある。
3. **呼ぶ場所が違うのに同じ言葉で話している**: `room` は端末で人が打つ。AI 行動フックはチャットで合言葉を言う。

## 分け方（提案）

| | 運用コマンド（`room`） | AI 行動フック（kit） |
|---|---|---|
| 呼ぶ人・場所 | 人。Windows の端末 | 人が言い、AI が実行。チャット（部屋の AI、または Vault 側の AI） |
| 性質 | 決まった手順の副作用（マウント、コピー、移動、コミット） | 判断（インタビュー、確認、振り分け、下書き） |
| 実行者 | スクリプト（AI には実行させない） | AI（手順書を読んで実行） |
| 名前 | `room <動詞>` と必ず前置きする | 合言葉（日本語の別名を主に使う: 「作業を始めて」「終了処理して」） |
| 正本 | `workflow-kit/room/README.md` | `workflow-kit/hooks.md` |

## 時間の流れで見ると、入れ子になる

```
room open        ひな形の作成（副作用）
  └ [部屋の AI] open の判断部分（目的・完了条件の聞き取り）  ← 下の論点1
room start       準備（チェック、写しの送付、マウント）→ AI を起動
  └ [部屋の AI] start（開始インタビュー）→ 作業 → wrap（現在状態の更新、下書き）
                 回収（アンマウント、復元、Area への転記、コミット）
room close       最後の回収
  └ [部屋の AI] close の判断部分（完了条件、暫定の見直し、振り分け）→ ai/out/close.md
                 副作用（状態の更新、archives への移動、reap の印）
```

つながりは **ファイルの受け渡し** だけにする（これが2層の契約）。

| 向き | 受け渡し |
|---|---|
| スクリプト → AI | `ai/ctx/`（README の写し、workbase の写し）、`ai/in/`（マスク済みの入力）、部屋の `AGENTS.md` |
| AI → スクリプト | `ai/out/close.md`（close の判断）、`ai/out/stock/`（【汎用】の下書き）、`ai/docs/decisions.md` の【案件】ラベル（Area への転記） |

## AI 行動フックの置き場所（どこで動くか）

| フック | 動く場所 | 部屋との関係 |
|---|---|---|
| `start` `wrap` | 部屋の中 | `room start` が起動する。`docs/` は `ai/docs/` |
| `open` `close` | 部屋の中（判断部分だけ） | 副作用は `room open` / `room close` が行う |
| `stock` | 部屋の中は下書きまで | 運び先（`exmem/inbox/`）は人の門を通る |
| `integrate` `review` | Vault 側（workbase の作業） | 部屋の外。`integrate` が rebase の解決を担当 |
| `init` | Vault 側 | ワークスペースへの導入。部屋の作成は別（下の論点2） |

## 論点の結果（2026-10-13、ユーザーの「フックの整理をお願い」を受けて実施）

| 論点 | 結果 |
|---|---|
| 1 README の書き手 | 下書き方式で実装: AI が `ai/out/readme-draft.md`（本文だけ）を書き、人が `room readme <名>` で反映（`room.py`、テスト2件） |
| 2 部屋の作成 | `room init <Area>` は**未実装**。実際の WSL が要るので PC のセッションで（`wsl --import`、`wsl.conf`、一般ユーザー `ai`、道具、`~/CLAUDE.md` から `~/shared/ROOM.md` への案内） |
| 3 名前の衝突 | `hooks.md` に「運用コマンド」の節を足した。`room` を前置する決まりは `room-context.md` |
| 4 手順書の読み替え | 手順書の本文は変えず、`workflow-kit/room-context.md` に差分（`docs/` → `ai/docs/`、分担、受け渡しのファイル）を集めた |
| 5 手順書の渡し方 | ロードマップ2番で実装済み（`~/shared`、`ROOM.md`） |

## 論点（決めること）（以下は整理前の記述）

1. **README の書き手**: Project の `README.md`（目的・完了条件）は Vault が正本で、部屋の AI からは読み取りの写し（`ai/ctx/`）しか見えない。kit の `open`（AI が README を作る）は、そのままでは動かない。案: `room open` が人に聞く（目的・完了条件）、または AI が `ai/out/readme-draft.md` に下書きして、`room` が反映する（`close.md` と同じ形）。**推奨: 後者**（AI の判断と副作用の分担が `close` と揃う）。
2. **部屋の作成**: 部屋専用のディストリビューションの作成（`wsl.conf`、一般ユーザー、道具、ログイン）を、どのコマンドにするか。案: `room init <Area>`（新設）。kit の `init` は Vault への導入のままにして、手順書の中で「部屋が要るなら `room init`」と案内する。
3. **名前の衝突の扱い**: 決定4は変えない（`room open/start/close`）。会話と文書では、運用コマンドは必ず `room` を前置し、AI 行動フックは日本語の別名で呼ぶ決まりにする。`hooks.md` に「運用コマンド」の節を足し、2つの表を分ける。
4. **kit の手順書の読み替え**: `start` `wrap` `close` `open` の手順書が `docs/` を Project 直下と想定している。部屋の中の読み替え（`ai/docs/`）と、「AI が行う部分・人（スクリプト）が行う部分」の分担を、手順書に書く。
5. **部屋の AI への手順書の渡し方**: ワークスペースの `AGENTS.md` は `resources/workflow-kit` を指すが、部屋からは見えない。写し（[[ai-room-shared-knowledge-sync]] の方式 A）を `~/shared` に置き、部屋の `AGENTS.md` からそこを指す。
