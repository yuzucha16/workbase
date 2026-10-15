# 大きなトピックを、セッションと端末をまたいで進める型（汎化の案）

- 作成: 2026-10-15（Claude Projects のスレッドで作った案を、そのまま移した）。決定と次の一手は [[topic-workflow-handover]] と [[topic-workflow-next-steps]]。この文書は分析と案の詳細（決定前の推奨を含む）。
- 読んだもの: `topics/` の全18ファイル（約14万字）、ルートと exmem の `AGENTS.md`、`workflow-kit/`（README、hooks、docs-rules、stock、wrap ほか）、`exmem/lessons/` の session-handoff・accretion-without-pruning・para-operations・session-goal-modes、Claude Projects の共有フォルダの過去の議論メモ。

## 0. 3行で

1. `topics/` の話題ディレクトリは、実質「**クラウドから届く場所に置いた `docs/`**」になっている。kit にある `docs/` の型（log・decisions・log-history）と、Project の寿命（open / close）を**そのまま流用**すれば、新しい仕組みはほぼ要らない。
2. 試行錯誤の負債の中心は「**状態の写しが4〜5か所にある**」ことと「**毎回読む文書の予算が無い**」こと。人が覚えられない、モバイルで読めない、の原因もここ。
3. 進め方は「案に合意 → 小さい話題で1回試す → 大きい話題を畳み直す → 2回使えたら kit に取り込む（足すなら畳む）」。

---

## 1. いまの方式の分析

### 1-1. うまくいっていること（残す）

| # | 観察 | 根拠 |
|---|---|---|
| A | 話題ごとのディレクトリで、状態をリポジトリに置き、会話に置かない | `topics-index.md`、`session-handoff.md` の原則 |
| B | 項目ごとに「場所（モバイル / PC）」を明記し、分担している | `ai-room-roadmap.md` の「主な場所」列 |
| C | 1項目ずつ、未決は1問ずつ聞く | `ai-room-start-here.md`「作業の約束」 |
| D | 決定に「ユーザーの発言」を根拠として付ける | `dotfiles-boundary-handover.md`「決めた方法」列 |
| E | 途中で知識を inbox → lessons へ流している（話題が終わる前に） | `improvement-methods` は6本を lessons に統合済み |
| F | 出口がある（反映したらディレクトリを消す） | index の「使い方」 |
| G | 実機で確かめた事実と、推測を分けている | 各 handover の「PC での確認の結果」「注意（推測を含む点）」 |

### 1-2. 決定負債・改善点（直す）

| # | 問題 | 根拠 | 影響 |
|---|---|---|---|
| 1 | **状態の写しが多い**。同じ項目の状態が roadmap の表、next-steps の TODO、各 handover、index の「状態」列、start-here の「ローカルの状態」にある | ai-room の R1 の状態は少なくとも4か所 | 更新漏れ。どれが正しいか人が分からない |
| 2 | **毎回読む文書に予算が無い**。next-steps が 34KB・210行、start-here が 7KB、話題全体で 13万字 | `wc -c` | モバイルで読めない。セッションの先頭が重い |
| 3 | **next-steps が追記型の経緯を抱えている**（実測の結果、1巡目・2巡目の問題…） | next-steps の「1」「2」「3」節 | docs-rules の「log と log-history の分割」を自分で破っている |
| 4 | **引き継ぎの置き場の規則が3つあり、食い違う** | ① `exmem/AGENTS.md` と docs-rules「使い捨ての環境」: lessons の Open Questions / Next Actions、② index: `topics/`、③ Claude Projects の共有フォルダ（git 外） | どこを見ればよいか毎回迷う |
| 5 | **引き継ぎの型が2つある**（session-handoff の「3行の依頼文」と、start-here の窓口） | 両ファイル | 型の正本が無い |
| 6 | **名前が実態とずれている**。PC のセッションも書くし、モバイルに限らない | 「PC のセッション」が書いた commit が多数 | 何の置き場か直感で分からない |
| 7 | **話題の間の依存が追えない**。R5 は「別セッションのディレクトリ構造の議論と合流してから」保留 | roadmap の 5 | 保留が忘れられる |
| 8 | **出口が1回も使われていない**。3話題とも削除前。improvement-methods は残り1項目 | index | 足す経路だけが動く（accretion-without-pruning の再発） |
| 9 | 機密を含む Area（業務）は、この方式に乗れない | workbase は公開前提。Vault は remote なし | Areas に横展開するときの壁 |

---

## 2. 汎化の案

