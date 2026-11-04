# Project の構造

`open-hook.md` から移した（2026-10-17、ユーザーの承認。本文は原文のまま）。`open-hook.md` は 2026-10-24 に廃止した。Project を立てる前の判断基準は下の「Project を立てる前の判断基準」、README 本文の下書きの書き方は `room-context.md`。

2026-10-08 ユーザーが承認。2026-10-16 に、AI 作業部屋の構造（`ai/` と `_noai/`）への対応に書き直した（ユーザーが承認）。

すべての Project は AI 作業部屋で行う（部屋の外の読み替えは持たない）。type ごとの違いは、**成果物の中身と、`ai/` のどこに何を置くか**だけ（type は `dev` と `inv` の2つ。下の「種類別の置き場」）。`ai/` と `_noai/` の中身は `room open` が作る（`workflow-kit/room/README.md`）。`ai/` 直下の5つは `room open` が先に作る。その下は、空のディレクトリを先に作らず、最初のファイルが来たときに作る。深さは `ai/out/<成果物名>/` の下まで数えて2階層以内（`src/` の中身などは対象外）。

## type の考え方（2026-10-24 ユーザーの決定）

Project は、問題解決の単位で、1 つの部屋で行う。問題解決の活動は、大きく**調べる側**（調べる、整理する）と**作る側**（計画する、作る、確かめる）に分かれる。type は、この 2 つのどちらを成果物にする Project かを表す。

- `inv`（調査。investigation）: 成果物が「結論と出典」で、出したら保守しない。調べ方は、依頼の言葉で引く出力の型（`research-explain-output`）。
- `dev`（開発。development）: 成果物が「作って保守するもの」で、基準文書と検証がある。手順書・仕様・設計・チェックリストなどの文書だけの成果物、環境構築、テストも含む。

**線は、活動ではなく成果物で引く。** 活動は反復し、1 つの Project に混ざる（調べながら作り、作りながら調べる）。活動で type を決めると、決められない。成果物なら、1 つに決まる。

- 曖昧なときは、成果物の名前で決める（設計書にまとめるなら `dev`、結論の報告なら `inv`）。
- 調べてから作る流れは、Project を分ける。`inv` の `report.md` は、閉じた後なら `room open <次> --area <A> --from <inv の Project>` で次の Project の `ai/in/from-<inv の Project>/` に引き継ぐ（下の「閉じた Project の引き継ぎ」）。まだ閉じていない成果物は、internal の Area なら人が `ai/in/` に置いて `room start --adopt` で記録する。1 Project の中で type を変えない。
- type の違いは、作業の構造の違いで、**成果物のサブディレクトリの組み合わせ**に現れる（`inv` は `report.md`。`dev` は `docs/` `src/` `env/` `tests/` `tools/` から必要なもの）。`room` は type で動きを変えない（README の frontmatter に書くだけ）。違いを持つのは、この文書と `dev-deliverable-guide.md`、`brief-work-types.md`、`brief-hook.md`、調査の出力の型（`research-explain-output`）。
- 活動と置き場の対応は、下の表の「主な活動」の列に目安として載せる。拘束ではない。

固定の核（全 type 共通）。「主な活動」は、活動と置き場の**目安**の対応（拘束ではない。活動は反復し、混ざる）。活動の語は、調べる・整理する・計画する・作る・確かめる:

