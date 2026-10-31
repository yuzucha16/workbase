# 作業ログの経緯（log-history）

## Log

### 2026-11-01（Obsidian の Vault を 2 つに分ける案を仮決めした。記録のみで、実装は未着手）
- ユーザーの相談: pc2 は resources（workbase）の改良が主、pc1 は areas・projects が主なので、`works/.obsidian` を `resources/.obsidian` と `projects/.obsidian` に分けたい。事実の確認: `.obsidian` は dotfiles へのジャンクション、プラグインは 3 つ（`colored-tags` `html-viewer` `xlsx-viewer`、約 240KB）、`workspace.json` は dotfiles で追跡対象外。pc2 で `resources/` の外の md 92 ファイルの `[[リンク]]` 47 件を数え、`resources/` を指すものは 0 件。
- 仮決め: Vault は `resources/`（md のみ）と `works/`（projects・areas・`resources_p/`。`resources/` `archives/` `repos/` を除外）の 2 つ。`areas/` が works 直下で `projects/` と並ぶため、`projects/` だけの Vault にはしなかった。実体は両方 dotfiles に置き、ジャンクションで張る（ユーザーの補足で、私が「workbase が追跡するか」と読み違えた点を直した）。resources 用が正本で、works 用の共通ファイルは派生物として生成し、追跡しない。works だけ違う項目は `app.override.json`。リンク適用時に自動、手動でも可、`--check` で点検（ユーザー「この形はいいですね」）。根拠は `decisions.md` の同日の項。
- 未着手: 入れ子の Vault の実機確認、今の `.obsidian` の移し先の決定、dotfiles の実装（別コミット）。

### 2026-11-01（deploy key の手順書を作り、ユーザーが手で通して確認した。Next Action「deploy key の再実施」を閉じた）
- 作成: `guides/howto/room-github-deploy-key-setup.md`（`howto` の型。構成案をユーザーが了承。リポジトリ名などは `<owner>` `<repo>` のプレースホルダー）。`guides/guides-index.md` に 2 か所追記。
- ユーザーの確認で直した点: 指紋の照合は、`/tmp/gh_hostkey`（公開鍵そのもの）でなく、`ssh-keygen -lf` が出した `SHA256:…` を、`gh api meta` の ED25519 の値と比べる（HTTPS 経由で SSH と独立）。read only の確認は `gh repo deploy-key list` でなく `gh api repos/<owner>/<repo>/keys --jq '.[] | {title, read_only}'`（`true`）。
- 閉じた根拠: ユーザーが章 4〜7（指紋、`read_only`、clone と push の拒否、片付け）を実機で通し、「na3 は close」と指示。`deploy-key add` の read only 登録と、公開鍵の受け渡しも通った。

### 2026-10-31（案 A の実装。実機の確認は 1 Project の実測にまとめる）
- `a9d03cc`: `room start` が `claude` のとき `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` と、README の `repos:`（`where: wsl`）の `~/src/<repo>` への `--add-dir` を渡す（`read_repos` `claude_extra_args`。clone が無ければ注意して渡さない）。
- `721f3f9`: `ROOM_GUIDE` に `git -C ~/src/<repo>` と push 不可、`project-structure.md` に `repos:` の節、`ai-isolated-work-room.md` の Decisions に案 A、`room open` の README 雛形に `repos:` の案内。`room close` が `repos:` の clone の未コミット・未 push で止まる（`unpushed_repos`）。単体テストは 143 件 OK（3 件スキップ）。
- 動作確認は単体テストまで。実機の確認は、ユーザーが「1 Project で `env/` `tests/` `docs/` を通す実測」の Next Action に `src/`（コード開発）を含めてまとめて行う（「上の na には src/ に関する実測が無かったので、今回のコード開発も含めてやってみます」）。

