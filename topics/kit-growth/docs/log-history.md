# 作業ログの経緯（log-history）

## Log

### 2026-10-16（topic-workflow を取り込み、close した）

- 止まっていた TODO 5 を見直した。足す側（docs-rules の読む順・「続き」、窓口の雛形）は済んでいたので、正本を `topics/AGENTS.md` にして、畳む側だけを行った。並行セッションの `close-hook.md` の削除（`c86b4d6`）と `topics/AGENTS.md` で重なり、マージした。
- topic-workflow は新しい「トピックを終わらせるとき」の最初の利用。【汎用】の Q4（共有フォルダ）だけ未反映だったので `topics/AGENTS.md` に足した。差分は `notes/topic-workflow/2026-10-16-kit-intake.diff`（プロジェクトの共有フォルダ）。

### 2026-10-16（`open` / `close` を畳む議論。`open` の Project の構造を `ai/` と `_noai/` に対応させた）

- ユーザーの問い「`open` と `close` は `room` に統合されて不要では」から始め、両手順書の役割を洗い出した。ひな形・状態更新・`archives/` への移動・コミットは `room` が担う。残るのは、部屋の AI の判断（`readme-draft.md`、`close.md`）、「Project の構造」の表、トピックの close だった。ユーザーは `close` をトピック専用にして `topics/AGENTS.md` に吸収する、`open` は構造に限定する、と決めた。
- `open` で、type 別の構造（`drafts/` `refs/` `src/` `sources/`）と `ai/` `_noai/` の対応を調べた。`_noai/` を外す案（直下にベタ置き）は、影響を調べて見送り、`_noai/` を残す（理由: type ごとの割り当てが要らず、追跡しない領域を一段で分けられる）。`ai/in/` へのシンボリックリンクは成り立たない（部屋から行き先が見えない）。
- 途中で出た前提: AI が使えなくなる（トークン制限）ケース。`restore` が `final/` を無条件に上書きする点を確認したが、別の話にした。リポジトリが正の `src` は、`restore` が `.git` の中身で止まることを確認し、残件にした。
- 差分は `notes/open-structure/2026-10-16-ai-mapping.diff`（プロジェクトの共有フォルダ）。コミットは `7b2c515`。
- 続けて、ユーザーの「キットに反映お願い」で `close-hook.md` の削除、`topics/AGENTS.md` への節、`room-context.md` への `close.md` の書き方の移動、`open-hook.md` の縮小を行った（`c86b4d6`）。`open-hook.md` は 6,748 字から 4,687 字、手順は 8 から 6、報告は 5 から 3。`hook-matrix.md` の基準の `open` 3,320 字は、実測と合っていなかったので下げ直した。

### 2026-10-16（「変更」を areas/projects に適用し、「基準文書」に改称した）

- 部屋の構成（`ai/work/`、`mask` `restore` `--adopt`、`close`）と突き合わせ、論点を2つ見つけた。①「中間成果物」が `ai/work/` の下書きの意味と衝突する。②繰り返す成果物は、次の変更が別の Project で起きるので、`close` の後も基準を渡す必要がある。ユーザーとのすり合わせで、①を役割で名づけ直し（向きによらず、変更の入力と検証の物差しになる文書。「基準文書」）、②を `ai/in/` + `--adopt` で解いた。置き場と機密の決まりは `decisions.md` と `change-method.md`。ユーザーの仮説「人と AI は工程を分割し、その境界が基準文書」も記録した。コミットは `40d8aa6`。

### 2026-10-16（「変更のやり方」を Must / Want で足した）

- `init 更新` が一撃で通った要因を振り返り、「変更のやり方」を解決・改善のやり方の延長に足した。ブロックA（仕込み。中間成果物）とB（変更）に分け、プレイブックの3文書（要求仕様・機能仕様・運用マニュアル）を中間成果物の出どころとして格下げした。ユーザーの条件は「ガッチリ定義しない。Must と Want で小さく始め、`review` の対象にする」。`methods.md`、`exmem/lessons/change-method.md`、`hook-matrix.md` の「review の点検」7、`exmem-index.md` を更新。決定は `decisions.md` の同日の項。

