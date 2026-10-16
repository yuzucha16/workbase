# 作業ログの経緯（log-history）

## Log

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
