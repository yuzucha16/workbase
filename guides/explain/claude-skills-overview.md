# Claude スキル（Agent Skills）調査メモ

調査日: 2026-10-16。出典は Anthropic の一次情報を優先し、第三者の情報はそう明記する。【推測】と書いた箇所は、出典で確認できていない筆者の解釈。

## 0. 3行で表すと

1. スキルは、手順・知識・スクリプトを入れた `SKILL.md` のフォルダで、Claude に「現場のやり方」を教える仕組み。
2. 普段は名前と説明だけを持ち、必要なときだけ本文を読むので、文脈を圧迫せずに大量に持てる。
3. 2025-12 にオープン標準になり、Claude 以外のエージェントにも広がった。ただしコードを実行できるので、出所の確認が必須。

## 0.5 ひとことで

スキルは「`SKILL.md` を入れたフォルダ」。中身は手順・知識・スクリプト・資料で、Claude は**必要になったときだけ**読み込む。最初は名前と説明（1スキル約100トークン）だけを常に持ち、本文や付属ファイルは関係するタスクのときに開く（段階的開示 = progressive disclosure）。

> "organized folders of instructions, scripts, and resources that agents can discover and load dynamically"（[Anthropic Engineering, 2025-10-16](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)）

## 1. 生まれた経緯

