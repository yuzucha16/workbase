# 判断の記録（decisions）

## Decisions

### 【この件】【保留 〜2026-11-08】Obsidian の Vault を 2 つに分ける（2026-11-01）

- **2026-11-01 `review 消化`: ユーザーが 3 論点とも【保留】と判断した**（期日は 11-08）。スクリーニング（型 D: 論点 1 Vault の分割、論点 2 `.obsidian` の実体と正本、論点 3 一方向の自動反映）の指摘: ① 10-17 前後の「works ＝ Vault」の一語化と、「Vault 側の AI／deny」の指す先が、分割後も works でよいか未確認。② 論点 2 は 10-05 の延長だが、ジャンクション 2 本でリンク前に Obsidian を開くと `30_link.bat` が止まる経路が倍になる。③ 論点 3 の仕組みの詳細は dotfiles 側に置く（`app-config-placement.md` の Principles、依存は dotfiles → workbase の一方向）。方針の 1 行だけ workbase に残す。④ 実機確認の順序は ③ → ④ → 論点 2・3 の実装。加えて pc1 のリンク調査、「Vault ＝ works」の文面の直し方の一覧、Obsidian を先に開いた場合の確認。

- 決めたこと（仮。ユーザー「確認はすべてOKです」）: Vault を `resources/`（workbase。md のみ）と `works/`（projects・areas・`resources_p/`。html や excel など `inv` の成果物も見る）の 2 つにする。`works/.obsidian` は残し、除外（`app.json` の `userIgnoreFilters`）に `resources/` `archives/` `repos/` を加える。`resources_p/` は works の Vault に含める（ユーザー「ファイラー 兼 viewer になればラッキー」）。`archives/` はほぼ見ない（同）。pc1 は `resources/` の Vault も参照用に開く（特に `guides/`）。
- 根拠（ユーザーの発言）: pc2 は resources（workbase）の改良が主、pc1 は areas・projects の作業が主で、works 配下で両方を見る利点が無い。事実: プラグインは 3 つだけ（`colored-tags` `html-viewer` `xlsx-viewer`）で、md のみの `resources/` で 2 つのビューアは効かないだけ。差は小さい。Vault を分ける利点は、検索・ブックマーク・クイックスイッチャーの範囲と `workspace.json` が閉じること。`workspace.json` は dotfiles で追跡対象外（`.gitignore`）で、Obsidian が自動生成する。最小構成のコピーは置かない。pc2 の調査（2026-11-01）: works の `resources/` の外の md 92 ファイルに `[[リンク]]` 47 件。`resources/` を指すものは 0 件（残りは `areas/…` `projects/…` のパス形式で、works の Vault 内で完結）。pc1 は未調査（ユーザー「使っていない」）。
- 設定の持ち方（ユーザー、同日）: 2 つの `.obsidian` の実体は、どちらも dotfiles に置き、`resources/.obsidian` と `works/.obsidian` へジャンクションで張る（ユーザー「それぞれを workbase へジャンクションする。dotfiles 側の正本の話」）。dotfiles の中では **resources 用が正本**。プラグイン以外の設定（外観・CSS スニペット・テーマ・コア設定）は正本だけを直し、works 用へ自動で反映する（一方向）。見た目は両方でそろえる。プラグインは Vault ごとに別で、ユーザーがコミットする（反映の対象外）。workbase は dotfiles を知らず、`.obsidian` を追跡しない（`.gitignore` に足す）。2026-10-05 の「実体は dotfiles」と依存の向きは変わらない。
- 却下案: 設定を dotfiles に 2 系統持ち、直すたびに対象を指定する（ユーザー「面倒なので避けたい」）。同じ実体を 2 つの Vault に張る（`workspace.json` が衝突する）。
- 反映の仕組み（仮決め。ユーザー「この形はいいですね。派生物として作るわけか。良いです」「リンク適用時がトラブルに気づけて良い。手動でもあると便利」。意図は、意図的な二重管理でも resources 用と works 用の設定がずれないようにすること）:
  - dotfiles に Vault ごとの置き場を 2 つ持つ。resources 用（正本）: `app.json` `appearance.json` `core-plugins.json` `types.json` `snippets/` `themes/` とプラグイン（`colored-tags` のみ）。works 用の固有分: `community-plugins.json` `plugins/`（3 つ）と `app.override.json`（works だけ違う項目。今は `userIgnoreFilters` だけ）。いずれも git で追跡する。
  - works 用の派生分（正本からコピーした共通ファイルと、正本に `app.override.json` を重ねた `app.json`）は、git で**追跡せず**、反映のたびに生成する（`.gitignore`）。git に二重のファイルが残らず、works 側を直しても次の反映で正本に戻る。
  - 反映はリンク適用時に自動で走り、手動でも同じコマンドで走らせる（何度走らせても同じ結果）。上書きの前に、works 側が前回の反映から変わっていないかを比べ、変わっていたら表示して上書きする（works の画面で設定を変えたことに気づける）。`--check` は書き換えずに差分だけを出し、dotfiles の試験が「派生分が正本と一致するか」の点検に使う。
  - 限界: resources の画面で変えた外観は、次の反映まで works に届かない（`--check` が未反映を出す）。
  - 却下案: works 側の共通ファイルを読み取り専用にする（Obsidian の保存が失敗しうる）。`snippets/` `themes/` をリンクで共有する（Windows の git のシンボリックリンクに特権が要る）。
  - dotfiles の README に、正本はどれか、反映の方向、直してよい場所は resources 用だけであること、固有分と派生分の区別、反映のコマンドを書く（実装と同時）。
