# 引き継ぎ: 大きなトピックを、セッションと端末をまたいで進める型

- 作成: 2026-10-15（Claude Projects のスレッドでの検討。モバイル）。
- 読む順: この文書 → [[topic-workflow-next-steps]]。分析と案の詳細は [[topic-workflow-proposal]]。
- 状態: 5問の方針が決まった。**実行は、PC2 で並行中の ai-workspace-boundary の動作確認が終わってから**（ユーザーの指示）。ユーザーは、[[kit-growth-handover]] などと合わせて、別の場所でまとめて対応する予定。

## 目的

`mobile-session/` での進め方（話題ディレクトリ、handover・next-steps・roadmap・窓口）を分析・一般化し、AI との作業の進め方の一サンプルにする。横展開できる部分は workflow-kit に取り込む。

ユーザーが重視する観点: ① 大きなトピックを他のセッションに引き継ぎながら進める、② 問題・課題と決定を残す、③ 途中で知識を部分的に stock する、④ workflow への取り込み、⑤ モバイルと PC をまたいだ共有。

背景（ユーザー）: リポジトリのある PC を常に触っているわけではない。セッションが長くなりがち。再説明と失念を防ぎたい。反面、トピックが肥大化して人が覚えていられない（モバイルで文が読みづらいことも理由）。

## 分析の要点（詳細は proposal の 1）

- 話題ディレクトリは、実質「クラウドから届く場所に置いた `docs/`」。kit の log・decisions・log-history と open / close を流用できる。
- 負債の中心: 状態の写しが4〜5か所（roadmap、next-steps の TODO、各 handover、index の状態列、窓口）。毎回読む文書に予算が無い（ai-room-next-steps は 34KB）。引き継ぎの置き場の規則が3つあり食い違う。出口（削除）が1回も使われていない。

## 決まったこと（ユーザーの発言。2026-10-15）

| # | 内容 | 発言 |
|---|---|---|
| Q1 | `mobile-session/` を `topics/` に改名する | 「する」 |
| Q2 | トピックの中身を kit の `docs/` の型（log・decisions・log-history）にそろえる。フックの再利用を優先する | 「揃える」「いまはフック再利用を優先して docs と同じで良い」 |
| Q3 | AI 作業部屋（ai-workspace-boundary）は Project 型。完了条件は「roadmap の 1〜7 が PC で確認済み」。8 以降は新しい Project か改善の1行にする。子には分けない | 「はい、すっきりした」（AI の意見「Area はもうある。改善の Area を別に作ると状態が二重になる」への同意） |
| Q4 | Claude Projects の共有フォルダは、議論の下書きの置き場。確定したらリポジトリのトピックへ移す（リポジトリの旧用語 `notes/`（今の `works`）とは別物） | 「はい」 |
| Q5 | 最初の試行は、improvement-methods を新しい型で close すること | 「はい」 |
| 時機 | 改名・組み替えなどの実行は、ai-workspace-boundary の動作確認が終わってから | 「実行タイミングはあちらの進捗に揃えさせて」 |

## 改善ネタ（後で検討）

- handover・next-steps・roadmap は、名前と内容が一致していて、log・decisions より分かりやすい（ユーザーの評価）。いずれ両方の良いところを取る。いまはフックの再利用を優先して docs の名前にする。

## 食い違い（まとめて対応するときに解く）

- Q3 の会話で AI は「kit の改善という Area は、`workflow-kit/` 本体・`improvements.md`・`review` が担い、別の Area を作らない」と述べた。同日の [[kit-growth-handover]] は「改善を Area 型のトピック `topics/kit-growth/` にし、`improvements.md` は凍結」と決めている。AI 作業部屋を Project 型で閉じる点は両方で一致。**Area の担い手は kit-growth の決定（トピック）を優先するのが自然**（AI の推測。未確認）。
