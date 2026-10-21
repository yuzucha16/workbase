# 判断の記録（decisions）

## Principles

- 1つの情報を読者の違う複数の人（人と AI）に読ませるときは、分ける基準を「読む問いが違い、かつ中身も違うか」にする。同じ事実の表示違いは分けない。理由: 分けると同期がずれる。手順書のように、問い（順序・実行）が違うものは分ける。→ inbox/2026-10-21-multi-reader-doc-split

## Decisions

### 【この件】会議録のナレッジ化: 置き場・単位・範囲・2層・顧客名を決めた（2026-10-21）
- 決めたこと（ユーザー）:
  - ①規則（型・タグ・索引・昇格の流れ）だけ workbase に置き、中身（顧客・案件）は works 側に置く。ただし参照用は、Project 内の `ai/work` → `ai/in` だけでなく、Project を跨げる Area 配下に置く。
  - ②共有の単位は Area。自社・顧客ごとの抽出は want で、`org:` の項目を持たせる。
  - ③「同じ扱い・方針・ルール」は、型・タグ・索引・昇格の流れまで。
  - ④決定事項・アクションアイテムは、既存の3ラベル（【この件】【案件】【汎用】）に載せる。
  - ⑤AI 向け・私向けの2系統は手段で、緩和する。1ファイル2層（冒頭の数行＝人向け、本文＝AI 向け）にし、横断の一覧は Bases で見る。ファイル分割はできるだけ減らす。
  - ⑥顧客名は Area 内では書いてよい。AI（room）に渡すところは従来どおりマスク。
  - ⑦入力は、自動の文字起こしと、自分の議事録・メモ。
- 根拠: ユーザーの回答と発言（2026-10-21）。使い方は ToDo・アクションアイテムの抽出、決定事項の要約、各 Project への入力と方向修正、Area・Project 全体に効くナレッジ。
- 却下案: 非公開リポジトリの新設（運用が増える）、マスクして workbase に上げる（顧客固有の内容が残らない）、2ファイル（同期がずれる。「シンプルに」に反する）、Project 内だけの置き場（Project を跨げず、寿命が狭い）。

### 【汎用】Area を跨ぐ共有知の設計の軸: 渡し方・選び方・マスクの時期・戻り（2026-10-21）
- 決めたこと（ユーザー）: ①渡し方は (a)（必要な分を Area から取り出し、マスクして `ai/in/` に置く）。②選び方は「絞って人が確認」。ただし手間になるので**仮案**（見直しは、実際に使って負担が出たとき）。③マスクの時期は渡すとき。④戻りは既存の `room close` → `ai/docs/inbox.md`（【案件】）。統合の流れは未決。
- 追加で決めたこと（ユーザー、2026-10-21）: ⑤マスクした写しは**渡すときに作る**（生成物として常に持つ案は採らない。負担が出たら見直す）。⑥**統合は Area に置く**。⑦知識は3層で扱う: ①事実（実名入り、Area）、②部屋用の写し（渡すときに作る、マスク済み）、③一般化した教訓（workbase。既存の `room stock` で、一般化したものだけを出す）。**固有の事実は、仮名にしても workbase に切り出さない**（どんな条件でも）。
- 統合の実行主体（ユーザー、2026-10-21）: ⑧**統合は部屋の作業にする**（マスクした写しを `ai/in/` に置き、部屋の AI がマスクのまま統合し、人が `restore` で実名に戻して Area に置く）。works のルートで起動した AI が Area の実名入りの知識を読んで統合する案は採らない。理由（確認済み）: 部屋の目的は実名を AI に見せないこと。deny は `Read` と `Edit` を止める安全網で、シェル経由は止まらない（`init-workspace.md`、2026-10-16）。`integrate` の works 権限は「－」（`hooks.md`）で、変えなくて済む。⑨戻り先を Area の知識置き場にする経路を `room` に足す（kit の変更。設計後に承認を取る）。⑩復元の上書き保護（`final-manifest.json`）の実機試験は前提から外す。運用か警告にとどめる。
- `room` の設計（ユーザーが4点を承認、2026-10-21。`room.py` の読解に基づく）: ⑪Area の知識置き場は `areas/<Area>/knowledge/`（`ai/docs/inbox.md` とは別）。⑫絞り込みは `--where <項目>=<値>`（frontmatter のどの項目でもよい。複数なら AND）。⑬部屋の AI の出力は `ai/out/knowledge/` に置き、この下だけを Area に戻す（ほかの成果物は従来どおり `_noai/final/`）。⑭`pull` したファイルは `manifest.json` に Area 由来として記録する（`masked_from` に Area のパス）。
- 変更の範囲（案。**`room` の実装は kit の変更で、実装前に承認を取る**）: `room pull`（絞り込み → 人が確認 → `_noai/raw/area/` にコピー。マスクは既存の `room mask`）、`restore_project` に Area への書き出しを追加（既存ファイルは警告）、Project の README に `knowledge-dest:`（`data: restore` が前提）、`room/README.md`、テスト。
- 会議録の型（ユーザーが承認、2026-10-21。見本 `records/meeting-note-example.md`）: ⑮置き場とファイル名は `areas/<Area>/knowledge/YYYY-MM-DD-<slug>.md`（打合せ1件 = 1ファイル。統合ノートは日付なしのトピック名、`kind: integrated`）。⑯frontmatter は `type: area-note`、`kind`、`title`、`status`、`date`、`org`、`project`、`tags`、`created`、`updated`、`sources`、`todo_open`、`todo_due`。⑰本文の見出しは `冒頭`（人向け、10行以内〔仮〕）、`決定`、`ToDo`（表）、`背景・経緯`、`事実・数値`、`未決・要確認`。⑱ToDo の正は本文の表で、`todo_open` と `todo_due` は表から数えた派生（ずれたら表を信じる）。⑲決定と教訓の各行に【この件】【案件】【汎用】を付ける。⑳AI に渡す写しはファイル全体をマスクし、AI は冒頭を読み飛ばしてよい。
- 実装（2026-10-21。`workflow-kit/room/room.py` の `pull`、`restore_project` の追加、`tests/test_room.py` の `PullKnowledgeTest`、`room/README.md`）と、設計からの差分（ユーザーが「実装へ」と承認した範囲での AI の判断。**確認を求める**）:
  - ㉑README の項目名は `knowledge-dest` でなく `knowledge_dest`。理由: `read_frontmatter` の正規表現がハイフンを読めない。
  - ㉒決定 ⑭の「`masked_from` に Area のパス」は採らず、manifest には名前を書かない（`pull-sources.json` に置く）。理由: manifest は `ai/records/` にあり部屋の AI から見える。Area のファイル名（`<日付>-<スラッグ>.md`）は顧客名を含みうる。同じ理由で、部屋に渡るファイル名は `<日付>-<パスのハッシュ>.md` にした。
  - ㉓Area への書き出しで、前回の書き出しから変わっている既存ファイルは、警告して上書きし、直前の版を `_noai/final/_prev/knowledge/` に退避する（決定 ⑩の「警告にとどめる」の範囲。止めない）。
  - ㉕（ユーザー、2026-10-21）㉓を変更: 人が変えた Area の既存ファイルは、警告して上書きでなく、**`restore` が何も書かずに止まる**（`--force` で上書き。直前の版は `_noai/final/_prev/knowledge/` に退避）。決定 ⑩（上書き保護を前提から外す）は、`final-manifest.json` の実機試験を前提にしない、という意味に限る。理由: 人の編集を黙って消さない。影響: `start` の終わりで止まっても `ai/out/` は回収済み。単体テストは更新して通った。
  - ㉔`pull` は `status: active`（無ければ active 扱い）だけを取り出す（古い決定を渡さない）。
  - ユーザーが ㉑〜㉔ を承認（2026-10-21）。
  - 確認: 単体テスト 102 件のうち、新規 5 件と既存のマスク・復元は合格。失敗 2 件は `openssl` が無い環境の `CaCertTest`（今回の変更と無関係）。実機の通し試験（ダミーの Area `pilot2`、手順 `records/pull-e2e-test.md`）は、ユーザーが 2026-10-21 に「すべて問題なし」と報告した（個別の数字は未記録）。
