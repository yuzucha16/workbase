# AI に見せる領域・見せない領域の境界（設計）

- 初版: 2026-10-12（このスレッドで、ユーザーがカードで選択した4項目）。
- 改訂: 2026-10-12（ユーザーが前提を追加。初版の決定を見直した。下の「見直し」）。4 の取り下げはユーザーが承認。1〜3 の改訂案は提示済みで、異論なし。
- workbase とワークスペースには、まだ何も反映していない。
- 2026-10-12: ユーザーが「人の作業場から AI 作業部屋へ切り出す」方向（案Y）を選んだ。深掘りは [[ai-room-design]]。この設計の `_noai/` 方式は、ふつうの Project の安全網として残すかが未決。

## 前提（ユーザーが提示、2026-10-12）

1. AI は Obsidian と Zed から使う。
2. AI は Claude Code が主。Codex、Copilot はほぼ使わないが、対応はできるようにする。これが重荷なら緩めてよい。
3. 顧客データ・社外秘ファイルは、マスクしたものを AI に渡す。ただし、マスク前の原本が同じディレクトリに置かれる。
4. AI の出力に顧客データ・社外秘は無い。ただし、その中間ファイルをもとに、顧客データ・社外秘を含むファイルを作る。
5. 分離によるファイルの点在で、作業効率が大きく落ちた。改善したい。
6. WSL は使える。
7. workflow-kit に組み込み、projects / areas に展開するやり方を踏襲する。
8. works 直下は、remote を持たないローカルの git 管理。

## 前提から分かること

- **作業の流れ**: 原本 → マスク → AI が作業 → 中間ファイル → 復元（実データを戻す）→ 成果物。AI に見せないのは、両端（原本、成果物）と、マスクの対応表。
- **マスクと復元は、AI にやらせない**。AI が原本を読むことになるため。人か、人が実行する決まったスクリプトで行う。
- **点在を避けるには、原本も Project の中に置く**。Vault の外へ出すのは、案件に属さないもの（鍵、証明書、トークン）だけにする。
- **Obsidian と Zed は Windows で動く**。そこから起動する Claude Code も Windows ネイティブになり、サンドボックスは効かない（公式文書: サンドボックスは macOS / Linux / WSL2 だけ）。
- **Office ファイル（xlsx、pptx）は、AI が Python などのスクリプトで読む**。スクリプトの中で開くファイルは、Claude Code の deny 設定では止まらない。ここが最大の抜け道。

## 見直し（初版の決定 → 改訂案）

| # | 初版 | 改訂案 | 理由 |
|---|---|---|---|
| 1 | 送信と混入の両方を防ぐ。2段階 | 維持 | 前提と矛盾しない |
| 2 | 1段目（鍵・証明書・顧客データ）は Vault の外 `works-secret` | **鍵・証明書・トークンだけ**にする。顧客データの原本は、2段目（Project の中）へ | 前提3・5。顧客データまで外に出すと点在が戻る |
| 3 | 2段目は各 Project / Area の `_noai/` | 維持し、**git の追跡から外す**（`.gitignore` に `**/_noai/`）。中を `raw/`（原本）`map/`（対応表）`final/`（成果物）に分ける | 前提8: 追跡すると `.git` に原本の写しが残り、`git show` で読める。ignore すれば Claude Code の Grep（ripgrep）も既定で読まない |
| 4 | WSL2 でサンドボックスを使う | **既定にしない（ユーザー承認済み）**。WSL のターミナルで Claude Code を起動するときだけ使える追加の層にする | 前提1: Obsidian と Zed からの起動は Windows ネイティブで、サンドボックスが効かない。Vault を WSL 側に移すと Obsidian が使いにくく、`/mnt/c` 経由は遅い |

## 他案

| 案 | 内容 | 評価 |
|---|---|---|
| A（推奨） | Project の中に `_noai/`。deny ＋ git ignore ＋ エディタの除外 ＋ 規約 | 点在しない。Claude Code では強い。スクリプト経由と、他の AI ツールには弱い |
| B | Vault の外に同じ構成の木（`works-noai/projects/<名>/`）を作る | どの AI ツールにも効く。点在が戻る（前提5に反する） |
| C | 原本をパスワード付きで保存（Office のパスワード、7z など） | スクリプト経由でも、どの AI ツールでも読めない。開くたびにパスワードが要る。特に機密の高い原本だけに使う |
| D | AI の作業ディレクトリを `projects/<名>/work/` に絞り、`_noai/` をその外に置く | Claude Code は作業ディレクトリの外を読むとき許可を求める。ただし Obsidian / Zed はワークスペースのルートで開くので、効かない場面が多い |