- 〔未決。実装の前に決める〕③ 入れ子の Vault で除外フィルタが検索・リンク補完に効くかの実機確認。④ 今の `windows\obsidian\.obsidian` をどちらへ移すか（プラグイン 3 つがあるので works 用が自然）。
- 影響範囲（変えるのは `review 消化` の後）: `exmem/lessons/obsidian-vault-structure.md` の図と works の再定義、`app-config-placement.md` の `.obsidian` の節、dotfiles の `links.map`・反映スクリプト・試験（別リポジトリ・別コミット）、`resources/.gitignore`（`/.obsidian`）。

### 【この件】type を `dev` と `inv` に集約した（2026-10-24）

- 正本は workbase 直下の `docs/decisions.md` の同日の項（決めたこと、根拠、却下案）。ここには重ねて書かない。
- 論点8件と仮決めの経緯は [[room-type-consolidation-notes]]。

### 【この件】room の GitHub 認証は、リポジトリ単位の読み取り専用 deploy key（SSH）で始める（2026-10-31）

- 根拠: ユーザーが「deploy key（推奨）」「読み取り専用で始める」を選んだ。
- 却下案: ホストの `gh` のトークンを room に渡す（AI から全リポジトリに書けてしまう）。fine-grained PAT は、deploy key で足りない場面（複数リポジトリを 1 つの認証で扱う）が出たら再検討。
- push は room に許さない（ユーザー「個人開発は許す、チーム開発は許さないの 2 パターンが出るので、許さない方に倒す」）。個人開発で許す場面が出たら、書き込み可の deploy key をリポジトリごとに足す。
- 正本は `ai-isolated-work-room.md` の同日の決定（C 案の却下理由の更新を含む）。
- `room close` に「部屋の中の clone が全部 push 済み」の検査を足す（ユーザー、10-31）。実装は `repos:`（Open Questions 2）と置き場（5）の後。

### 【この件】cwd は案 A に決定（2026-10-31）

- 根拠: ユーザー「ソフト開発全般 かつ room の設計思想を考えると a の方が良い」「a にしましょう。すすめて」。理由は、`records` を `ai/records` の一か所に纏めたいこと、`ai/<成果物>/env` のように `~/src` より前の工程でも cwd が変わらないこと。
- 却下案 B（コード作業は cwd=`~/src/<repo>`）: 工程で cwd が変わり、`records` が `~/claude-records/<名>` に分かれる。コード開発だけなら直感的だが、設計の例外になる。
- 実測で見つかった問題: `ROOM_GIT_WRAPPER` が `$PWD` だけで判定していたため、cwd が `/mnt/room/` のとき `git -C ~/src/<repo>` が部屋用 git に化けた。判定を git の対象（cwd に `-C` を順に当てる）に直した。下の「`~/src/<repo>` は差し替えの外」は、この改修で成り立つ。

### 【この件】works の再定義と開発リポジトリの置き場（2026-10-31）