### 2026-10-31（案 A の実測。git ラッパーを直し、cwd 固定の案 A に決定）
- 実測（`room-myenv`、`claude -p`、cwd=`/mnt/room/sample_dev`、使い捨ての `~/src/probe-repo`）: `--add-dir` あり→読み書きできる、なし→拒否。`records` は cwd が `/mnt/room/` のままなので `ai/records` に出る。追加ディレクトリの `CLAUDE.md` は既定では読まれず、`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` で読まれる。
- 見つけた問題: `ROOM_GIT_WRAPPER` が `$PWD` だけで判定し、cwd が `/mnt/room/` のとき `git -C ~/src/<repo>` が部屋用 git（`~/gitdirs/<Project>`）に化けた（AI の commit が `ai/` に入る）。`cd ~/src/<repo> && git` は正しいが、承認待ちで止まる（非対話）。
- 議論: 私は案 B（コード作業は cwd=`~/src/<repo>`）を推したが、ユーザーが「`ai/<成果物>/env` のように `~/src` より前の工程では cwd が変わるのは違和感」「`records` を一か所に纏めたい」と指摘。ジレンマ（コード開発なら B、ソフト開発全般と room の設計思想なら A）を整理し、A の影響範囲（変更は `ROOM_GIT_WRAPPER` の 1 か所、Area 共有の `/usr/local/bin/git` なので不具合は全 Project に出る）とリスクを示して、ユーザーが A を選択（「a にしましょう。すすめて」）。
- 実施（`83ecc18`）: ラッパーの判定を git の対象（cwd に `-C` を順に当てる）に変更。`--git-dir` `--work-tree` `--bare`、`GIT_DIR` 設定済み、`clone`、読み取れない引数は素通し。`RoomGitWrapperTest` を新設（偽 git で 15 ケース）、全 140 件 OK。実機で `git -C` の add/commit、ローカル clone、AI の commit が clone 側にだけ入ることを確認。実機の `/usr/local/bin/git` は新版に差し替え済み。計測用の clone・退避・一時ファイルは削除。
- 罠: PowerShell から `wsl` へ渡す文字列は CRLF になり、`/usr/local/bin/git` が壊れた（`/bin/sh^M`）。base64 で渡して直した。`claude -p` は標準入力を読むので、`bash -s` でスクリプトを渡すと食われる（`</dev/null` を付ける）。非対話では、`cd` 後の git と `--allowedTools` の書式（`"Bash(git:*)"` を 1 つずつ引用）で止まる。
- 区切り: 残りの実装（`room start` の環境変数、`repos:` の `--add-dir`）は別セッションで行う（ユーザー）。

### 2026-10-31（WSL からの認証の確認を受けて、works の再定義と置き場を決めた）
- 確認: ユーザーが、WSL から認証が要る clone を通せることを確認した。WSL にリポジトリを置く前提の仕様の確認。
- 決定（`decisions.md` の「works の再定義と開発リポジトリの置き場」）: works（Vault）と workbase は 1:1。works と projects は 1:N の PC ローカルの台帳。`dev` のリポジトリは、開発環境（IDE）のある OS に置く（今は WSL だけ）。`repos:` に `where: wsl|win|linux` を持たせる。clone は `~/src/<repo>`、git で管理しないコードは `ai/out/<成果物名>/src/`。`ai/` のマウントは続け、cwd は `/mnt/room/<Project>` のまま `~/src/<repo>` を追加ディレクトリで渡す（案 A、実測前）。room から開発サーバーへ SSH しない。人が SSH して、窓口は `ai/in/target/` と README の `target:`。サーバー側で AI を動かす形は対象外。
- 閉じた論点: 旧 Open Questions 1〜6（3 は 10-31 に決定済み、4 は pc2 を非公開にして削除するので閉じた）。`ai/src` と呼んでいた置き場は `ai/out/<成果物名>/src/` で合っている（`project-structure.md` の `dev` の構成）。
- 補足: Obsidian の Vault は works 全体なので、`inv` の markdown を Obsidian で開くのは矛盾しない。「Obsidian が見るのは `resources/`」とは書かず、「works の中に workbase が `resources/` として入る」と書く。
- ユーザーの指示: deploy key の再実施は優先度を下げる（手すきで）。手順書にするかは置いておく。次は案 A の実測を別セッションで行う。