推奨は A を基本にして、機密の高い原本だけ C を足す組み合わせ。

## リスクと緩和策

| # | リスク | 緩和策 | 残る度合い |
|---|---|---|---|
| R1 | AI が書いたスクリプト（openpyxl など）が、フォルダをまとめて読み、`_noai/` の原本を開く | 規約: スクリプトは入力のパスを明示し、上のフォルダを glob しない。`_noai/` を ignore して検索に出さない。機密の高い原本は案 C | 中。規約頼み |
| R2 | `grep -r` など、名前を指定しない読み取り | `rg` を使う規約（ignore を尊重する）。Grep ツールは ignore を尊重する | 小 |
| R3 | git の履歴から原本が読める | `**/_noai/` を ignore。`git add -f` 禁止は既存の規約 | 小 |
| R4 | Obsidian の AI プラグインが Vault 全体を索引する | 使うプラグインを Claude Code 系に絞る。Obsidian の「除外するファイル」に `_noai/` を足す（効くかはプラグインによる。要確認） | 中。プラグイン次第 |
| R5 | Zed の Claude Agent（ACP）が Claude Code の deny 設定を読むか不明 | 導入時に、`_noai/` のテストファイルを読ませて止まるか確かめる。Zed 側は `file_scan_exclusions` と `edit_predictions.disabled_globs` に `**/_noai/**` を足す（Zed の公式文書で確認。ただし AI のコンテキストから外す設定ではない） | 確認待ち |
| R6 | マスク漏れ（マスクした中間ファイルに実名が残る） | マスク後に、対応表の語が残っていないかを人がスクリプトで点検する（点検は対応表を読むので、AI には実行させない） | 中 |
| R7 | close で `git mv` しても、追跡外の `_noai/` は移らない | `close` の手順に、`_noai/` の移動か削除（保持期間）を足す | 小 |
| R8 | Codex / Copilot は Claude Code の deny を読まない | `AGENTS.md` の規約だけで対応。重要な作業は Claude Code で行う。足りなければ案 C | 中（前提2で許容） |
| R9 | 人が原本の中身をチャットに貼る | 規約 | 運用 |

## workflow-kit への組み込み（叩き台）

- `init`（ワークスペースの生成）: `.gitignore` に `**/_noai/`。`.claude/settings.json` に `"permissions": {"deny": ["Read(_noai/**)"]}`（`Read` の deny は Edit / Write も止める）。ワークスペースの `AGENTS.md` に規約（`_noai/` を読まない、書かない、スクリプトで glob しない、マスクと復元をしない）。
- `open`: Project / Area に `_noai/`（`raw/` `map/` `final/`）を作るかを聞く。
- `close`: `_noai/` の扱い（移す、消す、保持期限）を確認する手順を足す。
- ユーザー設定（PC ごと、workbase の外）: `Read(~/works-secret/**)` の deny。
- Obsidian / Zed の設定は dotfiles 側。

## 公式文書で確認した効き方

- Claude Code（code.claude.com/docs/en/permissions）: `Read(<名前>/**)` の deny はどの深さにも効き、Edit / Write も止める。`cat` `head` `sed` など名前を指定した読み取りも止める。名前を指定しない `grep -r` や、スクリプトが中で開くファイルは止めない。`.claudeignore` は効かない。
- Claude Code（/sandboxing）: サンドボックスは macOS / Linux / WSL2 だけ。シェルのコマンドだけを守る。`allowUnsandboxedCommands: false` で、外での再実行を止める。
- Zed（zed.dev/docs/configuring-zed）: `file_scan_exclusions` は検索とファイルツリーから外す。`private_files` は値を画面で隠すための印で、AI から外すとは書かれていない。編集予測は `edit_predictions.disabled_globs` で止める。
- Zed（/ai/external-agents）: Claude Agent は別プロセスで動き、ツールの許可はエージェント側に依存する。Claude Code の `settings.json` を読むかは書かれていない。

## 未決

- マスクと復元のスクリプトを workflow-kit で用意するか。
- Obsidian で使う AI プラグインは何か。
- `areas/dev-env/certs` の移し替え。
