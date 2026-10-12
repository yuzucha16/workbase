# 次のステップ: AI 作業部屋

前提と決定は [[ai-room-handover]]。詳細は [[ai-room-design]]。ここは PC のセッションで行う順序。各段階の終わりに、実測の結果を残して、次へ進むか判断する。

## 0. 反映の方針を決める（ユーザーに確認）

- 検討の結果を、どこに残すか。案: 決定と理由は `exmem/lessons/` の新しいノート（例: `ai-workspace-boundary.md`）、手順は `workflow-kit/`（新しいフック）、ワークスペースの規約は雛形（`workflow-kit/templates/workspace/`）。ノートの形式は `exmem/AGENTS.md` に従う。
- 検証は、まず使い捨ての Project で行う。実データは使わない。

## 1. 実機で確かめる（スパイク。作る前に、成立を確かめる）

| # | 確かめること | 合格の目安 |
|---|---|---|
| S1 | 部屋専用の WSL ディストリビューションを作る（`wsl --install` または `wsl --import`）。`/etc/wsl.conf` に `automount.enabled=false`、`interop.enabled=false`（`appendWindowsPath=false`）を書き、再起動する | `ls /mnt` に C: が無い。`cmd.exe` を起動できない |
| S2 | `automount` を切ったまま、`/etc/fstab` で Vault の `projects/<テスト>/ai/` **だけ**を drvfs でマウントできるか（`automount.mountFsTab` の挙動も） | 指定したフォルダだけが見える。親のフォルダは見えない |
| S3 | 部屋の中で Claude Code を導入し、ログインして、テストファイルを読み書きする。Windows の Excel で同じファイルを開いて、同時に編集しないことを確かめる | 動く。ロックなどの問題が無い |
| S4 | Zed で部屋のフォルダを WSL として開く。Zed の Claude Agent が WSL 側で動くか。動かなければ、Zed のターミナルで `wsl -d <部屋> claude` を使えるか | どちらかで使える |
| S5 | `openpyxl` で、ピボットとマクロを含む xlsx を読み書きして、壊れないか（ピボットは新規作成できない前提で、保持を確かめる）。シート名・コメント・プロパティ・隠しシート・名前の定義・外部リンク・ピボットのキャッシュに、マスク前の値が残る箇所を洗い出す | 残る箇所の一覧ができる |
| S6 | マウントしたフォルダの性能（Python で xlsx の読み書き、`rg`、`git` を使わない前提）と、ファイルの権限（`in/` を読み取り専用にできるか） | 作業に耐える |

S1・S2 が成立しなければ、案Yの形を見直す（代替: Windows 側の別フォルダを `\\wsl.localhost` 経由で受け渡す。前の「共有フォルダ」の節を参照）。

## 2. 未決を決める（ユーザーに確認。1つずつ）

1. 部屋の単位: Project ごと（P1）でよいか。
2. スクリプトの言語と実行場所: Windows 側の Python 1本（P2）でよいか。Windows に Python（`uv` など）を入れてよいか。
3. 共有フォルダの置き場: Vault の中の `projects/<名>/ai/`（P3）か、Vault の外か。Project の `docs/` を `ai/docs/` に移してよいか。
4. コマンドの名前と構成: `room open` / `room start` / `room close`（P4）か、既存のフック名（`open` `start` `close`）に寄せるか。
5. Area への同期: 郵便受け（P5）でよいか。
6. マスクの規則: プレースホルダーの形式（例: `⟦CUST_001⟧`）、マスクしない列（数値の扱い）の指定方法、xlsx の隠れた情報の消し方。
7. reap の期限（14日は仮）。
8. 前の `_noai/` の deny 設定（Claude Code の `Read(_noai/**)`）を、Vault 側の安全網として残すか（既定は、全部屋にするので不要。ただし Vault 側で workbase の作業中に誤って読むのを防ぐ意味はある）。
9. Codex・Copilot の対応: 部屋の中で動かせば同じ境界が効く。追加の設定が要るか。

## 3. スクリプト（`room`）の最小版を作る

1. `room open`: Project のひな形（`README.md`、`ai/{docs,in,work,out,records}`、`_noai/{raw,map,final}`）と、`.gitignore`（`**/_noai/`）、Area の一覧の更新。
2. `room start` の fork 部: `_noai/raw/` の新しいファイルをマスクして `ai/in/` へ（csv と xlsx）。マスクの対応表を `_noai/map/` へ。部屋の規約（`AGENTS.md` / `CLAUDE.md`）と設定を生成。manifest（ハッシュ、版）を `ai/records/` へ。マスク漏れの点検（対応表の語が残っていないか）。
3. `room start` の exec 部: ディストリビューションの起動、`ai/` のマウント、Claude Code の起動。
4. `room start` の wait 部（回収）: `ai/out/` の成果物の復元（プレースホルダー → 実データ）→ `_noai/final/`、戻らなかったプレースホルダーの一覧（あれば止める）、【案件】の項目を Area の `inbox.md` へ、manifest の更新、コミット。
5. `room close`: 最後の回収、`README.md` の状態の更新、アンマウント、`archives/` への移動（追跡する部分はファイル単位の `git mv`。`_noai/` も一緒に移す）、zombie の印（`reap_after`）、reap。
- 先に、手作業でこの流れを1巡して（S1〜S6 の環境で）、どこが重いかを測ってからスクリプトにする。

## 4. workflow-kit に組み込む

- 新しい手順書（`room-hook.md` など）と `hooks.md` の呼び出し表への追加。既存の `open` / `start` / `wrap` / `close` との関係の整理（部屋の中で AI が行うのは判断の部分、副作用は `room` が行う）。
- ワークスペースの雛形の更新: `AGENTS.md`（AI は部屋で使う、Vault 側で Project の作業をしない、`_noai/` と `works-secret` の扱い）、`gitignore.template`（`**/_noai/`）。`init` の手順に、部屋専用のディストリビューションの用意を足す。
- 規約: AI が書くスクリプトは、入力のパスを明示する。部屋の `AGENTS.md` で、`in/` と `ctx/` を変えない、プレースホルダーをそのまま残すと定める。
- 共有側に、会社固有の情報（実際の Project 名、顧客名）を書かない。

## 5. 1つの Project で試す

- 実際の Project 1つを、`room open` から `room close` まで1巡する。測るもの: 手数、マスクの漏れ、復元の失敗、ピボットのキャッシュ、点在（ファイルが散らばっていないか）、作業記録で再現できるか。
- 結果で、P1〜P8 と workflow-kit の手順を直す。安定したら、他の Project へ展開する。

## 6. 後回し（別の論点）

- `areas/dev-env/certs` など、いま Vault の中にある鍵・証明書の `works-secret` への移し替え。
- 対応表の保護（Vault の中の private 領域の扱い。今回の AI 分離とは別の論点とした）。
- Obsidian で使う AI プラグインの扱い（部屋の外にいるので、機密を扱う Project には使わない決まりにする）。
- Codex・Copilot の個別の設定。