| パス | 内容 | 主な活動 | 部屋の AI |
|---|---|---|---|
| `README.md` | frontmatter と、目的・成果物・計画（`ai/work/plan/`）へのリンク。完了条件・範囲外・未決は計画（6R）に書き、README に写さない | （前提） | 読むだけ（`ai/ctx/` の写し） |
| `ai/ctx/` | `room start` が作る前提の写し（Project と Area の README）。追跡しない（git が無視する） | （前提） | 読むだけ |
| `ai/in/` | 人が渡す入力。調べて得た資料、Area から渡された知識（`in/area/`）、マスク済みのデータ、前の Project の成果物。部屋では読み取り専用 | 調べる（の結果を受け取る） | 読むだけ |
| `ai/work/` | 途中の作業。集めた資料、整理、設計の下書き、試行、使い捨てのスクリプト。捨ててよい | 調べる、整理する、計画する（案を作る） | 読み書き |
| `ai/out/` | 最終成果物 `<成果物名>/`。基準文書と検証を伴う。予約名: `close.md` `stock/` `deliverable`（成果物の名前にしない。`deliverable/` は Area へ渡す専用） | 計画する（結論）、作る、確かめる | 読み書き |
| `ai/docs/` | 作業の記録だけ。`log.md`（現在状態）・`decisions.md`（判断）・`log-history.md`（経緯）の3つ（`room open` が雛形を置く） | 全活動の跡（何を決めたか） | 読み書き |
| `ai/records/` | 機械が書く実行記録（費用の推定、応答本文、部屋の操作のログ）、AI への指示の記録 | 作るの跡 | 読み書き |
| `_noai/` | 原本 `raw/`、対応表 `map/`、復元済みの成果物 `final/`、`mask.toml`、人だけの仮置き `user/`。マスクと復元は状態で決まる（`room/README.md`）。追跡しない | （AI の外） | 見えない |

種類別の置き場（type の考え方は上の節）:

| type | `ai/in/` | `ai/work/` | `ai/out/<成果物名>/` |
|---|---|---|---|
| `dev` | 参考資料、マスク済みの入力、渡された資料・チェックリスト、既存の手順書、対象環境の情報（OS、道具と版の一覧）、テスト対象と要求仕様 | 中間物、使い捨てのスクリプト、版ごとの下書き、レビュー版、試行のログ、試しのテスト、失敗の切り分け | 下の構成要素から、必要なものを選ぶ。構成は `dev-deliverable-guide.md` |
| `inv` | 人が渡した資料（調べて得たもの） | AI が集めた資料と抜粋、調べ途中の整理 | `report.md`（結論、出典、確認できなかった点） |

活動の流れの目安（拘束ではない）: `inv` は、調べる（`ai/in/` に渡された資料、`ai/work/` に集めた資料）→ 整理する（`ai/work/`）→ 結論（`report.md`）。`dev` は、調べた結果を受け取る（`ai/in/`）→ 整理・案づくり（`ai/work/`）→ 計画（`docs/`）→ 作る（`src/` `env/` `tools/`）→ 確かめる（`tests/` `report.md`）。判断は全体を通して `ai/docs/` に残す。

`dev` の構成要素（違いはサブディレクトリの組み合わせに現れる。選び方は `dev-deliverable-guide.md`）:

| 構成要素 | 用途 | 主な活動（目安） | 基準文書の正の向き |
|---|---|---|---|
| `docs/` | 基準文書。何を満たすか（要求）、どう作るか（機能）、どう使うか（運用） | 計画する（要求・設計を決める） | （基準文書そのもの） |
| `src/` | 本体。正本と派生物 | 作る | `docs/` の3文書（要求仕様・機能仕様・運用マニュアル）が兼ねる。正はソース |
| `env/` | 実行環境の定義（セットアップのスクリプト、コンテナ定義、版の固定）。実行の前提 | 作る（環境を整える） | 環境の要求仕様と運用マニュアルが兼ねる（機能仕様は省いてよい） |
| `tests/` | 基準文書の要求・検証項目に対応する検査（`env/` の確認スクリプトを含む） | 確かめる | `src/` が無く `tests/` だけのときは、テスト仕様が兼ねる。正はテスト対象の要求仕様（`ai/in/`） |
| `tools/` | 成果物を作る・動かす補助（変換・生成・実行・検査の束ね）。検査そのものは `tests/` | 作る（補助） | — |
| `report.md` | 実行の結果（`env/` の確認結果と版、`tests/` の実行結果） | 確かめる（結果の報告） | — |
| `docs/` だけ | 文書（手順書・仕様・設計・チェックリスト）が成果物 | 計画する | その文書自身の形は未決（下の「未決」） |

構成要素に当てはまらないものを置く逃げ道（2026-11-04）: 既存のディレクトリに混ぜず、`ai/out/<成果物名>/` の直下に名前を付けた専用のサブディレクトリを作って置く。置いたら、成果物の README に「どこに何があるか」を 1 行ずつ書く。Area へ渡すのは `ai/out/deliverable/` だけで、`<成果物名>` は Area 側の名前に使われない（Area では Project 名の下に入る）。