### 2026-10-31（room の非公開リポジトリの認証を実機で通した）
- 手順: ホストの `gh` で空の非公開リポジトリ `yuzucha16/room-auth-check` を作成。`room-myenv` の中で ed25519 の鍵を生成（`~/.ssh/id_room_authcheck`、パスフレーズなし、権限 600）。`~/.ssh/config` に別名 `github-authcheck`（`IdentitiesOnly yes`）を置き、known_hosts は `ssh-keyscan` の結果の指紋が GitHub 公開の値（`SHA256:+DiY3wvv…`）と一致することを見て採用。公開鍵を `gh api` で deploy key（read_only）として登録。
- 結果: room の中で `git clone git@github-authcheck:…` が通り、`push` は「The key you are authenticating with has been marked as read only」で拒否された（期待どおり）。
- 罠: PowerShell の here-string は CRLF。`wsl.exe … -- sh -s` に渡す前に `\r\n` を `\n` にする。
- `room close` は GitHub に触れない（`cmd_close` は remote を使わない）ため、認証の有無で結果は変わらない。「room 内の clone が全部 push 済み」の検査は未実装（Open Questions 3）。
- 部屋の内部 git（`~/gitdirs/<Project>`、`ROOM_GIT_WRAPPER`）との関係: ラッパーは `/mnt/room/<Project>` の下だけ `GIT_DIR` を差し替える。`~/src/<repo>` の clone と remote は影響を受けない。`room close` の `--commit` は works の git へのコミットで、部屋の内部 git ではない。3 者（works の git、部屋の内部 git、clone と remote）は無関係。
- ユーザーの決定: 確認用リポジトリは消す（作成は自分でもう一度やる）。C 案の却下理由の更新は了承。push は room に許さない（個人開発は許す・チーム開発は許さないの 2 パターンがあるので許さない方に倒す）。close の検査は足す。works の再定義と `repos:` は別トピックにする。
- 片付け: room 側の鍵、`~/.ssh`、clone は削除。GitHub 側の `room-auth-check` は `delete_repo` の権限が無く未削除（ユーザー作業）。
- 反映: `exmem/lessons/ai-isolated-work-room.md` の Decisions に 10-31 の決定を追記、10-13 の C 案の項に更新を指す注を付けた。
- 後続（ユーザー、同日）: 「別トピック」は「別セッションで続ける」の言い間違いで、トピックはここで続ける。Open Questions は見送る。GitHub の `room-auth-check` は削除済み。見送った論点（元の文）: ① works の再定義（works と workbase は 1:1、works と projects は 1:N の PC ローカルの台帳、成果物は `inv` が Office・`dev` が WSL 内の git リポジトリ N 個）。② Project の README に `repos:`（`url` `where` `branch`）を持たせるか。③ 閉じる条件に「room 内の clone が全部 push 済み」（決定済み、実装は ②⑤ の後だった）。④ pc2 の works の公開 remote を外すとき、公開済み成果物の切り出し先。⑤ clone の置き場（`~/src/<repo>`、`ai/src` との関係）。⑥ 影響する文書（`obsidian-vault-structure.md`、`room.py` の `open`、`project-structure.md`）。⑦ 置き場と対象環境を依頼に書かないとき AI が聞き返すかは未測。

### 2026-10-31（works の再定義の相談と、Zed から room の ext4 を扱えることの確認）
- ユーザーの問題提起: `open --type` の整理が発端。works が GitHub に公開・非公開どちらにもなり（pc1 は非公開、pc2 は公開）、リポジトリが works の 1 つに固定される。`inv`（Windows Office）と `dev`（Windows/Linux/WSL）の成果物があり、リポジトリ情報が Windows 側で、room のある WSL からファイルシステムを跨ぐ。複数のリポジトリを触る要望が pc1 で実際にあった。案は、works を remote なしの PC ローカルにし、開発用リポジトリを room 側で clone して 1:N にする。
- AI の初回の提案: 台帳（works、remote なし）／コード（room の `~/src/<repo>`、リポジトリごとの remote）／`inv` の成果物（works、公開するなら別リポジトリ）の 3 層。認証は room に読み取りだけ置き push は人、の案を推した（未決）。
- ユーザーの補足: works は Vault の写しとして始まった（`resources/` を参照するため）。今は Vault として要るのは `resources/` で、works 配下の markdown は主でない。works と workbase は 1:1、works と projects は 1:N の PC ローカルの台帳、という表現は正しい。今のルールに適合させるのでなく、この考えに既存のルールを合わせに行く。
- Zed の WSL 対応（公式 docs: `projects: open wsl`）。リモートの分担（UI はローカル、LSP・タスク・ターミナルはサーバー側）が WSL にも当てはまるとは docs に無かった。
- 実機の確認（ユーザー、10-31）: Windows の Zed から `room-myenv` に接続し、`ai` の `~` で `git clone` した `~/dotfiles`（公開リポジトリ）を読めた。`df -T` で ext4（`/dev/sdd`、マウント `/`）。続けて編集、LSP のハイライト、git の表示、Agent も動いた。「ext4 に置いたコードが Zed から見えない」懸念は解消。
- 未確認は、認証が要る（非公開の）リポジトリの clone / push。ユーザーが次回、SSH か `gh` かのベストプラクティスを聞くところから始める。
- 決定は書いていない（works の再定義は方針の整理の段階）。