- 根拠: ユーザーの承認（2026-10-21）。案と比較は `guides/explain/cross-area-shared-knowledge.md`。
- → inbox/2026-10-21-masked-area-knowledge-flow
- 却下案: (c) AI が Area を直接読む（`areas/` を扱わない決まりに反する）、(b) 常にマスク済みの写しを持つ（二重管理。ただし生成物にする案は検討中、同日の議論）。

### 【この件】【仮 〜2026-10-28】トピックと計画の置き場: `records/` は2か所にする（2026-10-21。正本は workbase 直下 `docs/decisions.md` の同日の項）
- 決めたこと（ユーザー）: トピックは `topics/private-knowledge/`（`planning-method` と同じ構造: 窓口・`docs/`・`records/`）。`records/` の使い分けは2つだけにする。①`topics/kit-growth/records/` = 測ったことだけ（品質チェックと振り返り。従来どおり）。②各トピックの `records/` = そのトピック自身の出力（計画・見本・確認メモ）。6R・憲章・WBS・マイルストーン・作り方のメモは `topics/private-knowledge/records/`。
- 根拠: ユーザーの選択（AI の案を採用）。中身で置き場を決めると、題材ごとの計画が計画のやり方のトピックに混ざらない。最初の指示（`topics/kit-growth/private_knowledge/`、計画は `topics/kit-growth/plans/`）は、ユーザーの記憶が曖昧で、既存の運用と違っていた。`plans/` は案④の中の案で、決定済みではなかった。
- 却下案: `topics/kit-growth/` の下にトピックを置く（索引の他のトピックは1階層）、`topics/kit-growth/plans/` への集約（案④は保留中で未決）、`planning-method/records/` に計画を集める（別題材の計画が混ざる。昇格のときまで現状維持）。
- 弱点: 計画の置き場が題材ごとに分散し、探す場所が増える。
- 見直しの条件: `planning-method` の昇格のとき（2026-10-20 の決定「計画の置き場は昇格のときに決める」を、この題材については先に決めた）。`planning-method/records/` の `stock-modes-*` と `usage-viz-*` は、同日にユーザーの指示でそれぞれのトピックに切り出した。
