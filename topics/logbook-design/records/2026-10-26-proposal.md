# 期限のあるナレッジの置き場と仕組み（叩き台）

> 注記（2026-10-26）: 置き場の名前は `ledger/` ではなく **`logbook/`** に決まった（仮決め）。この記録は議論の途中の版で、決定は `../docs/decisions.md` が正本。

- 日付: 2026-10-26（JST）
- 種類: 探索型の相談の叩き台。実装はしない。kit と workbase は未変更。
- 読んだもの: `README.md`、`docs/log.md`、`exmem/README.md` `AGENTS.md` `inbox/README.md`、`topics/AGENTS.md`、`topics/kit-growth/`（窓口、`inbox.md`、`records/`）、`workflow-kit/hooks.md` `docs-rules.md` `review-hook.md`、`exmem/lessons/accretion-without-pruning.md` `user-manual.md`。

## 0 結論（先に）

- 推奨は **案A（新設）を軽く作る形**: workbase 直下に期限つきの置き場を1つ作り、各ファイルに「現在の要約」と「明細」を持たせる。圧縮は log.md / log-history.md と同じ「縮めて、古い明細は git に任せる」。昇格は既存の `exmem/inbox/` → `integrate` の経路をそのまま使う。
- 新しく足す仕組みは、frontmatter の2項目（`review_by`、`budget`）と、`review` の入力1つだけ。新しいフックは作らない。
- 導入は今すぐでなくてよい。**11-29 の月次の振り返りで、週次の記録を1回だけ手で圧縮してみる**のを試行にし、その結果で置き場を作るかを決めるのが安い。

## 1 いま「期限のあるナレッジ」がどこにあるか（事実）

ユーザーが挙げた例は、すでに3か所に散っている。

| 例 | いまの置き場 | 大きさ | 増え方 | 畳む経路 |
|---|---|---|---|---|
| review の記録 | `docs/metrics/reviews.csv` | 0.5KB（1行） | 1回1行の追記 | なし |
| ユーザーの取扱説明書 | `exmem/lessons/user-manual.md`、`user-thinking-habits.md` | 18KB、31KB | 分析のたびに追記・上書き | なし（`updated` だけ） |
| 改善アイテムの規準 | `docs/alignment-baseline.md` | 5KB | 見直しのたびに上書き | 上書き（旧版は git） |
| 週報・月報 | `topics/kit-growth/records/retrospective-{daily,weekly,monthly}-record.md` | 28KB、24KB、5KB | 先頭に追記。「古い記録は消さない」 | なし |
| （参考）経緯 | `docs/log-history.md`、`docs/decisions.md` | 181KB、195KB | 追記 | なし（開始時に読まないだけ） |

読み取れること:

- 「半永久」のはずの exmem に、時系列で変わるもの（取扱説明書）が入っている。逆に、期限のある記録は kit-growth（kit の改善の Area）に寄っているが、取扱説明書や週報の業務側は kit の改善ではない。
- 足す経路はどれもあるが、畳む経路は `log.md` の 4KB 規則（→ `log-history.md` へ移す）だけ。`accretion-without-pruning` の「足すと畳むを対で」が、記録の層で守られていない。

## 2 置き場の案（3つ）

### 案A: workbase 直下に新しい置き場（名前は仮に `ledger/`）

```text
ledger/
├── README.md          # 窓口。型と寿命の規則、一覧（1件1行）
├── user-manual-log.md # 取扱説明書の観察の明細（期限あり）
├── retrospective-weekly.md
├── retrospective-monthly.md
└── reviews.csv        # docs/metrics/ から移す（任意）
```

- 良い点: exmem（半永久）と並ぶ「期限つき」の層が名前で分かる。triggers 索引の対象から外せる（短命なノートが引き当てを汚さない）。
- 悪い点: 置き場が1つ増える。2026-10-25 の決定「`records/` は2か所だけ」と、`kit-records-index.md` の「古い記録は消さない」を直す必要がある。

### 案B: `topics/kit-growth/records/` を「期限つきの記録」の置き場に広げる

- 良い点: 新しいディレクトリが要らない。週報・月報はもうここにある。
- 悪い点: kit-growth は「kit の育て方」の Area。取扱説明書や業務の週報が入ると、Area の意味がぼやける。トピックの規則（窓口 2KB、`log.md` 4KB）とも別の規則が混ざる。

### 案C: 置き場は作らず、exmem/lessons の中で frontmatter で区別する

- `horizon: short` と `review_by:` を足し、本文に `## Current`（いまの要約）と `## Log`（明細）を持たせる。
- 良い点: データの流れが一番少ない。昇格・降格は「frontmatter を変えるだけ」。
- 悪い点: exmem の定義（会話ログを溜めずに、知識として育てる）とぶつかる。`## Log` が溜まり、毎回読まれる lessons が太る。triggers の引き当てに短命の内容が混ざる。

### 比べると

| 観点 | A 新設 | B kit-growth を広げる | C exmem 内で区別 |
|---|---|---|---|
| データの流れの単純さ | ○（入口1つ、出口2つ） | ○ | ◎ |
| 既存の決定との衝突 | △（2件を直す） | △（1件を直す、Area の意味） | ×（exmem の定義） |
| 毎回読む量 | ○（開始時に読まない場所） | ○ | ×（lessons が太る） |
| 昇格・降格の分かりやすさ | ○（ディレクトリを跨ぐ） | ○ | △（frontmatter だけで見えにくい） |
| PC1 との相性 | ○（pull するだけ） | ○ | ○ |

## 3 運用（捨てる・圧縮・昇格・降格）