### 2026-10-28（`dev` の成果物が `ai/work/` に出る件を、再現待ちで閉じた）
- ユーザーの判断で、10-26 起票の Next Actions（`dev` の成果物が `ai/work/` に出る件の原因の特定）を `log.md` から外した。理由: その後、部屋の AI が急に `ai/out/` に出すようになり、当時のセッションの情報を探すのが手間なため。原因は未特定のまま（候補は 10-26 の項の 3 つ）。
- 再現したら再開する。そのとき確かめること: ① 部屋の `~/shared/ROOM.md` の基準コミット（cfd3b81 より前か）。② その Project の README の成果物の行。③ 部屋の AI に「`ai/work/` に置いた理由と、そのとき読んだ手順書」を聞く。(1) 写しが修正前か (3) `script-guide.md` の `ai/work/` の記述が原因なら、`ROOM.md`（`room.py`）と `brief-work-types.md` に「コードやスクリプトも成果物は `ai/out/<成果物名>/`。`ai/work/` は捨ててよい下書きだけ」を明記する。
### 2026-10-28（wrap の新しい規則で log.md を掃除）
- `wrap` の新しい規則で、決まった Open Questions を移した。置き場の取り違え 5 回の原因は特定し（`ROOM.md` と `room-context.md` の `ai/out/deliverable/` の記述が `dev-deliverable-guide.md` と食い違う。`decisions.md`）、手順書は 10-25 に直した（再発の確認は Next Actions に残る）。`sample_devenv` への不具合の返却はしない（ユーザーの判断、10-25）。
### 2026-10-27（済みの Next Actions を log.md から移した）
10-25 に済んだ 7 件の詳細。(1) `report.md` の置き場: コードは `ai/out/deliverable/` だけ Area に、それ以外は `_noai/final/` に戻す。食い違いは `methods.md` の書き方だけだったので `ai/out/<成果物名>/report.md` に直した(決定は不要)。(2) 単一の問いの章立て(`brief-hook.md`、`research-method.md`)。(3) `dev` の「テスト」に文書と実装の食い違いを機械で検査する型を足した(ユーザー承認)。(4) `dev-deliverable-guide.md` の旧名(`dev-env` `dev-test`)の説明を削った(承認)。(5) `sample_devenv`: ENV-001〜010 全件 PASS、SET-001(root で中止)も確認。型は機能した。静的検査は shellcheck と ruff が部屋に無く `bash -n` まで。uv の版は固定していない。(6) `sample_devtest`(`ai/out/devenv-tests/`): 要求 14 ID に対応、65 件実行で PASS 62・FAIL 3・SKIP 1。観察は、質問の推奨の置き場が `work/` でガイドの `ai/out/<成果物名>/` と食い違った(人が正した)、テストを実装に合わせて緩めた件は変更前後と理由を `report.md` に書かせる依頼が要った、`tests/t_static.sh` が(3)の起票の 2 例目。同日、サブエージェントでループを回す案を見送りと決めた(トークン使用量を抑えるため。`decisions.md`)。(7) `sample_devdoc`: 「文書作成」の項は残す。基準文書の形を仮決め(`project-structure.md` の未決)。あわせて `room.py:1197`(`ROOM.md` の元)と `room-context.md:67` を「Area に実名で戻したい最終版だけ `deliverable/`。Project の成果物は `ai/out/<成果物名>/`」に直し、`brief-work-types.md` に `dev` の最初の `brief` で `project-structure.md` と `dev-deliverable-guide.md` を読む指示を足した(単体テスト 139 件 OK、skip 3)。

