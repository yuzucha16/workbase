# 引き継ぎ: AI 作業部屋（AI に見せる領域の境界）

- **これは最初の引き継ぎ（2026-10-12 時点の背景と決定）。最新の入口は [[ai-room-start-here]]、状態の正本は `docs/log.md`。**
- 作成: 2026-10-12（モバイルのセッションでの検討の終了時）。
- 読む順: この文書 → `docs/log.md`（決定は `docs/decisions.md`、経緯は `docs/log-history.md`） → 必要なら [[ai-room-design]]（詳細）と [[ai-boundary-design]]（初期の案と、その見直し）。
- 状態: 設計の叩き台まで。**リポジトリにも、ワークスペース（ルート）にも、まだ何も反映していない**。公式文書の調査はしたが、実機での確認はしていない（→ 2026-10-12 に PC で S1〜S6 を実機で確認し、すべて合格。結果は `docs/log.md`（決定は `docs/decisions.md`、経緯は `docs/log-history.md`） の「実測の結果」。以下の「公式文書で確認した事実」の節は、実測で裏づけられた）。

## 課題

GitHub への公開・非公開の境界は、workbase とそれ以外の1本だけ。AI はワークスペースのルートで起動するので、非公開側の `areas/` `projects/` `archives/` を全部読める。セキュリティの懸念と、見せたくないファイルが Vault の外に点在して作業効率が落ちた問題を、同時に解きたい。

## 前提（ユーザーが提示）

1. AI は Obsidian と Zed から使う。
2. AI は Claude Code が主。Codex・Copilot はほぼ使わないが、対応はできるようにする（重荷なら緩めてよい）。
3. 顧客データ・社外秘は、マスクしたものを AI に渡す。マスク前の原本は同じディレクトリに置かれる。
4. AI の出力に顧客データ・社外秘は無い。ただし、その中間ファイルをもとに、顧客データ・社外秘を含むファイルを作る。
5. 分離によるファイルの点在で、作業効率が大きく落ちた。改善したい。
6. WSL は使える。
7. workflow-kit に組み込み、projects / areas に展開するやり方を踏襲する。
8. works 直下は、remote を持たないローカルの git 管理。
9. Excel のままやり取りしたい。ピボットテーブルの既定の作成を頼む。まれに Excel VBA の作成も頼む。
10. できるだけ1パターンに揃えたい（管理に自信がないため）。手数の少ないフックにしたい。
11. 要望: 作業記録がわかる。再現できる。projects の成果と作業記録を areas に戻して同期できる（同期の時機は問わない）。

## 方向性: 案Y「AI 作業部屋」

「全部見える、`_noai/` だけ隠す」（禁止リスト）をやめ、「何も見えない、渡したものだけ見える」（許可リスト）にする。人の作業場（Vault）を正本にしたまま、Project ごとに WSL 側の「AI 作業部屋」を作る。ユーザーのたとえでは、WSL に fork して exec し、wait で回収し、archives へ移る段階が zombie → reap。

## 決まったこと（ユーザーが決定）

| # | 内容 | 決めた方法 |
|---|---|---|
| 1 | 防ぐ相手は両方: AI 事業者への送信と、workbase / exmem への混入 | カード |
| 2 | 鍵・証明書・トークンは、Vault の外の隣のフォルダ（例: `$HOME\works-secret`）に置く | カード（隣のフォルダ） |
| 3 | 方向は「人の作業場から AI 作業部屋へ切り出す」案Y | 発言 |
| 4 | 部屋は最初から L2: 部屋専用の WSL ディストリビューション。`/etc/wsl.conf` で `automount.enabled=false`（C: をマウントしない）と `interop.enabled=false` | 発言 |
| 5 | projects / areas での AI 作業は、機密の有無にかかわらず全部屋で行う（1パターン）。Vault 側で AI を使うのは workbase の作業だけ | カード |
| 6 | Claude Code のサンドボックスは任意の追加策（既定にしない）。Windows ネイティブでは効かないため | カード |
| 7 | `_noai/`（原本・対応表・実データ入りの成果物）は、archives へ一緒に移して当面残す。対応表の漏えいは、AI 分離とは別の論点（Vault は private 領域） | 発言 |
| 8 | Excel のままやり取りする | 発言 |

## 提案段階（ユーザーが明示していない。承認を得て決める）

