# 判断の記録（decisions）

## Decisions

### 【この件】type を `dev` と `inv` に集約した（2026-10-24）

- 正本は workbase 直下の `docs/decisions.md` の同日の項（決めたこと、根拠、却下案）。ここには重ねて書かない。
- 論点8件と仮決めの経緯は [[room-type-consolidation-notes]]。

### 【この件】最初の実利用を受けた決定（2026-10-25）

- `room open` が `ai/docs/` に `log.md` `decisions.md` `log-history.md` の雛形を置く（他の単位と同じ 3 つ）。根拠: ユーザー「room open がひな形をおく」「他と同じように、log, log-history, decisions の3つ」。
- `inv` の基準文書は「問い＋完了条件の 1 行で足りる」とする。**仮決め**（ユーザー「これは仮決め。いまは決められないため」）。
- `docs/` だけの `dev` は測らない（ユーザー「もう使わないので測定しなくても良いかな」）。`env/` だけ、`tests/` だけは、最初に使うときに測る。
