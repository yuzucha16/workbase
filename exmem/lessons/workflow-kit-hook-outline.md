---
type: knowledge
title: フック手順書の章立て
status: active
tags:
  - workflow
  - knowledge-management
  - ai/claude
  - harness
aliases:
  - workflow-kit-hook-outline
triggers: [章立て, hook-common, check-hook-outline, 共通部, 固有部, 手順書の章]
created: 2026-10-08
updated: 2026-10-27
---

# フック手順書の章立て

設計の背景は [[workflow-kit]]（2026-10-27 に、追記の節を切り出した）。

複数のフック手順書（`*-hook.md`）の章立てを、共通部と固有部に分けて揃えたときの考え方。今の章立ての規則の正本は kit の `hook-common.md`（点検は `tools/check-hook-outline.ps1`）。一般的な進め方は [[abstract-concrete-matrix-review]]。2026-10-15 に、この節の Decisions・Facts・Open Questions・Next Actions を畳んだ（kit の正本と重なるか、置き換わった記録のため。全文は畳む前のコミット `33e9fe3` の、このファイルにある）。

### Principles（章立て）

- 複数の手順書の章立てを揃えるときは、既存の章を並べ替えず、足りない章を挿入して揃える。理由: 「上の」「下の」など位置を指す参照が、並べ替えで壊れる。
- 揃える対象は、全体で共通の章（共通部）に絞り、共通部の存在と相対順序だけを一致させる。固有の章は置き場所を自由にする。理由: 固有の章まで厳密に揃えると、該当なしの章（「なし」）が増え、文書が肥える。
- 章立ての規則は、機械で点検できる形（存在と順序）にしておく。理由: 人の目では、フックが増えるたびに崩れやすい。

## Related

- [[workflow-kit]]
