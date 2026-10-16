# kit-growth: 現在状態

更新: 2026-10-16

## 状態

- 経路は整備済み: 受け皿 = このトピック、入力 = `inbox.md`、見直し = `review`（inbox の未選別と、動いているトピックを見る）、`improvements.md` は凍結。
- 自動採用（`wrap-hook.md` の節）は、2026-10-15 に畳んだ（判定を前倒し）。
- cwd（起動する場所）を明文化した（`4997f7a`）: `AGENTS.md` の単位で起動、上の階層からの「続き」は AI が読みに行く、読む順番は 窓口 → `log.md`、部屋は例外、`wrap` は作業した単位の `docs/` を既定に。
- トークン節約（会話を切る・出力を絞る）の対応を kit と exmem に入れた。`review` が星取り表 `workflow-kit/token-matrix.md`（4観点）で自己採点する。基準値は 切る 16・絞る 24・予算 38・外部化 25、合計 103（`6bd1a2a`）。初回の採点し直しも 103（`70b8e22`）。
- `again`（言い直し）と `gap`（漏れ）の記録を廃止した（2026-10-16、`139091c`）。言い直しがほぼ起きず、`start` の利用も減ったため。`goal_change` は残した。topic-workflow の kit 取り込みの時機は要再判断（`topics/topic-workflow/topic-workflow-next-steps.md` の5）。
- `wrap` の空回りを減らした: workbase の `AGENTS.md` に「wrap の記録先」（トピック外の kit 等の変更は kit-growth の `docs/`、遠回りの「少し」「大きく」は `inbox.md`）を定め、`wrap-hook.md` の手順1がリポジトリの既定の対象を見るようにした（ユーザーの選択。案3「依頼文だけ」は見送り）。

- 3 リポジトリ（works、resources、dotfiles）の規則を揃えた（2026-10-16。一律に kit を正とはしない）。`docs-rules.md` を読む時機を「`docs/` 更新時とコミット・push の前」に統一、階層化の規則（上段は表引き、下段に詳細）を追加、機密の項は `review` の入力 6 に移した、`review` の入力 8（リポジトリ間の整合の表）を追加、workspace 雛形の写しを除去（`2156d92` `2a35149` `3cdeeb1` `286d714`）。

## Next Actions

0. 入力 8 は 2026-10-16 に初回を実施済み。deny 設定は dotfiles に入れ、凍結の対として 3 つの `AGENTS.md` の禁止コマンドの列挙を畳んだ（ユーザーの決定）。残るギャップは、`pre-push`（works の 11-08 の判定の項目⑧。git 周りは後日まとめて見直す）、works の `docs/log.md` の超過、dotfiles の `docs/setup/` の案（`topics/dotfiles-boundary/`）との置き場の整合。規則を足したので、凍結の対（畳むもの）は機密の項で足りたが、入力 8 の分は未対（次の `review` で畳む候補を挙げる）。

1. PC1 の印象を `inbox.md` に入れ始める（モバイル。随時）。
2. `start` のモード（確定型・探索型）を次の2〜3セッションで試し、`review` で `goal_change` を見る（`again`・`gap` は 2026-10-15 に廃止）（improvement-methods の close で受け継いだ。詳細は `exmem/lessons/session-goal-modes.md`）。
3. `token-matrix.md` の初回の採点し直しは済んだ（`70b8e22` で 103、下がった列なし）。入力「重い会話」は、会話履歴の集計がある端末の `review` で見る。見送った2件（切る目安の数値、`lessons/` の字数の目安）は、その結果を見て決める。
4. topic-workflow の kit への取り込み（docs-rules の「トピック」の節）が済んだら、`topics/` の型の記述をそちらへ寄せる。

## Open Questions

- Area の担い手: topic-workflow の Q3 の会話で、AI は「kit の改善という Area は kit 本体・`improvements.md`・`review` が担う」と述べたが、本トピックの決定は「トピックが担う」。後者（ユーザーの合意）を採った。