### 2026-10-16（init に `init 更新` を足した）

- ユーザーの依頼で、雛形の更新を works に反映するモードを検討し、案 B（基点つきの3者マージ。案を出して承認後に反映）を選んだ。`init-update.md` を新設し、`init-hook.md`・`hooks.md`・`docs-rules.md`（`Template-Rev` トレーラー）・`hook-matrix.md` を合わせた。決定は `decisions.md` の同日の項。`git merge-file` で、埋めた行が残ることと、旧版 → 新版の雛形の変更が当たることを一時ディレクトリで確認した（衝突 0）。
- 同日の追加（ユーザーの指摘）: 雛形の読む順番が指す `README.md` を項目 5 が生成していなかったので、`templates/workspace/README.md` を足し、生成物と初回コミットに含めた。`init-hook.md` の自己点検のトレーラーを2行（`Workflow-Kit` は廃止済み）に直した（`8b74187`）。`hook-matrix.md` の `init-update` の字数を 7.9k に直した（初出の 3.9k は誤り）。
- 続けて、`init 更新` が一撃で通った要因を話し合い、「変更のやり方」を解決・改善のやり方の延長で足す案が出た。議論は次のセッションへ(log.md の Next Actions 8）。

### 2026-10-16（各フックの cwd の期待を点検し、review の点検対象を 3 リポジトリに広げた）

- 各フックが期待する cwd と書き込み先を突き合わせた。`review` は起動した単位 1 つの記録だけを見ており、works から起動すると resources の `exmem/inbox/`・`topics/` と、公開リポジトリ（resources、dotfiles）の機密が点検されなかった。works の基準に「点検の対象」の一覧を置き、入力 3・4・6 がその全リポジトリを見るようにした（`302fccb` `9b19540`。ユーザーの決定、案 A）。
- 見つかった食い違い 4 件を直した（`9b19540`）: `wrap` の終了時の 1 問は起動した単位に記録、`exmem/AGENTS.md` と `exmem/README.md` の「exmem で起動する」を「`resources/` で起動し exmem の続きで扱う」に、`open` と `close` に実行場所（部屋の中。副作用は人が `room` で行う）を明記。
- 各フックの cwd の期待を `hook-matrix.md` の Must の 3 行に記録し、`review` の点検に含めた（`53c3771`）。あわせて、手順「網羅度を確認する」の本文を `hook-matrix.md` の「review の点検」に移し、`review-hook.md` を 4,623 → 4,183 字にした。入力の数は増やしていない。次回の `review` が初回の比較になる。

### 2026-10-16（wrap を軽くした、フックの重さの基準）

- `start 改善`（改善3: 星取り表）で `wrap` を軽くした（`9fbf4e4`）。`docs-rules.md` は「コミットと push」の節だけ読む（約4k字減の見込み。実測は未）、報告を6項目から5項目、改善案は Open Questions に足して `review 消化` で承認を取る。見送り: push 条件の `gh repo view` を毎回やめる案、手順1の対象特定を縮める案、「このフックの改善」章を畳む案（改善案の移し方で代替）。
- 各フックの字数・手順の項目数・報告の項目数を `hook-matrix.md` の「重さの基準」に固定し、`review` が比べる形にした（`da81042`、ユーザーが設計を採用した記録は `dc2931d`）。字数 +20%、項目数 +2 以上で見直し対象。N は3回の `review` の後に決め直す。判断は `decisions.md` の同日の2項目。
- 終了時の1問: 遠回りなし。

### 2026-10-16（review の消化モードと start の引数つきモード）

- 並行作業で完了済みの Next Actions / Open Questions が残る問題に、フックを増やさず対応した。`review` に消化モード（`review 消化`。完了の可能性・すぐ完了・それ以外に、根拠つきで分ける。完了の判断はユーザー）を足し、`start` が合計10件超のとき一度だけ勧める（`f395e34`）。「10件」は仮置きで、実測していない。
- `start` に `start 解決` / `start 改善` を足した（`8242e1c`、名称は `c0a46cb` で「問題解決」から「解決」に変更）。インタビューの代わりに、ゴールを聞いて、やり方を選んで始める。引数なしの `start` は残した。
- やり方の置き場を検討し、案 C を採った(`28202d7`、ユーザーの承認): 選ぶ基準と骨子は `workflow-kit/methods.md`、理由・実例・落とし穴は `exmem/lessons/` に残す。`lessons/` は統合や改名で参照が切れやすく、手順の入口には不安定なため。
- 決定記録に追記したとき、PowerShell の二重引用符内のバッククォートが制御文字に化けた（`` `review` `` の `` `r `` が改行、`` `again` `` の `` `a `` がベル）。元の版から書き直した（`c0a46cb`）。追記は単一引用符で行う。

### 2026-10-16（共有側から works への名指しを外した）

- 共有側（resources）が works をリポジトリとして名指しする説明を、「ワークスペースのルート」に言い換えた（窓口、手順書、`room.py` のヘルプ文、設計・引継ぎ 5 本）。works 固有の運用記録 `guides/explain/agent-safety-rules.md` は works の `docs/explain/` へ移し、`guides-index.md` と `review-hook-why.md` の参照を外した。kit の `init` フックと `room` が works の PARA 構造を前提にすることは許容。判断は works の `docs/decisions.md` の先頭の項（ユーザーの決定）。コミット `6d8f427` `b50bab2`。遠回りの答え: なし。

### 2026-10-16

- works、resources、dotfiles の `AGENTS.md`・README・`docs/log.md` の規則を揃える作業をした（フェーズ1〜3。一律に kit を正とはしない方針で、明らかなずれは事前にユーザーへ確認した）。kit の変更: `docs-rules.md` を読む時機の統一、階層化の規則、機密の項の畳み、workspace 雛形の写しの除去、`review` の入力 6（機密の点検）と入力 8（リポジトリ間の整合）。判断は `docs/decisions.md` の「2026-10-16」。dotfiles 側は README を 34.8KB から 16KB に分割し、`log.md` を 17.9KB から 3.8KB に縮めた。コミット: resources `9c87f10` `2156d92` `2a35149` `3cdeeb1` `286d714`、dotfiles `cc20299` `71e326d` `000125e` `a404711` `293c0a3`、works `142c226`。遠回りの答え: なし。

### 2026-10-15

- cwd の明文化（topic-workflow の TODO）を、ユーザーがカードで5問選んで決めた（起動場所、読む順番、上の階層からの続き、部屋、`wrap` の書き込み先）。kit 5ファイルを変え（`4997f7a`）、判断は `docs/decisions.md` の「2026-10-15 cwd を明文化した」。
- トークン消費を抑える改善を、改善のやり方3（観点のランキング → 星取り表 → 修正・削除・追加の案 → 優先度 → 実施項目の確定）で進めた。12観点から上位4点、さらに切る・絞るに絞り込み、ユーザーが選んだ13件を反映した（`d1150f2`、`a74a017`、`a46cf2e`）。星取り表の点は、切る 10 → 16、絞る 18 → 24。判断は `docs/decisions.md` の「2026-10-15 会話を『切る』と出力を『絞る』の対応を入れた」。やり方は exmem の `lessons/improvement-coverage-matrix.md`（`fbbefa0`）。
- `review` の入力に、トークン消費の自己採点を足した（`4a294b2`、`6bd1a2a`）。星取り表は `workflow-kit/token-matrix.md`（4観点、基準値 103）。
- 既存のワークスペースの `AGENTS.md` の読む順番は、ユーザーが各 PC で直した（2026-10-15、ユーザーの申告）。
