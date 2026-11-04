# 判断の記録（decisions）

## Decisions

### 【この件】`inv` を工程別の構造にする素案を採る（2026-11-04）

- 根拠: ユーザー「（名前は）良いです。実際にやってみて変える可能性はありますが、第一印象ではあっていると思います」「（基準文書は仮決めのまま）良いです。ただ今回は pptx などに清書するまでが成果物」「（記録先）良いです」。
- 決めたこと: `inv` の構成要素を `question.md` `sources/` `findings/` `checks/` `report.md` `publish/`（清書。pptx など）にする（`project-structure.md`）。置き場は `ai/out/<成果物名>/` の下。叩き台で、実測で変える可能性がある。
- 実験は別セッションで観点別（問い設計・収集・集約・示唆・裏取り・清書）に行い、`topics/room-type-consolidation/records/` に残す。最初の例は eg1（Web）を通しで 1 回、次に eg2（社内 Excel・テキスト）でマスクの差分を足す。
- 最初の実験のお題（ユーザー指定）: プレゼン資料作成ツールの比較（Marp、Quarto、Slidev）。AI 活用を想定した選定軸と作成時間短縮の方法。
- `inv` の基準文書（問い＋完了条件の 1 行）は仮決めのまま。`question.md` が育つので、実験 1 の結果で見直す。

### 【この件】置き場の実測を受けた 3 点を決める（2026-11-04）

- 根拠: ユーザー「表通りに分けないことを許しても、人間が気づけるならOK。…逃げ道としても区別ができるようにしたい」「cwd が変わらず実害がなければ許容できる」「足します／緩めます／記録します」。
- ① 表通りでなくてよい。逃げ道は専用サブディレクトリ＋README の 1 行ずつの記録。`deliverable` を成果物名の予約名に足した（`project-structure.md`）。
- ② `git -C` は望ましいにとどめ、`cd` も許容（`project-structure.md`、`room.py` の ROOM.md 雛形）。
- ③ Area の成果物置き場は `routes()` が Project 名の下に固定するので、成果物名は衝突に関係しない。規則はこのまま運用し、強めない。

### 【この件】`<成果物名>` の既定を Project 名と同じにする規則を、手順書と `ROOM.md` に書く。測定は打ち切る（2026-11-04）

- 根拠: ユーザー「書いてよいです」（手順書）、「案1で進めます」（`ROOM.md` の雛形に足す）、「切りましょう」（A の追試後に測定を終える）。11-01 の案 1 の実施。
- 手順書だけでは AI が読まず効かなかった。`ROOM.md` に足した後は、規則あり 5 回中 1 回だけ Project 名と同じ。残りの判断は log の Next Actions。

### 【この件】`target:` の書式と `ai/in/target/` に置くものを決める（2026-11-01）

- 根拠: ユーザー「良いです。私のイメージ通り」（`review 消化` で素案を示した後）。前提はユーザーの「ssh で room（WSL）に繋ぐか、物理的に別環境の PC（Linux）に繋ぐかの差でしかない」。
- 内容: README の frontmatter に `target:`（`name`、`via: ssh|wsl`、`os`、`note`）。`ai/in/target/` は `env.md`、`run-YYYY-MM-DD.md`、秘匿値抜きの設定サンプル。秘密鍵・パスワード・トークン・機密のホスト名は置かない。処理する側は作らない。
- 反映先: `workflow-kit/project-structure.md` の「開発リポジトリ」の節。10-31 の「room から開発サーバーへ SSH しない」は変更なし。

### 【この件】Obsidian の Vault を 2 つに分ける（2026-11-01 仮決め、2026-11-02 正式化）

- **2026-11-01 `review 消化`: ユーザーが 3 論点とも【保留】と判断した**（期日は 11-08）。スクリーニング（型 D: 論点 1 Vault の分割、論点 2 `.obsidian` の実体と正本、論点 3 一方向の自動反映）の指摘: ① 10-17 前後の「works ＝ Vault」の一語化と、「Vault 側の AI／deny」の指す先が、分割後も works でよいか未確認。② 論点 2 は 10-05 の延長だが、ジャンクション 2 本でリンク前に Obsidian を開くと `30_link.bat` が止まる経路が倍になる。③ 論点 3 の仕組みの詳細は dotfiles 側に置く（`app-config-placement.md` の Principles、依存は dotfiles → workbase の一方向）。方針の 1 行だけ workbase に残す。④ 実機確認の順序は ③ → ④ → 論点 2・3 の実装。加えて pc1 のリンク調査、「Vault ＝ works」の文面の直し方の一覧、Obsidian を先に開いた場合の確認。

