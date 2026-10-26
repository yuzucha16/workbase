---
type: index
title: guides の索引
tags:
  - knowledge-management
aliases:
  - guides
  - 手順書の索引
created: 2026-10-10
updated: 2026-10-21
---

# guides の索引

やりたいこと・場面から、見る文書を引く。`guides/` の入口。
文書の種類（手順書・理解ガイド・クイックリファレンス）の分け方と作り方は [[reference-doc-types]]。

## 場面から引く

### PC をセットアップする

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| Windows 11 / Debian 系 Linux（MX / Ubuntu / Mint）を入れて、dotfiles のスクリプトまで通す。マルチブート、Linux の EFI・パーティション、SSH 鍵と GitHub、WSL2、フォント（PlemolJP）もここ | dotfiles の `docs/setup/`（`win11.md`、`debian-family.md`、`fonts-setup.md`。このリポジトリの外。`$HOME\works\repos\github.com\yuzucha16\dotfiles\docs\setup\`） | 手順書 |
| Claude Code の設定を PC に入れる・入れ替える | dotfiles の `windows/claude/README.md`（このリポジトリの外。スクリプトの隣に置く手順書） | 手順書 |

### AI を使う環境をつなぐ

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| 個人の AWS アカウントを作って、Bedrock 経由で Claude Code に「こんにちは」と話しかける | [[bedrock-first-hello]] | 手順書 |
| Bedrock と Anthropic 直接の単価の差、リージョン指定の割増を思い出す | [[bedrock-first-hello#対応バージョン表]] | 手順書 |
| 勤務先から「ゲートウェイのベース URL と発行者 URL」を渡された。Claude Code / Zed でどうつなぐのか、OIDC のサインインとトークンの流れを、自分で説明できるようにする | [[llm-gateway-oidc]] | 理解ガイド |
| ゲートウェイにつながらない・`apiKeyHelper` が失敗する・約1時間で `401` になる、などの症状から原因を切り分ける | [[llm-gateway-oidc#3. チェックリスト（症状 → 原因 → 対処）]] | 理解ガイド |
| Claude Code を勤務先のゲートウェイにつなぐ（URL・クライアント ID を入れて、サインインして起動する） | dotfiles の `windows/claude/README.md` 第4章（このリポジトリの外。スクリプトの隣に置く手順書） | 手順書 |

### AI に顧客データ・社外秘を見せない

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| なぜ「AI 作業部屋」を入れたのか、選択肢から選ぶまでの経緯と、試して確かめたことを、自分で説明できるようにする | [[ai-room-why]] | 理解ガイド |
| Area の知識（実名入り）を、別の Project の部屋の AI に使わせる設計と、workbase の共有知との違いを、自分で説明できるようにする | [[cross-area-shared-knowledge]] | 理解ガイド |
| AI に見せたくないファイルを、設定で隠す方式（禁止リスト）でなく、渡したものだけ見せる方式（許可リスト）にする理由を思い出す | [[ai-room-why#2. 理解のための基礎知識]] | 理解ガイド |
| 実名入りの原本・成果物・知識が Area と Project のどこに置かれ、どの順に流れるか（`_noai/source` `deliverable` `knowledge`、`pull` → `mask` → `restore`）を、自分で説明できるようにする | [[ai-room-data-layout]] | 理解ガイド |
| 同じ Area の Project を、同じ部屋で並行して `room start` したとき、何が共有され、どこで衝突するかを思い出す。後から start が止まる、`index.lock` で失敗する | [[ai-room-concurrent-start]] | 理解ガイド |
| 部屋で AI を使っていて、`Permission denied`、成果物がコミットに入らない、マウントが残る、などで困った | [[ai-room-why#3. チェックリスト（症状・疑問 → 原因 → 対処）]]、[[ai-room-setup#10. うまくいかないとき]] | 理解ガイド・手順書 |
| WSL に AI 作業部屋を作り、Project の `ai/` だけを渡して Claude Code で作業する | [[ai-room-setup]] | 手順書 |
| 実際の名前（`pilot2` `pilot2-1`）で、`room.py` を1手ずつ通して、部屋の作成から `close` まで行う | [[ai-room-setup-script]] | 手順書 |
| 実際の名前（`pilot` `pilot-1`）で、`room.py` を使わずに、マウント・アンマウントを含めて手作業で通す | [[ai-room-setup-manual]] | 手順書 |
| 顧客情報を含む資料（議事録、事業戦略など）を、マスクだけして AI に要約させる（実名には戻さない） | [[ai-room-mask-summary]] | 手順書 |
| シートや個人名を消した xlsx・pptx を AI に見せたら、消したはずのものが見えていた。なぜ残るかと、渡す前の点検・掃除（`cleankit.py`）を思い出す | [[ooxml-residue]] | 理解ガイド |
| 部屋で作業した Project を閉じて、`archives/` に移す | [[ai-room-setup#7. Project を閉じる]] | 手順書 |
| 部屋の中で、Markdown の HTML 化、mermaid の画像出力、xlsx の変換と再計算をしたい。入っている道具と、使い方（`room-mmdc` など）を思い出す | [[ai-room-convert-tools#3. v1 で入れたもの]] | 理解ガイド |
| Windows が要る実行（pwsh、Excel 固有の機能）を、AI がスクリプトを作り人が 1 件ずつ実行する形にする案（`room run`）と、その境界への影響を思い出す | [[ai-room-convert-tools#7. room run の案（未実装）]] | 理解ガイド |
| 部屋の Chromium が起動しない、PDF の漢字の字形が中国式になる、日本語が化ける、などで困った | [[ai-room-convert-tools#5. 実機で分かったこと（PC2、2026-10-20）]] | 理解ガイド |

### 仕組みを見直す

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| ルールや知識がノートにあるのに、作業中に読まれない。作業の前に知識を引く仕組み（`triggers:` と `find_knowledge.py`）を、自分で説明できるようにする | [[triggers-knowledge-index]] | 理解ガイド |
| `review`（見直して）は何のためか、何を見て何を決めるか、ここまでの経緯とこれからを、自分で説明できるようにする | [[review-hook-why]] | 理解ガイド |

### AI の使用量を振り返る

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| 会話を続けるか切るかの目安（約10万トークン）が、なぜ費用に効くかを、自分で説明できるようにする。間があいた後の最初の応答が高い、などの症状から原因を切り分ける | [[claude-code-cost-session-size]] | 理解ガイド |
| Claude Code のトークン使用量・概算費用($)を、週次・月次で集計して、上位セッションや 1 件当たりの平均/最大/最小を見る | [[claude-usage-report]] | 手順書 |
| 使用量の集計を HTML のレポートにする。単価表を足す・更新する。ccusage と突き合わせる | [[claude-usage-report]] | 手順書 |

### エラー・困りごとを切り分ける

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| `SSL certificate problem` などの証明書エラーが出た（勤務先のプロキシ環境） | [[ssl-inspection#3. チェックリスト（症状 → 原因 → 対処）]] | 理解ガイド |
| ブラウザは通るのに git / WSL / docker / pip / npm だけ通らない | [[ssl-inspection]] | 理解ガイド |
| SSL インスペクションの仕組みを、自分で説明できるようにする | [[ssl-inspection#2. 理解のための基礎知識]] | 理解ガイド |

### コマンド・書き方を思い出す

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| パッケージを調べる・入れる・更新する・消す（Debian 系） | [[apt]] | クイックリファレンス |
| git の clone・commit・push・ブランチ・submodule・取り消し | [[git]] | クイックリファレンス |
| docker のイメージ・コンテナ、docker-compose の起動・ログ・停止 | [[docker]] | クイックリファレンス |
| シェルのプロセス・権限・ディレクトリ・シンボリックリンク・リダイレクト | [[shell]] | クイックリファレンス |
| SSH サーバーを入れる・設定する、クライアントの `~/.ssh/config` | [[ssh]] | クイックリファレンス |
| Markdown の記法（見出し・表・コードブロック・チェックボックス） | [[markdown]] | クイックリファレンス |

## 種類から引く

| 種類 | 読む人の問い | 文書 |
|---|---|---|
| 手順書（`howto/`） | どの順で何をやるんだっけ | [[ai-room-setup]]、[[ai-room-setup-script]]、[[ai-room-setup-manual]]、[[ai-room-mask-summary]]、[[bedrock-first-hello]]、[[claude-usage-report]]（PC のセットアップの手順書は dotfiles の `docs/setup/`） |
| 理解ガイド（`explain/`） | なぜそうなる？ どう動いている？ | [[ssl-inspection]]、[[ai-room-why]]、[[ai-room-convert-tools]]、[[ai-room-data-layout]]、[[ai-room-concurrent-start]]、[[review-hook-why]]、[[llm-gateway-oidc]]、[[cross-area-shared-knowledge]]、[[triggers-knowledge-index]]、[[claude-code-cost-session-size]]、[[ooxml-residue]] |
| クイックリファレンス（`quickref/`） | あのコマンドは何だっけ | [[apt]]、[[git]]、[[docker]]、[[shell]]、[[ssh]]、[[markdown]] |

## この索引の更新

- `guides/` に文書を足したら、「場面から引く」に1行以上と、「種類から引く」の文書の欄に足す。消したら、両方から消す。
- 行は、やりたいこと・場面（読む人の言葉）で書く。ファイル名やコマンド名だけの行にしない。
- 場面に合う節が無ければ、節を足す。