### 2-1. 中心の考え: 「トピック」= 寿命の長い作業ディレクトリ

新しい概念は作らず、kit の既存の部品の組み合わせとして定義する。

| いまの mobile-session | 対応する kit の部品 |
|---|---|
| 話題ディレクトリ | `init` を入れた作業ディレクトリ |
| start-here（窓口） | `AGENTS.md` の「読む順番」＋ `README.md` |
| roadmap（状態の正本） | `docs/log.md`（現在状態と Next Actions。4KB） |
| handover の「決まったこと」 | `docs/decisions.md`（【汎用】【案件】【この件】） |
| next-steps の実測・経緯 | `docs/log-history.md`（開始時に読まない） |
| 話題を作る / 消す | `open` / `close` |
| セッションの開始・終了 | `start` / `wrap`（どの端末でも同じ） |
| 途中のナレッジ化 | `stock`（【汎用】を inbox へ） |

これで、「どこに何を書くか」の規則は docs-rules が1本で持つ。トピック固有の規則は数行で済む。

### 2-2. トピックのディレクトリの形（案）

```text
topics/<トピック名>/
  README.md        窓口（人とAIの入口。予算 2KB = スマホ1〜2画面）
  docs/log.md      状態の正本（項目表・次の一手・ユーザー待ち。4KB）
  docs/decisions.md 決定の正本
  docs/log-history.md 経緯（読まない。検索だけ）
  notes/           詳細の設計ノート（必要なときだけ読む）
```

窓口 `README.md` の固定の見出し（**人が30秒で読める**ことを目的にする）:

1. **何の取り組みか**（3行）
2. **ゴール（完了条件）**（1文。書けなければ Area 型。2-4）
3. **いまどこ**（1行。詳細は log.md）
4. **あなた待ち**（ユーザーの決定待ちを最大3件。無ければ「なし」）
5. **次の一手**（1つ。場所つき: どこでも / PC / モバイル）
6. **読む順**（AI 向け）と、**リポジトリに無いローカルの状態**

状態の値は log.md だけに置き、窓口は「いまどこ」の1行だけを持つ（写しは1か所・1行に制限）。

### 2-3. 4つの観点への答え

| 観点 | 案 |
|---|---|
| 他のセッションに引き継ぐ | 新しいセッションへの依頼は「`<トピック名>` の続き」の1行。AI は窓口 → log.md の順に読む。session-handoff の3行の依頼文は、この1行に畳む |
| 問題・課題・決定を残す | 課題は log.md の Open Questions、決定は decisions.md。決定は「ユーザーの発言」を根拠に持つ（既存の規則どおり）。保留は理由と「再開の条件」を書く（依存先のトピック名つき。負債7） |
| 途中で stock する | 項目が1つ終わるごとに、【汎用】の決定を `stock` で inbox へ。終わりにまとめない。`→` の有無で運んだかが分かる（既存の規則） |
| workflow への取り込み | kit に足すのは「トピック」の節を1つ（docs-rules）と、窓口の雛形1つだけ。代わりに畳むもの: `topics-index.md` の使い方、session-handoff の依頼文の型、docs-rules と exmem/AGENTS の「引継ぎは lessons の Open Questions」の記述（負債4・5） |
| モバイル・PC をまたぐ | トピックは workbase（GitHub）に置く＝両方から届く。各項目に場所を付ける（B を規則化）。Claude Projects の `notes/` は「議論の下書き」、確定したらトピックへ移す、で役割を分ける（負債4） |

### 2-4. Areas への横展開

> **Q3 で置き換え済み**: ai-workspace-boundary は Project 型（初版で close）に決まった。下の ai-workspace-boundary を Area 型とする記述は、決定前の推奨。

PARA の定義（para-operations）では、Area = 期間未定の案件、Project = 期限とゴールのあるタスク。トピックも同じ2型に分けられる。

| 型 | 例 | 出口 |
|---|---|---|
| Project 型（完了条件を1文で書ける） | improvement-methods、dotfiles-boundary | `close` で lessons・kit・guides に反映して、ディレクトリを消す |
| Area 型（書けない。続く） | ai-workspace-boundary（項目が増え続けている） | 消さない。代わりに、項目ごとに Project 型の子を切り出し、Area 側は窓口と decisions だけを持つ |

ai-workspace-boundary は、実態が Area 型なのに Project 型の置き場（消す前提の mobile-session）にいる。だから膨らむ。roadmap の8項目を、それぞれ子のトピック（または Area の項目表の行）にすると、1回に読む量が項目1つ分に減る。