基準文書（`exmem/lessons/change-method.md`。変更の設計と検証の物差しになる、AI が読めるテキスト。人と AI の工程の境界）:

- 置き場は、成果物と同じ `ai/out/<成果物名>/`（全 type 共通）。`dev` の正の向きは上の表。`inv` は、問い（章立て）と品質条件（出典、未確認の明記）が兼ねる（`methods.md` の調査の Must）。
- `ai/work/` の下書きや使い捨てのスクリプトとは別物。`ai/docs/`（作業の記録）にも入れない。
- 前の Project の基準文書を次の Project に渡すときは、前の Project を `room close` で閉じ、`room open <次> --area <A> --from <前>` で引き継ぐ（下の「閉じた Project の引き継ぎ」）。
- 設計メモ（design、coding-rules）は `ai/docs/`。下書きは `ai/docs/` に入れない（`ai/docs/` を「作業の記録」の意味だけにする）。
- `ai/in/` は部屋では読み取り専用なので、AI が集めた資料は `ai/work/` に置く。
- `inv` と、`dev` の構成要素（特に `env/` と `tests/` だけの成果物）は、実測が無い叩き台。

## 開発リポジトリ（`repos:`。2026-10-31 ユーザーの決定）

`dev` で git のリポジトリを扱うときは、README の frontmatter に `repos:` を書く（`inv` は書かない）。

```yaml
repos:
  - url: git@github.com:<owner>/<repo>.git
    where: wsl      # wsl | win | linux。省略時は wsl。room が処理するのは wsl だけ
    branch: main
```

- clone の置き場は、部屋の `~/src/<repo>`（`<repo>` は url の末尾の名前から `.git` を除いたもの）。git で管理しない試作や一時のコードは `ai/out/<成果物名>/src/`。
- `room start` は、`claude` を起動するとき `~/src/<repo>` を `--add-dir` で渡し、`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` で追加ディレクトリの `CLAUDE.md` を読ませる。cwd は `/mnt/room/<Project>` のまま（案 A）。部屋に clone が無ければ注意を出して渡さない。
- AI は `git -C ~/src/<repo>` を使うのが望ましい（`cd` 後の git も、cwd が変わらず実害がなければ許容する。2026-11-04）。push は room に許さない（読み取り専用の deploy key）。人が部屋の外から行う。
- サーバーを使う Project は、README の frontmatter に `target:`（実行環境の記述。2026-11-01 ユーザーの決定）を書く。接続先が room の WSL でも別の Linux 機でも、書くのは「どこに、どう繋ぐか」だけで、違いは `via` の値だけ。`repos:` の `where:` とは別物（`repos:` は clone の置き場、`target:` は実行環境）。複数あれば `repos:` と同じ形で並べる。処理する側（`room.py`）は無い。

  ```yaml
  target:
    - name: dev-box     # ssh config の別名、または WSL のディストリ名。実ホスト名・IP・ユーザー名は書かない
      via: ssh          # ssh | wsl
      os: ubuntu-24.04
      note: 検証用サーバー
  ```

- サーバーへ room から SSH しない。サーバー上の作業は人が行い（`run:` のような項目は設けない）、結果を `ai/in/target/` に置く。置くもの: `env.md`（OS・言語・主なパッケージの版、接続の手順は別名だけ）、`run-YYYY-MM-DD.md`（人が実行した出力・エラーを貼ったもの）、秘匿値を抜いた設定ファイルのサンプル。置かないもの: 秘密鍵、パスワード、トークン、機密のホスト名。AI が集めた資料は `ai/work/` に置く（`ai/in/` は部屋では読み取り専用）。

## Project を立てる前の判断基準

`room open` を打つ前に、人が確かめる。

1. **対象を決める**: 候補（Area の README の「次の Project の候補」、`ai/docs/log.md` の Next Actions）から選ぶ。新しい題材なら、どの Area に属するかを決める（Area の上限は、works の規約に従う。暫定: 5件）。
2. **判断基準で検査する**:
   - 完了条件を、1文で書けるか（書けなければ Project ではなく Area）。
   - 見直し日を置けるか。成果物が1つに特定できるか（複数なら Project を分ける）。
   - 進行中の Project の上限を超えないか（暫定: 3件）。