- **2026-11-02 正式化（ユーザー「正式化して実装に進めますが、文面直しはnaに積んでおいてください」）**: 下の仮決めを決定にする。実装前の前提（③④、pc1 のリンク調査、文面の一覧、`30_link.bat` が止まる条件）は済んだ。実装は dotfiles（別リポジトリ・別コミット）と、workbase の `/.obsidian` の `.gitignore`（済み）。文面直しは実装とは分け、NA に積んで後で行う。
- 決めたこと（仮。ユーザー「確認はすべてOKです」）: Vault を `resources/`（workbase。md のみ）と `works/`（projects・areas・`resources_p/`。html や excel など `inv` の成果物も見る）の 2 つにする。`works/.obsidian` は残し、除外（`app.json` の `userIgnoreFilters`）に `resources/` `archives/` `repos/` を加える。`resources_p/` は works の Vault に含める（ユーザー「ファイラー 兼 viewer になればラッキー」）。`archives/` はほぼ見ない（同）。pc1 は `resources/` の Vault も参照用に開く（特に `guides/`）。
- 根拠（ユーザーの発言）: pc2 は resources（workbase）の改良が主、pc1 は areas・projects の作業が主で、works 配下で両方を見る利点が無い。事実: プラグインは 3 つだけ（`colored-tags` `html-viewer` `xlsx-viewer`）で、md のみの `resources/` で 2 つのビューアは効かないだけ。差は小さい。Vault を分ける利点は、検索・ブックマーク・クイックスイッチャーの範囲と `workspace.json` が閉じること。`workspace.json` は dotfiles で追跡対象外（`.gitignore`）で、Obsidian が自動生成する。最小構成のコピーは置かない。pc2 の調査（2026-11-01）: works の `resources/` の外の md 92 ファイルに `[[リンク]]` 47 件。`resources/` を指すものは 0 件（残りは `areas/…` `projects/…` のパス形式で、works の Vault 内で完結）。pc1 は 11-02 に調査（下の実機確認の項）。
- 設定の持ち方（ユーザー、同日）: 2 つの `.obsidian` の実体は、どちらも dotfiles に置き、`resources/.obsidian` と `works/.obsidian` へジャンクションで張る（ユーザー「それぞれを workbase へジャンクションする。dotfiles 側の正本の話」）。dotfiles の中では **resources 用が正本**。プラグイン以外の設定（外観・CSS スニペット・テーマ・コア設定）は正本だけを直し、works 用へ自動で反映する（一方向）。見た目は両方でそろえる。プラグインは Vault ごとに別で、ユーザーがコミットする（反映の対象外）。workbase は dotfiles を知らず、`.obsidian` を追跡しない（`.gitignore` に足す）。2026-10-05 の「実体は dotfiles」と依存の向きは変わらない。
- 却下案: 設定を dotfiles に 2 系統持ち、直すたびに対象を指定する（ユーザー「面倒なので避けたい」）。同じ実体を 2 つの Vault に張る（`workspace.json` が衝突する）。
- 反映の仕組み（仮決め。ユーザー「この形はいいですね。派生物として作るわけか。良いです」「リンク適用時がトラブルに気づけて良い。手動でもあると便利」。意図は、意図的な二重管理でも resources 用と works 用の設定がずれないようにすること）:
  - dotfiles に Vault ごとの置き場を 2 つ持つ。resources 用（正本）: `app.json` `appearance.json` `core-plugins.json` `types.json` `snippets/` `themes/` とプラグイン（`colored-tags` のみ）。works 用の固有分: `community-plugins.json` `plugins/`（3 つ）と `app.override.json`（works だけ違う項目。今は `userIgnoreFilters` だけ）。いずれも git で追跡する。
  - works 用の派生分（正本からコピーした共通ファイルと、正本に `app.override.json` を重ねた `app.json`）は、git で**追跡せず**、反映のたびに生成する（`.gitignore`）。git に二重のファイルが残らず、works 側を直しても次の反映で正本に戻る。
  - 反映はリンク適用時に自動で走り、手動でも同じコマンドで走らせる（何度走らせても同じ結果）。上書きの前に、works 側が前回の反映から変わっていないかを比べ、変わっていたら表示して上書きする（works の画面で設定を変えたことに気づける）。`--check` は書き換えずに差分だけを出し、dotfiles の試験が「派生分が正本と一致するか」の点検に使う。
  - 限界: resources の画面で変えた外観は、次の反映まで works に届かない（`--check` が未反映を出す）。
  - 却下案: works 側の共通ファイルを読み取り専用にする（Obsidian の保存が失敗しうる）。`snippets/` `themes/` をリンクで共有する（Windows の git のシンボリックリンクに特権が要る）。
  - dotfiles の README に、正本はどれか、反映の方向、直してよい場所は resources 用だけであること、固有分と派生分の区別、反映のコマンドを書く（実装と同時）。
