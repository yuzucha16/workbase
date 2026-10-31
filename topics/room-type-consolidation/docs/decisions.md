# 判断の記録（decisions）

## Decisions

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