- 根拠: ユーザーが「よいです」「想定は前者です。あなたの推奨でOK」と承認した。
- works（Vault）と workbase は 1:1 で、workbase は works の中の `resources/`。works と projects は 1:N の PC ローカルの台帳（remote なし）。pc2 の works は非公開にして、その後削除する。渡せるものは workbase に移す（Open Questions 4 は閉じた）。
- 成果物: `inv` は Office ファイルと markdown。`dev` は git リポジトリ（N 個）で、置き場は開発環境（IDE）のある OS（win / wsl / linux）。今の対象は WSL だけ。
- `repos:`（`url`、`where: wsl|win|linux`、`branch`）を Project の README に持たせる。`dev` の既定は `where: wsl`、`inv` は repo なし。処理するのは `wsl` だけ。
- clone の置き場: `~/src/<repo>`。git で管理するものは `~/src/<repo>`、しない試作や一時のコードは `ai/out/<成果物名>/src/`。
- `ai/` のマウントは続ける（人と AI の受け渡しの唯一の経路）。claude の cwd は `/mnt/room/<Project>` のまま、`~/src/<repo>` は追加ディレクトリで渡す（案 A）。実測してから確定する。
- room から開発サーバーへ SSH しない（分離と読み取り専用の認証の方針に反する）。サーバー上の作業は人が SSH して行い、窓口は `ai/in/target/`（環境メモ、実行ログ）と README の `target:`。AI は手順を `ai/out/` か `ai/docs/` に書き、人が実行して結果を戻す。秘密鍵、パスワード、トークン、機密のホスト名は置かない（ホストは別名）。
- サーバー側で AI を動かす形は、room の外のモードなので別設計（今は対象外）。

### 【この件】Open Questions を見送る（2026-10-31）

- 根拠: ユーザー「oq を omit してください」。works の再定義、`repos:`、clone の置き場、pc2 の remote、影響する文書、聞き返しの未測の 7 件を、ここでは追わない。
- 「別トピックにします」は、ユーザーの言い間違い（意図は「別セッションで続ける」）で撤回した。トピックはこのまま。
- 「room close に clone が全部 push 済みの検査を足す」（同日の決定）は、前提の `repos:` と置き場が見送りになったため、実装の予定が無い。決定の記録は上の項に残す。

### 【この件】サブエージェントで実測のループを回す案は見送る（2026-10-27）

- 根拠: ユーザー「omit します。トークン使用量を抑えたいため」。3 構成を通す実測は、人が部屋を回す。

### 【この件】最初の実利用を受けた決定（2026-10-25）

- `room open` が `ai/docs/` に `log.md` `decisions.md` `log-history.md` の雛形を置く（他の単位と同じ 3 つ）。根拠: ユーザー「room open がひな形をおく」「他と同じように、log, log-history, decisions の3つ」。
- `inv` の基準文書は「問い＋完了条件の 1 行で足りる」とする。**仮決め**（ユーザー「これは仮決め。いまは決められないため」）。
- 実測A・B の記録としてこの件を閉じる(ユーザー「実測の記録として閉じる」、2026-10-25)。対象 Project への不具合の返却はしない。
- `dev` の「テスト」の節に、文書と実装の食い違いを機械で検査する静的ケースの型を足した(ユーザー「足します」、2026-10-25)。根拠: `sample_dev` と `tests/` だけの実測(`t_static.sh`)の 2 例。
- `docs/` だけの `dev` を測った(`sample_devdoc`、2026-10-25。以前の「測らない」をユーザーの指示で取り消した)。結果の承認(ユーザー「承認しました」): 「文書作成」の項(骨子、図、ゲート承認の判断基準)は残す。基準文書の形は `project-structure.md` の未決に仮決めとして書いた。
- 置き場の取り違えの原因(2026-10-25 に部屋の AI に聞いた): `ROOM.md` と `room-context.md:67` の「人が読む最終版の成果物は `ai/out/deliverable/` の下」が、`dev-deliverable-guide.md` の「成果物は `ai/out/<成果物名>/`」と食い違う。`deliverable/` は Area に実名で戻す経路(2026-10-21)の置き場で、「人が読む最終版」の語が手順書(人が読む文書)に当たってしまった。`project-structure.md` は読まれていなかった(`brief-hook.md` は `room open` の判断基準として指すだけ)。取り違えは 5 回(`work/`、`deliverable/` 3 回、README、レビュー版を `ai/docs/`)。
- `docs/` だけの `dev` は測らない（ユーザー「もう使わないので測定しなくても良いかな」）。`env/` だけ、`tests/` だけは、最初に使うときに測る。