3. **type を決める**（`dev` か `inv`。成果物で決める。結論と出典で保守しないなら `inv`、作って保守するもの（文書だけ、環境やテストだけの成果物を含む）なら `dev`。曖昧なら成果物の名前で決める。Area は既定値のヒント）。Project の名前は `<動詞か領域>-<主題>`（例: `learn-c-pool-allocator`。works 内で一意）。`dev` の Project は、`brief-work-types.md` の「開発」の項目を、**実装の前に**最初の `brief` で聞く。

README 本文（目的、成果物、計画へのリンク。雛形は `templates/project/README.template.md`）は、`room open` のひな形を人が埋める（部屋の AI は README に書けない。目的・完了条件の下書きは 6R として `ai/work/plan/` に書く。書き方は `room-context.md`）。

## 未決

- `inv` の基準文書の形。仮決め（2026-10-25、ユーザー。いまは決められない）: 別ファイルにせず、問い（`report.md` の冒頭 1 行）と完了条件の 1 行で足りるとする。`sample_inv` で 1 問の調査（約 4KB）は困らなかった。複数の問いや、結果を道具にする調査は未検証。
- `docs/` だけの `dev` 成果物の基準文書の形。仮決め（2026-10-25 に `sample_devdoc` で測った。ユーザー承認）: `ai/out/<成果物名>/docs/<名前>.md` の 1 本。冒頭に状況表（実環境での確認の有無）、元にした文書への言及（食い違ったら元が正）を置き、README は作らない。レビュー版（合否の項目）は `ai/work/`、手順書とスクリプトの食い違いの検査は `ai/work/` の使い捨て（成果物に含めない）。1 例のみ。`env/` だけ、`tests/` だけは 2026-10-25 に測った（叩き台のまま、実測は各 1 例）。
- Area が無い題材のときの、Area の作り方（基準: 終わりのない責任領域か）。
- 上限（Project 3件、Area 5件）の見直し。
- Project の構造（type は2種 `dev` `inv`、`ai/work/` の下書きの分離）の実測。`inv` と、`dev` の構成要素（`env/`、`tests/` だけ）は叩き台で、実測が無い。
- `target:` の書式と、`ai/in/target/` に置くものの一覧(`room-type-consolidation` の `docs/log.md` の Open Questions)。

## 閉じた Project の引き継ぎ（機能追加・改訂など、過去の資産を使う再作業）

2026-11-04 決定。閉じた（`room close` 済みで `archives/` にある）Project は開き直さない。再作業は、新しい完了条件を持つ別の Project にする（1 Project = 1 成果物、入れ子にしない）。

- 手順: `room open <新> --area <A> [--type] --from <前>`。<前> は同じ Area の `archives/<前>/`（`status: done`）。
- 写すもの（`ai/in/from-<前>/` の下に、`ai/` からの相対パスのまま）: `ai/out/` の成果物と `close.md`（`stock/` と `readme-draft.md` は除く）、`ai/work/plan/` の `status: 正式` の計画（6R など）。`_noai/` と `ai/ctx/` は写さない。
- 来歴: 写したファイルは manifest に確認済みで記録する（`origin` に元の Project・パス・ハッシュ）。AI の側から AI の側への写しなので、`--adopt` の関門（internal だけ）は通さず、external の Area でも使える。新しい Project の README に `from: <前>`、Area README の進行中の行に「← <前>」が付く。
- `brief 計画` は、`ai/in/from-<前>/` の `close.md`（完了条件の実測、暫定の見直し）と前の計画を読み、6R の「状況」に前回の到達点と残りを書き、完了条件は今回の差分で書く。
- 止まる条件（何も作らない）: <前> が archives に無い・`status: done` でない・別の Area、または写すものが無い。`ai/out/` と計画は git で追跡しないので、別の PC には無い。閉じた PC で実行する。
- `room reap` 済みでも使える（reap は会話履歴と作業用の一時ファイルだけを消す）。経緯を引くときは `room trace` が従来どおり使える。
- 開き直し（archives を projects に戻す）はしない。閉じ方を誤ったときは、人が git で戻す。