### 2026-10-26（`dev` の成果物が `ai/work/` に出る件の起票）
ユーザーが、PC1 の `dev` の部屋の AI が成果物をすべて `ai/work/` に出したと報告(一貫して `work/` だったので読み替えられたが、`work/` と `out/` が混ざると困る)。手順書を調べ、原因の候補を 3 つ挙げた(写しが修正前、`work` と `out` の線の曖昧さ、`script-guide.md` の `ai/work/` の記述の多さ)。PC1 の部屋は見られないため特定できず、ユーザーが「部屋の AI に聞くやり方で最適化しましょう」と決め、Next Actions に積んだ。同日、メモリの「次は考え方の文書」は、10-24 に済んでいたため直した(`project-structure.md` の「type の考え方」)。

### 2026-10-25（`env/` だけ・`tests/` だけ・`docs/` だけの実測と、置き場の取り違えの修正）
ユーザーが手元で 3 本を作り、AI の質問と成果物を見て手順書を直した。`sample_devenv`(Ubuntu 24.04 実機で ENV-001〜010 全件 PASS、SET-001 も中止を確認)、`sample_devtest`(要求 14 ID に対応、65 件実行で不具合 3 件と仕様の曖昧さ 2 件。`ai/in/` は不変)、`sample_devdoc`(骨子と図の要否を聞いた。基準文書の形を仮決め)。置き場の取り違えが 5 回(`work/`、`deliverable/` 3 回、README、レビュー版を `ai/docs/`)。部屋の AI に読んだ手順書を聞き、原因は `ROOM.md`/`room-context.md` の「人が読む最終版は `deliverable/`」と、`project-structure.md` を読んでいないことと分かった。直した(単体テスト 139 件 OK)。旧名の説明の削除、`dev` の「テスト」に文書と実装の整合の検査の型、`brief-work-types.md` に `project-structure.md` を読む指示も同日。決定は `decisions.md`。確認待ちは、直した `ROOM.md` で次の `dev` が取り違えないか。

### 2026-10-25（最初の実利用の観察を受けた手順書の修正）

`sample_dev`（`src/ env/ tests/ tools/ docs/` の CLI）と `sample_inv`（Obsidian の wikilink の調査）で観察した。両方で出た指摘を直した: `room open` が `docs/` の 3 つの雛形を置く（テスト 123 件合格）、`ai/X` の読み替え（`room-context.md`）、`docs/` の中身を 3 つに揃える（`project-structure.md`）、先に全部渡されたときの要約の省略（`brief-hook.md`）、ユーザーが書いた完了条件の扱い（`room-context.md`）。`dev` 側は、構成要素の聞き方（`brief-work-types.md`）、表の組み合わせ・環境要求の置き場（`dev-deliverable-guide.md`）。`ai-room-why.md` の `start` の記述を `brief` の改名に合わせた。残件は `log.md`。

### 2026-10-24（続き: type の考え方を記載）
- ユーザーが、考え方・方針は叩き台で十分と判断。`project-structure.md` の冒頭に節「type の考え方」を置いた。前回の `project-structure.md` に重複が混入していたのを直した（原因: 文字列置換で、先に出る同じ語に当たった。置換後に見出しと行数を確認していなかった）。

### 2026-10-24（続き: guide の見直し）
- `dev-deliverable-guide.md` の不整合 7 件の叩き台を出し、ユーザーが論点 1〜5、活動の表の程度、`script-guide.md` の名前に OK。実装して反映した（決定は root の `decisions.md`）。ユーザーが、「方針の文書が無い」と指摘し、Next Actions に起票。

### 2026-10-24
- ユーザーの依頼で議論を開始。`room.py` は type を読まず、違いは手順書だけと確認し、叩き台（事実の表、論点8件）を出した。ユーザーが別セッションの分類（investigation と development）を持ち込み、2 type 案に改訂。新値は `dev` と `inv`、既定は `dev`、旧値は受け付けない、曖昧な例は成果物の名前で決める、で承認。同日に実装して反映した（`decisions.md` は root の同日の項）。