### ファイルの型（案A を前提に。B でも同じ）

各ファイルは2つの節を持つ。

- `## いま`（要約。予算あり。これだけ読めば使える）
- `## 明細`（日付つき、新しい順。開始時に読まない）

frontmatter に足すのは2つだけ。

```yaml
review_by: 2026-11-29   # 次に「捨てる/圧縮」を判断する日
budget: 8KB             # 超えたら判断の対象
```

### 判断の契機（新しいフックは作らない）

- `review_by` の到来、または `budget` の超過。
- 見る場は、すでにある **月次の振り返り**（`docs/log.md` の期日表、28日周期）。`review` の入力 3「警告の目安」に「期限切れ・予算超過の ledger の件数」を1行足すだけにする。

### 4つの操作

| 操作 | 何をするか | 使う既存の仕組み | 決める人 |
|---|---|---|---|
| 捨てる | ファイル（または明細の古い区間）を削除。理由を1行、`docs/log-history.md` に | git の履歴、`log-history.md` | ユーザー |
| 圧縮 | 明細の古い区間を `## いま` の要約に畳み、明細から消す。消した区間の範囲（日付）だけを要約に残す | `log.md` → `log-history.md` の 4KB 規則と同じ型。ただし移し先は git（別ファイルを作らない） | AI が案、ユーザーが承認 |
| 昇格 | 期限が切れても使える原則・落とし穴を `exmem/inbox/` にメモで出し、`integrate` で lessons に入れる。ledger 側には `→ [[lesson 名]]` を残す | `stock` の書式と `integrate`（そのまま） | ユーザー（`integrate` の承認） |
| 降格 | lessons の時系列で変わる部分（観察、件数、最新の傾向）を ledger に移し、lesson には原則だけを残して `[[ledger の名前]]` を張る。丸ごと古くなった lesson は、これまでどおり `status: superseded` | `status: superseded` の規則 | ユーザー |

圧縮を git に任せる理由: 別の「アーカイブ」ファイルを作ると、`accretion-without-pruning` の「畳む作業の副産物が肥大の原因になる」をそのまま踏む。

### 例で当てはめると

- **取扱説明書**: `user-manual.md` の Principles と Decisions は exmem に残す。分析のたびに増える Facts（観察）と、`user-thinking-habits.md` の分析の明細を ledger に降格。月次で、繰り返し出た傾向を1行にして lessons に昇格する。
- **週報・月報**: 週次は月次で圧縮（その月の週次4回分を月次の `## いま` に畳み、週次の明細を消す）。月次は四半期か半年で圧縮。施策のうち定着した原則は昇格。
- **review の記録**: CSV は行が小さいので、捨てる・圧縮はしばらく不要。100行を超えたら、月ごとの集計行に畳む。
- **改善の規準**（`alignment-baseline.md`）: いまの上書き運用で足りる。ledger に移すかは任意（期限より「版」の性質が強い）。

## 4 データフロー（文章で）

```text
作業・会話
  ├─(stock)──────────────→ exmem/inbox/ ─(integrate)→ exmem/lessons/   ［半永久］
  │                                                     │  ↑
  │                                              降格   │  │ 昇格（inbox 経由）
  │                                                     ↓  │
  └─(wrap / 振り返り / review が追記)──→ ledger/<名前>.md ［期限つき］
                                             │
                          月次の振り返りで判断（review_by・budget）
                                             ├─ 捨てる → 削除（git に残る）
                                             └─ 圧縮  → 「いま」に畳む（明細は git に残る）
```

- 入口は、いま記録を書いている手順（`wrap`、振り返り、`review`）のまま。書き先のパスが変わるだけ。
- 出口は2つ（削除、exmem への昇格）。昇格は必ず `exmem/inbox/` を通る。lessons へ直接書かないので、`integrate` の照合がそのまま効く。
- 降格だけが lessons → ledger の逆向き。`integrate` の権限（workbase だけで rw）と同じく、workbase で行う。
- PC1 は ledger を pull して読むだけ。書くのは PC2 とモバイル（いまの kit-growth と同じ）。

## 5 推奨と導入時期

- **推奨**: 案A（新設）。理由: 例のうち2つ（取扱説明書、業務の週報）が kit の改善ではなく、案B だと Area の意味が崩れる。案C は exmem の定義を壊す。置き場が1つ増える代わりに、exmem と kit-growth の両方が本来の意味に戻る。
- **導入時期の目安**（数字は暫定。根拠なし）:
  1. いますぐは作らない。
  2. **11-29 の月次の振り返り**で、週次の記録（いま 24KB）を、置き場を変えずに1回だけ手で圧縮してみる。かかった手間と、消して困ったことを見る。
  3. 困らなければ、次の条件のどちらかで案A を入れる: 期限つきのファイルが3種類以上そろったとき、または workbase の大きな整理（room、フック、索引）が落ち着いたとき。
- 入れるときに直すもの: `topics/AGENTS.md` の「`records/` は2か所だけ」、`kit-records-index.md` の「古い記録は消さない」、`review-hook.md` の入力 3 に1行、`find_knowledge.py` の対象から ledger を外すか。

## 6 ユーザーに決めてほしいこと（急がない）

1. 置き場: 案A / B / C のどれで進めるか（推奨 A）。
2. 試行: 11-29 の月次で、週次の記録を1回圧縮してみるか（推奨: やる）。
3. 取扱説明書の降格: Facts と分析の明細を exmem から出すことに違和感がないか。
4. 名前: `ledger/` は仮。ほかに `logbook/` `seasonal/` など（短く、`records/` と紛れない名前がよい）。