**機密のある業務の Area（負債9）**: 同じ型を Vault の `areas/` に入れる。違いは「モバイルから届かない」ことだけ。【汎用】の部分は、既存の隔離ソースの運び方（docs-rules）で workbase に出す。モバイルで続けたい公開可の部分は、別トピックとして workbase に切り出す。

### 2-5. 肥大化を防ぐ規則（人が覚えられない問題への対策）

- **予算**: 窓口 2KB、log.md 4KB。超えたら、log-history へ移すか、子に分ける（決める側は AI。報告に1行）。
- **項目は最大8**（roadmap の実績）。9個目を足すときは、1つ畳むか子に分ける。
- **出口の点検**: `review`（週1回）が、30日更新の無いトピックと、ゴールを満たしたのに残っているトピックを1行で挙げる。
- **トピック一覧**（index）は1トピック1行だけ。状態は書かず、窓口へのリンクと「あなた待ち」の件数だけ。

---

## 3. ゴール（この取り組みの完了条件）

1文: **新しいセッションに「`<トピック名>` の続き」と言うだけで、モバイルでも PC でも再説明なしに再開でき、終わったトピックは lessons・kit に反映されて消える状態にする。**

測り方（既存の `events` の記録を使う。新しい指標は足さない）:

| 指標 | 目安 |
|---|---|
| 再伝達 `again`（再説明） | 再開1回あたり 0〜1件 |
| 漏れ `gap`（忘れていた決定） | 再開1回あたり 0件 |
| 窓口の大きさ | 2KB 以下（スマホで1〜2画面） |
| 人の確認時間 | 窓口を読んで30秒で「いまどこ・次・自分待ち」が言える（主観でよい） |
| 出口 | 試行の期間中に、トピックを1つ以上 `close` して削除できた |

---

## 4. 進め方（案）

ユーザーの方針（1項目ずつ、1問ずつ、kit は承認の後）に合わせる。

| 段階 | 内容 | 場所 | 完了の目安 |
|---|---|---|---|
| 1 | この案の論点を、1問ずつ決める（下の5問） | どこでも | 5問が decisions に入る |
| 2 | **小さく試す**: improvement-methods（残り1項目）を新しい型で `close` する。出口の手順を1回通す | どこでも | ディレクトリが消え、lessons に残る |
| 3 | **大きいものを畳み直す**: ai-workspace-boundary を Project 型（Q3）のまま docs の型に組み替える。13ファイル → 窓口・log・decisions・notes。state の写しを消す。初版（roadmap 1〜7）で close | モバイル（文書）＋ PC（ローカルの状態の確認） | 窓口 2KB、log 4KB に収まる。再開を2回試して again・gap を数える |
| 4 | dotfiles-boundary を新しい型で進めるか close する | PC | 同上 |
| 5 | **kit へ取り込む**（2回使えてから。accretion-without-pruning の「二度目から規則化」）。足す: docs-rules の節1つ、窓口の雛形1つ。畳む: 1-2 の負債4・5の記述と index の使い方 | どこでも | 足した字数 ≦ 畳んだ字数（規模の凍結。判定日 2026-11-08 と合わせる） |

---

## 5. ユーザーに決めてほしいこと（1問ずつ聞く。推奨つき）

1. **置き場の名前**: `mobile-session/` → `topics/` に改名するか。推奨: 改名する（PC も書く。端末を問わないことを名前で示す）。
2. **中身の型**: トピックの中を kit の `docs/` の型（log・decisions・log-history）にそろえるか。推奨: そろえる（新しい規則がほぼ要らない）。
3. **Area 型の扱い**: ai-workspace-boundary を Area 型として残し、子に分けるか。推奨: そうする。
4. **Claude Projects の `notes/` の役割**: 「下書き。確定したら repo のトピックへ移す」でよいか。推奨: それでよい（notes は git に無く、PC の Claude Code から見えないため）。
5. **最初の試行**: improvement-methods の close から始めるか。推奨: そうする（一番小さく、出口を1回通せる）。

決まったこと（Q1〜Q5）は [[topic-workflow-handover]] が正本。

## 6. 推測を含む点

- 「30秒で読める」「2KB」は目安で、実測の裏づけは無い（仮説）。段階3の再開2回で確かめる。
- ai-workspace-boundary を Area 型と見なすのは、項目が増え続けている観察からの推測。ユーザーの見方と違えば、3問目で直す。
- Claude Projects の `notes/` に、PC の Claude Code からは届かない、というのは、この環境の構成からの推測（未確認）。