- 追加（2026-11-02、ユーザー）: works のエクスプローラーから `resources` `resources_p` `repos` を CSS スニペットで隠す（dotfiles 側。実機で消えた）。重さは感じないとのことで、`resources_p/` も `userIgnoreFilters` に足す（検索・リンクから外れる。`resources_p` を works の Vault の viewer として使う案は、当面見送り）。
- 〔2026-11-02 実機確認（PC1、ユーザー）〕③ works の `app.json` の `userIgnoreFilters` に `resources/` を加えると、検索とリンク（補完）の対象から外れた。ファイルエクスプローラーには表示されたまま（除外フィルタは表示を消さない）。これは限界として受け入れる（ユーザー、11-02。分割の目的の検索・クイックスイッチャーの範囲は閉じるため。CSS スニペットで隠す案は、反映する設定が増えるので採らない）。`resources/` に `.obsidian` を作っても、上位の `works/.obsidian` に影響しなかった（入れ子の Vault は互いに独立）。pc1 のリンク調査: `resources/` を指す `[[リンク]]` は 0 本で、pc2 と同じ結論。
- 〔2026-11-02 ユーザー〕`30_link.bat` が止まる経路は、リンク先に**実ファイル（実ディレクトリ）がすでにある**とき。ジャンクションが既にあれば上書きする。したがって、Obsidian を先に開いて実の `.obsidian` ができた場合だけ止まる（手で退避して再実行。`app-config-placement.md` の既存の記述どおり）。2 本になっても、止まる条件は変わらない（Vault ごとに同じ）。これで実装前の前提はすべて済んだ。
- **④ 決めたこと（ユーザー、2026-11-02）: 今の dotfiles の `windows\obsidian\.obsidian` の写し先は works（works 用の置き場）。** 根拠: プラグイン 3 つ（`html-viewer` `xlsx-viewer` は works でしか効かない）がある。resources 用（正本）は、ここから共通の設定を切り出して作る。
- 〔2026-11-02 動作確認（ユーザー「a,b,c,d,e問題なしです」）〕`30_link.bat` の (a) `uv` `py` `python` のどれでも `obsidian_sync.py` が走る、(b) 2 本のジャンクション、(c) `resources\` が無いときの `[SKIP]`、(d) 旧 `.obsidian` の上書き、(e) 両方の Vault が開く、がすべて問題なし。Vault の 2 分割の実装は確認済み。
- 〔2026-11-02 文面直し済み（ユーザー「良いです」「承認します」）〕下の一覧のとおり直した。`exmem/lessons/obsidian-vault-structure.md`（節・図・`.obsidian` の項）、`app-config-placement.md`（Principle 1 文と新しい Decision）、`templates/workspace/` は `workflow-kit` の `docs/decisions.md` にも記録。
- 「Vault ＝ works」の文面の直し方の一覧（2026-11-02、AI。直すのは正式化の後、実装と同時）: 「works（Obsidian の Vault）」の形が `README.md` 3 行、`AGENTS.md` 8 行、`exmem/README.md` 37 行、`workflow-kit/templates/workspace/README.md` 5 行と `AGENTS.md` 5 行にある。直し方は「works（Obsidian の Vault の 1 つ。`resources/` は別の Vault）」の形に揃える。`exmem/lessons/obsidian-vault-structure.md` は図と「works の再定義」の節、`exmem/lessons/app-config-placement.md` は 31・35 行と `.obsidian` の節（88 行〜。2 つの置き場と一方向の反映を足す）。`guides/explain/ai-room-why.md` 264・270 行の「Vault 側」は、部屋の外（人が触る側）の意味なので「Obsidian 側」に直す（指摘 ①。Obsidian の AI を workbase の作業に使うのは、分割後は resources の Vault）。`exmem/lessons/git-line-endings.md` 28 行は経緯の記述なので直さない。
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

### 【この件】`<成果物名>` の決め方は案 1(階層を残し、名前の規則を決める)(2026-11-01)

- 根拠: ユーザー「案 1 にします」。`<成果物名>` は「外部に成果物としてそのまま出せる形」の名前(ユーザーの説明)。階層は、`ai/out/` 直下の予約物(`close.md` `readme-draft.md` `stock/` `knowledge/` `deliverable/`)と混ざらないため、`room restore` が `ai/out/` を置換するときの配布の単位にするために残す(10-15 の決定の根拠)。
- 規則の案: 1 Project = 1 成果物なので、名前は Project 名と同じを既定にする。外部に出す名前が Project 名と違うときだけ、その名前にする。
- 順序: 手順書(`dev-deliverable-guide.md`)に書く前に、AI が名前をどう付けるかを実測し(規則なし)、その後に書いて、もう 1 回測る。ケース A・B・C(A: `src/` のみ、B: `src/` `tests/` `docs/`、C: `env/` `src/` `tests/` `docs/` `report.md`)を、置き場を依頼に書かずに通す。判定は、配置が `project-structure.md` の表どおりか、取り違えが再発しないか、聞き返したか。
- 却下案: 階層をやめて `ai/out/` 直下に置く(予約物を移す必要があり、`room.py` の restore・stock・readme・close の前提が変わる)。

### 【この件】log の Open Questions から「サーバー側で AI を動かす形」を外す（2026-11-01）

- 根拠: ユーザー「room-type-consolidation の oq1 は omit してください。不要です」。上の 10-31 の項の「別設計（今は対象外）」の記述は、記録として残す。

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
- 〔2026-11-04 ユーザー「仮決めのままでよい」〕`inv` の基準文書（問い＋完了条件の 1 行）は仮決めのまま据え置く。見直しの期日は置かない。