| 日付 | 出来事 | 出典 |
|---|---|---|
| 2025-09 頃 | claude.ai のファイル作成機能（docx / xlsx / pptx / pdf）が、裏側ではスキルで作られていた。発表時にこれらが公開スキルとして出された | Simon Willison（第三者）[2025-10-16](https://simonw.substack.com/p/claude-skills-are-awesome-maybe-a)。機能の開始月は【未確認】 |
| **2025-10-16** | 「Introducing Agent Skills」発表。claude.ai（Pro / Max / Team / Enterprise）、Claude Code、Claude API（`/v1/skills`、Code Execution Tool が前提）、Agent SDK で同じ形式が使えると告知 | [claude.com/blog/skills](https://claude.com/blog/skills)、[Engineering ブログ](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) |
| 2025-12-12 頃 | OpenAI が ChatGPT（Code Interpreter 内の `/home/oai/skills`）と Codex CLI（`~/.codex/skills`）で同じ形式を試験的に採用 | Simon Willison（第三者）[2025-12-17](https://simonw.substack.com/p/openai-are-quietly-adopting-skills) |
| **2025-12-18** | Agent Skills を**オープン標準**として公開（[agentskills.io](https://agentskills.io)）。同時に、組織単位のスキル管理（Team / Enterprise の管理者が一括で有効化）と、パートナー製スキルのディレクトリを追加 | 上記 2 記事の追記、[gihyo.jp 2025-12](https://gihyo.jp/article/2025/12/agent-skills-to-open-standard) |
| 時期は【未確認】 | Claude Code で、カスタムスラッシュコマンド（`.claude/commands/`）がスキルに統合された。古い置き場も動き続ける | [Claude Code Docs: Skills](https://code.claude.com/docs/en/skills) |

## 2. 解決したかった問題

公式の言い分は次の3点に集約できる。

1. **能力はあるが、現場の手順と文脈がない。** "real work requires procedural knowledge and organizational context"（[Engineering ブログ](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)）。新人に渡すオンボーディング資料のように、会社やチームのやり方を渡す手段が要った。
2. **用途ごとに専用エージェントを作る非効率。** 個別のエージェントを作る代わりに、汎用エージェントへ「組み合わせ可能・持ち運べる」専門知識を足す方式にした（同上）。
3. **コンテキスト（トークン）の圧迫。** 全部をシステムプロンプトに入れると窓が埋まる。段階的開示で、持っておけるスキルの量を実質無制限にした（"effectively unbounded"、同上）。
   - レベル1 メタデータ: 常時、約100トークン/スキル
   - レベル2 `SKILL.md` 本文: 発動時、5k トークン未満が目安
   - レベル3 付属ファイル・スクリプト: 必要時のみ。スクリプトはコードを読まず、出力だけが文脈に入る
   （[Platform Docs: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)）

あわせて、**決まった処理はトークン生成よりコードの方が確実で再現性がある**ので、スクリプトを同梱できるようにした（Engineering ブログ）。

## 3. 与えた影響

- **業界の共通形式になった。** agentskills.io の採用例には GitHub Copilot / VS Code、Cursor、Gemini CLI、OpenAI Codex / ChatGPT、JetBrains Junie、OpenHands、Goose、Kiro、Databricks、Snowflake などが並ぶ（[agentskills.io](https://agentskills.io)、2026-10-16 閲覧）。MCP に続く、Anthropic 発の事実上の標準になった。
- **「MCP より大事かもしれない」という評価。** Simon Willison は、MCP がツール定義だけで数万トークンを食うのに対し、スキルは数十トークンで済み、Markdown とスクリプトだけの単純さが LLM 向きだと論じた（[2025-10-16](https://simonw.substack.com/p/claude-skills-are-awesome-maybe-a)、第三者の意見）。
- **Claude Code の拡張機能の整理。** スラッシュコマンドがスキルに吸収され、公式が「最も柔軟な拡張」と位置づけた（[Extend Claude Code](https://code.claude.com/docs/en/features-overview)）。CLAUDE.md に書いていた手順を、スキルへ移すよう公式が勧めている。
- **配布と統制の仕組みが育った。** プラグイン・マーケットプレイス経由の配布、組織単位の管理、Enterprise のスキル内容スキャン（[Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)）。
- **新しい危険の面ができた。** スキルはコードを実行できるため、公式は「信頼できる出所のものだけ使い、ソフトのインストールと同じ注意で監査せよ」と警告している（同上）。

## 4. 現在の役割（2026-10 時点）

Claude Code の公式整理では、拡張機能は次のように役割分担されている（[Extend Claude Code](https://code.claude.com/docs/en/features-overview)）。

> CLAUDE.md は常時の文脈、**スキルはオンデマンドの知識とワークフロー**、MCP は外部接続、サブエージェントは隔離、フックは自動化。

スキルの中身は2種類ある。

- **参照型**: API スタイルガイドなど、必要なときに読む知識
- **実行型**: `/deploy` のように、呼べば手順を実行するワークフロー

製品ごとの扱い（[Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)）:

| 製品 | 使えるスキル | 共有範囲 |
|---|---|---|
| claude.ai / Cowork | 既製（docx / xlsx / pptx / pdf）＋カスタム（zip をアップロード） | Docs 上は個人単位。ただし 2025-12-18 に組織管理が追加されており、Docs の記述と食い違う【要確認】 |
| Claude API | 既製＋カスタム（`/v1/skills`、`container` で `skill_id` を指定） | ワークスペース単位 |
| Claude Code | カスタム（既製の文書スキルは無し） | 個人・プロジェクト・プラグイン |

**製品間で同期しない。** あるところに入れたスキルは、別の製品には別途入れる必要がある。

## 5. 具体例（著名なスキル）

GitHub の星の数は **2026-10-16 に GitHub の検索 API で取得**した値。星の数は人気の指標であって、品質や安全性の指標ではない。

### 5.1 星の数トップ5（スキルを主体とするリポジトリ）

| 順位 | リポジトリ | 星 | 何をするか | 種類 |
|---|---|---|---|---|
| 1 | [obra/superpowers](https://github.com/obra/superpowers) | 300,650 | 計画・サブエージェント・テスト駆動・レビューを束ねた開発手法のスキル群 | 開発ワークフロー |
| 2 | [mattpocock/skills](https://github.com/mattpocock/skills) | 294,045 | TypeScript 開発者が自分の `.agents` から公開した実務スキル集 | 開発（個人集） |
| 3 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 220,361 | Karpathy 氏の LLM コーディングの落とし穴の観察を、1枚の `CLAUDE.md` にしたもの | 行動規則（コミュニティ製） |
| 4 | [anthropics/skills](https://github.com/anthropics/skills) | 181,599 | Anthropic 公式のスキル集（docx / pdf / pptx / xlsx ほか） | 公式 |
| 5 | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 165,207 | 「一番怠け者のシニア開発者のように考えさせる」（YAGNI）スキル | 開発の思想 |

選び方の注意:
- 検索で上位に出ても、**スキル集ではないものは除いた**。例: `morluto/rea`（290,363。逆アセンブル用のツール。フォーク数が星に対して極端に多く、実態は未確認）、`affaan-m/ECC`（281,443。エージェント実行基盤）、`openclaw/openclaw`、`NousResearch/hermes-agent`（いずれもエージェント本体）。この除外は筆者の判断で、機械的な基準ではない。
- GitHub のトピックは自己申告なので、**取りこぼしがありうる**。上の表は、トピック検索と著名リポジトリの個別確認を組み合わせたもので、網羅ではない。
- 3位は `SKILL.md` 形式のスキルではなく単一の `CLAUDE.md`。名前に skills と付くため上位に入るが、種類は規則集。同じ名前で `forrestchang/` 配下を紹介する資料もあり、現在は `multica-ai/` で確認できた。移管の経緯は未確認。
- 第三者のランキングサイト（[Shareuhack](https://www.shareuhack.com/en/tools/claude-skills-ranking)、2026-10-09 更新）でも、同じ顔ぶれが上位に並ぶ。

### 5.2 ジャンル別の著名スキル

| ジャンル | 代表例（星は 2026-10-16） | ひとこと |
|---|---|---|
| **文書作成** | anthropics/skills の `docx` `pdf` `pptx` `xlsx`（181,599） | Anthropic 提供。claude.ai のファイル作成の中身。ソース公開だが Apache 2.0 ではない（参照用） |
| **開発ワークフロー** | [obra/superpowers](https://github.com/obra/superpowers)（300,650）、[mattpocock/skills](https://github.com/mattpocock/skills)（294,045）、[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)（107,381） | 計画→実装→レビューの型を渡す。Superpowers は権限が広いので、監督のもとで使うよう勧める評価もある（Shareuhack） |
| **フロントエンド / デザイン** | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)（98,008）、[nexu-io/open-design](https://github.com/nexu-io/open-design)（101,615）、anthropics/skills の `frontend-design` | 「AI が作りがちな凡庸な画面」を避ける方向 |
| **ベンダー公式の知識** | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)（32,533。React / Next.js の性能、Web デザイン指針）、[vercel-labs/skills](https://github.com/vercel-labs/skills)（35,246。`npx skills` でスキルを入れる道具） | 製品側が「正しい使い方」をスキルで配る例 |
| **図・可視化** | [tt-a1i/archify](https://github.com/tt-a1i/archify)（84,472）、[cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)（56,414） | アイデアやコードを図にする |
| **文章** | [blader/humanizer](https://github.com/blader/humanizer)（57,570） | AI っぽい文章の癖を消す |
| **マーケティング** | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)（55,106） | SEO・コピー・CRO など |
| **科学・研究** | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)（51,454。177 スキル） | 生物・化学・医療。100 以上の科学データベースを扱う、と説明にある |
| **キャリア** | [career-ops-hq/career-ops](https://github.com/career-ops-hq/career-ops)（75,243） | 求人の採点、履歴書の調整（提出は人が押す） |
| **トークン節約** | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)（113,059） | 出力を簡潔にして約65%減らすと説明。効果の数字は作者の主張で未検証 |
| **計画・記憶** | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files)（27,481）、[thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)（101,238。プラグイン） | 長い作業を、ファイルに計画を残して継続する |
| **スキルの目録（まとめ集）** | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)（77,251）、[VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)（35,847）、[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)（55,844） | 探すときの入口。載っているものの安全性までは保証しない |

出典の確認度:
- 星・フォーク数・説明文は GitHub API の値（一次）。
- 「何をするか」は各リポジトリの説明文と、第三者の紹介（[Firecrawl の紹介記事](https://www.firecrawl.dev/blog/best-claude-code-skills)、2026-09 更新）によるもので、筆者は各スキルの中身を読んで検証していない。
- Trail of Bits の `security`（CodeQL / Semgrep による監査）など、星の数を確認していないものは表に入れていない。

### 5.3 このリポジトリでの参考【筆者の提案】

- 上位は「開発向け」が多い。文書や調査の用途なら、まず公式の `docx` / `pdf` / `pptx` / `xlsx` が出発点になる。
- 星の数が多いことと、安全であることは別（第7章）。入れる前に `scripts/` と外部取得の有無を読む。

## 6. 今後の展望

公式が語っている方向と、そこから読み取れる筆者の見立てを分けて書く。

**公式・登壇者が述べていること**
- **ライフサイクル全体の機能追加。** 作成・編集・発見・共有・利用の各段階に機能を足す。あわせて、エージェント自身がスキルを作り、編集し、評価できるようにして、自分の行動パターンを再利用できる能力として残させる（[Engineering ブログ](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)）。
- **MCP との補完。** スキルが複数の外部ツールにまたがる複雑なワークフローを教える形を探る（同上）。
- **スキルのソフトウェア化。** Anthropic の登壇者（Barry Zhang、Mahesh Murag）は、スキルが単なる Markdown から、ソフトウェアや実行ファイルを含むパッケージへ育つこと、テスト・バージョン管理・品質測定の方法を作ること、使い始めの1日目から30日目で Claude が目に見えて良くなることを目標に挙げた。登壇の日付は未確認で、確認できたのは第三者の要約ページ（[videohighlight.com](https://videohighlight.com/v/CEvIs9y1uog)）のみ。原典の動画では確認していない。
- **標準の共同運営。** 仕様は Anthropic 発だが、エコシステムからの貢献を受け付ける形で公開されている（[agentskills.io](https://agentskills.io)）。

**筆者の見立て【推測】**
- 配布の場（マーケットプレイス、組織ディレクトリ）が増えるので、審査・署名・スキャンなど「信頼の仕組み」が競争点になる。
- 標準が共通になるほど、同じスキルフォルダを複数のエージェントで使い回す運用（このリポジトリの `AGENTS.md` や手順書の置き方にも近い）が現実的になる。
- 「スキルを書く」より「スキルをテストして育てる」側に、作業の重心が移る可能性が高い。

## 7. リスクと懸念点

### 7.1 セキュリティ（最大の論点）

スキルは「Claude が読んで従う文章」と「実行されるコード」の両方を運べる。そのため、入れた時点で、悪意のある指示や処理が Claude の権限で動く。公式も「信頼できる出所のものだけ使う。ソフトのインストールと同じ注意で、同梱ファイルを監査する」と警告している（[Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)）。

実態の調査として、Snyk が 2026-02-05 に公開した報告がある（第三者の調査。ClawHub と skills.sh のスキル 3,984 件が対象で、Anthropic 公式ではない）。

| 指標 | 結果 |
|---|---|
| 重大（CRITICAL）な問題を1つ以上含む | 534 件（13.4%） |
| 重大度を問わず問題を1つ以上含む | 1,467 件（36.82%） |
| 人の確認で悪意ありと確定 | 76 件（公開時点で 8 件が公開されたまま） |
| 外部コンテンツを取得する（間接プロンプトインジェクションの入口） | ClawHub のスキルの 17.7% |
| 悪意が確定したもののうち、プロンプトインジェクションを併用 | 91%（悪意あるコードは 100%） |

出典: [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub)、[技術報告（arXiv）](https://arxiv.org/pdf/2605.28588)。この調査は特定の公開サイトの集計で、Anthropic 公式のスキルや、人が自分で書いたスキルの安全性を示すものではない。

主な手口は、①未検証のバイナリをダウンロードして実行させる、②Base64 などで隠した命令で認証情報を外部へ送る、③セキュリティ設定の無効化や破壊的操作、の3つ。報告書の対策は、入れる前にコードと同梱スクリプトを読むこと、人気を安全の目安にしないこと、公開側は CRITICAL の指摘があるものを審査待ちで止めること。

公式側の対策としては、Enterprise 管理者が claude.ai と Cowork のカスタムスキルの内容スキャンを有効にできる。ただし Skills API と Console は対象外（Platform Docs）。

### 7.2 運用上の懸念

- **動作が確定的でない。** スキルは Claude が解釈して従うので、結果がぶれる。必ず守らせたいことはフックで強制する、というのが公式の整理（[Extend Claude Code](https://code.claude.com/docs/en/features-overview)）。「CLAUDE.md やスキルに書いた『編集禁止』は依頼であって保証ではない」とも明記されている。
- **description の質に依存する。** 説明が曖昧、または他と重なると、違うスキルが選ばれたり、必要なものが読まれなかったりする（同上）。スキルが増えるほど選択の精度が課題になる。
- **文脈の消費。** 本文は発動時に会話へ入る。説明文も常時載るため、数が増えると無視できない（副作用のあるものは `disable-model-invocation: true` で説明文ごと外せる）。
- **製品間で同期しない。** claude.ai・API・Claude Code にそれぞれ入れる必要があり、版のずれが起きうる（Platform Docs）。
- **実行環境の制約が違う。** API はネットワークなし・パッケージ追加不可、Claude Code は完全なネットワークあり、claude.ai は設定次第。同じスキルでも動作が変わる（同上）。
- **更新に伴う危険。** 信頼したスキルでも、依存先や外部取得先が変われば危険になりうる（同上）。外部 URL を取りに行くスキルは特に注意。

### 7.3 標準化に伴う懸念【推測】

- 同じ形式を各社が読むので、悪意あるスキルの影響範囲も製品をまたぐ。
- 標準の仕様と、各社の拡張（Claude Code の `context: fork` など）が混ざり、「標準だと思って書いたら他では動かない」ことが起きうる。

### 7.4 このリポジトリで使うときの目安【筆者の提案】

- 自分で書いたもの、または出所が明確なものだけ入れる。
- `scripts/` の中身と、外部 URL を取得する箇所を、入れる前に読む。
- このリポジトリは公開（PUBLIC）なので、スキルに機密や会社固有の情報を入れない。

## 8. 使い方（作り方・置き場・呼ばれ方）

**作り方**: フォルダに `SKILL.md` を置き、先頭の YAML に `name` と `description` を書く。`description` が「いつ使うか」の判断材料なので、ここが一番大事。付属物は `scripts/` `references/` `assets/` などに置く（[agentskills.io](https://agentskills.io)）。claude.ai では会話で頼んで作らせるか、skill-creator を使える。

```markdown
---
name: deploy
description: 本番へデプロイする。ユーザーがデプロイを頼んだとき使う
disable-model-invocation: true
---
1. テストを走らせる
2. ビルドする
3. デプロイ先へ push する
```

**置き場（Claude Code）**: `~/.claude/skills/<名前>/SKILL.md`（個人）、`.claude/skills/<名前>/SKILL.md`（プロジェクト、コミットで共有）、`<plugin>/skills/`（プラグイン、`/プラグイン名:スキル名`）、管理者設定（組織）。名前が重なると組織 > 個人 > プロジェクトの順で勝つ（[Claude Code Docs: Skills](https://code.claude.com/docs/en/skills)）。

**呼ばれ方**: ①Claude が依頼と `description` を照らして自動で読む、②人が `/スキル名 引数` で呼ぶ。主な制御:

- `disable-model-invocation: true` … 人だけが呼べる（副作用のある操作向け。説明文も文脈に載らない）
- `user-invocable: false` … `/` メニューに出さず、Claude だけが使う
- `context: fork` … サブエージェントで隔離して実行
- `allowed-tools` … そのターンだけツールを事前許可

## 9. 類似ワードと関連ワード

### 同じものの別名

| 言葉 | 意味 |
|---|---|
| Agent Skills | 公式の正式名。オープン標準の名前でもある |
| Claude Skills / Skills | 報道や Claude の画面での呼び方。同じもの |
| `SKILL.md` | スキル本体のファイル名。転じてスキルそのものを指すことも |
| agentskills.io | オープン標準の仕様サイト |
| 既製スキル（pre-built） | Anthropic 提供の docx / xlsx / pptx / pdf |
| skill-creator | スキルを作るためのスキル |

### 似ているが別のもの（違いが分かる形で）

| 言葉 | 何か | いつ読まれる・動く | スキルとの違い |
|---|---|---|---|
| **CLAUDE.md**（AGENTS.md も同類） | Claude Code のプロジェクト記憶ファイル | 毎セッション全文 | 常時載る「いつも守る規則」。スキルは必要時だけ。公式は 200 行以内を推奨し、手順はスキルへ移せと言う |
| `.claude/rules/` | パス別の規則 | 毎回、または該当ファイルを開いたとき | 場所で絞る規則。スキルはタスクで絞る |
| **プロジェクト指示**（claude.ai Projects） | プロジェクト内の全会話に効く指示 | そのプロジェクトの会話で常時 | CLAUDE.md の claude.ai 版に近い。常時載る点がスキルと違う【一般知識による整理】 |
| **カスタム指示**（プロフィールの設定 / スタイル） | 個人の好み・口調 | 全会話で常時 | 「どう答えるか」。スキルは「何をどうやるか」【一般知識による整理】 |
| 出力スタイル（Claude Code） | 役割・口調・形式 | セッション中ずっと | 応答の形を決める。手順や知識は持たない |
| **スラッシュコマンド** | `/名前` で呼ぶ定型プロンプト | 人が打ったとき | Claude Code では**スキルに統合済み**。スキル＝自動でも呼ばれる上位互換 |
| **MCP**（Model Context Protocol） | 外部サービスにつなぐプロトコル | ツール名は起動時、定義は使用時 | 「つなぐ（道具）」。スキルは「使い方を教える（知識）」。併用が基本（例: MCP で DB 接続、スキルでスキーマと書き方） |
| コネクタ | claude.ai での MCP 接続の呼び名 | 同上 | 同上 |
| **サブエージェント** | 別の文脈で動く作業者 | 呼ばれたとき、隔離された窓で | スキルは今の文脈に足す内容、サブエージェントは別窓の作業者。`context: fork` や `skills:` で組み合わせ可 |
| **フック** | イベント時に必ず動くスクリプト等 | ライフサイクルのイベント時 | 決定的・強制。スキルは Claude が解釈するので結果がぶれる。「絶対守らせたい」ならフック |
| **プラグイン** | スキル・フック・サブエージェント・MCP を束ねた配布単位 | 有効化した場所で | スキルの「入れ物と配り方」。マーケットプレイスで配る |
| ツール（tool use） | 関数呼び出し | Claude が呼んだとき | 1つの操作。スキルは操作を含む手順のまとまり |
| Agent SDK | Claude Code の基盤でエージェントを作る SDK | — | スキルを読み込める実行環境の一つ |
| Code Execution Tool | API でコードを動かすサンドボックス | — | API・claude.ai でスキルを使う前提条件 |

## 確認できなかった点・注意

- claude.ai のファイル作成機能が始まった正確な日付は未確認。
- Claude Code でスラッシュコマンドがスキルに統合された日付は未確認（Docs で統合済みであることだけ確認）。
- claude.ai の共有範囲は、Platform Docs（個人単位）と 2025-12-18 の発表（組織管理の追加）で食い違う。最新の画面で確かめる必要がある。
- 第5章の星の数は 2026-10-16 時点の値で、日々変わる。トップ5の選び方は筆者の判断。各スキルの中身は読んでいない。
- 登壇（Barry Zhang、Mahesh Murag）の内容は第三者の要約ページでのみ確認。日付も未確認。
- Snyk の数値は 2026-02-05 時点の特定サイトの集計で、現在の状況は未確認。
- プロジェクト指示・カスタム指示の行は、今回の調査で公式ページを開いておらず、一般知識による整理。

## 出典

- Anthropic, Introducing Agent Skills（2025-10-16、2025-12-18 追記）: https://claude.com/blog/skills
- Anthropic Engineering, Equipping agents for the real world with Agent Skills（2025-10-16）: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Claude Platform Docs, Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Claude Code Docs, Skills: https://code.claude.com/docs/en/skills
- Claude Code Docs, Extend Claude Code: https://code.claude.com/docs/en/features-overview
- Agent Skills（オープン標準）: https://agentskills.io
- gihyo.jp, Agent Skills のオープン標準化（2025-12）: https://gihyo.jp/article/2025/12/agent-skills-to-open-standard
- Simon Willison, Claude Skills are awesome, maybe a bigger deal than MCP（2025-10-16）: https://simonw.substack.com/p/claude-skills-are-awesome-maybe-a
- Simon Willison, OpenAI are quietly adopting skills（2025-12）: https://simonw.substack.com/p/openai-are-quietly-adopting-skills
- Snyk, ToxicSkills（2026-02-05）: https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub
- Snyk, Technical Report: Exploring the Emerging Threats of the Agent Skill Ecosystem（2026-02-05）: https://arxiv.org/pdf/2605.28588
- GitHub 検索 API（2026-10-16 取得）: 第5章の星・フォーク数
- Shareuhack, Claude Code Skills Ranking（2026-10-09 更新・第三者）: https://www.shareuhack.com/en/tools/claude-skills-ranking
- Firecrawl, Best Claude Code Skills（2026-09 更新・第三者）: https://www.firecrawl.dev/blog/best-claude-code-skills
- 登壇「Don't Build Agents, Build Skills Instead」の第三者要約: https://videohighlight.com/v/CEvIs9y1uog