> 2026-10-12 に、P1〜P8 を含む未決9項目を確定した（P1 は「Area ごとのディストロ、Project ごとのマウント」に変更。マウント点は `/mnt/room/<Project 名>`）。**確定の内容は `docs/log.md`（決定は `docs/decisions.md`、経緯は `docs/log-history.md`） の「2」が優先**。以下の表は、確定前の提案の記録。

| # | 内容 |
|---|---|
| P1 | 部屋の単位は Project ごと（open で作り close で捨てる。部屋の数 = 進行中の Project の数、上限3）。作業ごとの使い捨てより管理が少ない |
| P2 | 書き出し・取り込みのスクリプトは Windows 側の Python 1本（`room fork` / `collect` 相当）。部屋は C: をマウントしないので、Vault と部屋の両方が見えるのは Windows 側だけ。対応表も Windows 側にある |
| P3 | 部屋の共有フォルダは、Vault の中の `projects/<名>/ai/` だけをマウントする（drvfs のフォルダ単位のマウント。要実機確認）。`_noai/`（`raw/` `map/` `final/`）は `ai/` の外に置き、git で追跡しない |
| P4 | 人が言うコマンドは `room open` / `room start`（fork → exec → wait を1回で）/ `room close`（exit → zombie → reap）の3つ。部屋の中の `start` / `wrap` は今までどおり |
| P5 | Area への同期は郵便受け方式: 回収のたびに【案件】の項目を Area の `ai/docs/inbox.md` へ追記し、Area の AI が次の `start` で取り込む |
| P6 | Excel のピボットと VBA: AI がデータの xlsx と VBA を書き、人が Windows の Excel で実行する（部屋から Excel は起動しない）。復元後は「すべて更新」でピボットのキャッシュを直す |
| P7 | zombie（部屋の WSL 側の環境と履歴）は close から14日（仮）残し、期限後に記録を `ai/records/` に写して消す（reap） |
| P8 | マスクと復元は AI にやらせない（原本と対応表を読むため）。人が実行するスクリプトで行う |

## 公式文書で確認した事実（実機では未確認）

- Claude Code の `Read(<名前>/**)` の deny は、どの深さの同名フォルダにも効き、Edit / Write も止める。`cat` `head` など名前を指定した読み取りは止めるが、`grep -r` や、スクリプトの中で開くファイルは止めない。`.claudeignore` は効かない（code.claude.com/docs/en/permissions）。
- サンドボックスは macOS・Linux・WSL2 だけ。Windows ネイティブでは効かない。シェルのコマンドだけを守り、AI のファイル操作は deny 設定が守る（/sandboxing）。
- WSL の `wsl.conf` はディストリビューションごとの設定。`automount.enabled=false` で C: を自動マウントしない。`interop.enabled=false` で Windows のプロセスを起動しない。Windows からは `\\wsl.localhost\<ディストリビューション>\` で部屋のファイルに届く（learn.microsoft.com/windows/wsl/wsl-config）。
- Zed は Windows で WSL のフォルダを直接開ける。ただし Claude Agent（ACP）が WSL 側で動くか、Claude Code の設定を読むかは、文書に記述が無い（zed.dev/docs）。

## 既存のリポジトリとの関係（調べた範囲）

- workbase にあるのは、フックの手順書（`workflow-kit/`）とナレッジ。ワークスペースのルート（`areas/` `projects/` `archives/` `docs/`）は PC ごとのローカルで、workbase の外にある。手順書 `open-hook.md` / `wrap-hook.md`（`close-hook.md` は 2026-10-16 に削除。Project の終了は `room close`、判断は `room-context.md`） / `start-hook.md` と `hooks.md`（呼び出し表の正本）、ワークスペースの雛形 `workflow-kit/templates/workspace/`（`AGENTS.md`、`gitignore.template`、`ignore.template`）が、変更の対象になる。
- 現在の Project は `docs/` を Project 直下に持つ。P3 では `ai/docs/` に移る。open / close / wrap の「`docs/` の場所」を直す必要がある。
- `close` は `archives/` への `git mv` を、ディレクトリごとだと `Permission denied` で失敗することがあり、ファイル単位で行う（旧 `close-hook.md` の実測。今は `room close` がファイル単位で移す）。マウント中のフォルダの移動は、先にアンマウントする。
- 共有側（workbase）のルール: ローカルのファイルへ `[[リンク]]` を張らない。機密・会社固有の情報を書かない。コミットは `[領域] 変更内容`。
- モバイル側のセッションの記憶（チームのメモ）はリポジトリに入っていない。必要な情報は、この文書にすべて書いた。
