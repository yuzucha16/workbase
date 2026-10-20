---
type: index
title: guides の索引
tags:
  - knowledge-management
aliases:
  - guides
  - 手順書の索引
created: 2026-10-10
updated: 2026-10-20
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
| 会社から「ゲートウェイのベース URL と発行者 URL」を渡された。Claude Code / Zed でどうつなぐのか、OIDC のサインインとトークンの流れを、自分で説明できるようにする | [[llm-gateway-oidc]] | 理解ガイド |
| ゲートウェイにつながらない・`apiKeyHelper` が失敗する・約1時間で `401` になる、などの症状から原因を切り分ける | [[llm-gateway-oidc#3. チェックリスト（症状 → 原因 → 対処）]] | 理解ガイド |
| Claude Code を会社のゲートウェイにつなぐ（URL・クライアント ID を入れて、サインインして起動する） | dotfiles の `windows/claude/README.md` 第4章（このリポジトリの外。スクリプトの隣に置く手順書） | 手順書 |

### AI に顧客データ・社外秘を見せない

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| なぜ「AI 作業部屋」を入れたのか、選択肢から選ぶまでの経緯と、試して確かめたことを、自分で説明できるようにする | [[ai-room-why]] | 理解ガイド |
| AI に見せたくないファイルを、設定で隠す方式（禁止リスト）でなく、渡したものだけ見せる方式（許可リスト）にする理由を思い出す | [[ai-room-why#2. 理解のための基礎知識]] | 理解ガイド |
| 部屋で AI を使っていて、`Permission denied`、成果物がコミットに入らない、マウントが残る、などで困った | [[ai-room-why#3. チェックリスト（症状・疑問 → 原因 → 対処）]]、[[ai-room-setup#10. うまくいかないとき]] | 理解ガイド・手順書 |
| WSL に AI 作業部屋を作り、Project の `ai/` だけを渡して Claude Code で作業する | [[ai-room-setup]] | 手順書 |
| 実際の名前（`pilot2` `pilot2-1`）で、`room.py` を1手ずつ通して、部屋の作成から `close` まで行う | [[ai-room-setup-script]] | 手順書 |
| 実際の名前（`pilot` `pilot-1`）で、`room.py` を使わずに、マウント・アンマウントを含めて手作業で通す | [[ai-room-setup-manual]] | 手順書 |
| 顧客情報を含む資料（議事録、事業戦略など）を、マスクだけして AI に要約させる（実名には戻さない） | [[ai-room-mask-summary]] | 手順書 |
| 部屋で作業した Project を閉じて、`archives/` に移す | [[ai-room-setup#7. Project を閉じる]] | 手順書 |

### 仕組みを見直す

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| `review`（見直して）は何のためか、何を見て何を決めるか、ここまでの経緯とこれからを、自分で説明できるようにする | [[review-hook-why]] | 理解ガイド |

### エラー・困りごとを切り分ける

| やりたいこと・場面 | 見る文書 | 種類 |
|---|---|---|
| `SSL certificate problem` などの証明書エラーが出た（会社のプロキシ環境） | [[ssl-inspection#3. チェックリスト（症状 → 原因 → 対処）]] | 理解ガイド |
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
| 手順書（`howto/`） | どの順で何をやるんだっけ | [[ai-room-setup]]、[[ai-room-setup-script]]、[[ai-room-setup-manual]]、[[ai-room-mask-summary]]、[[bedrock-first-hello]]（PC のセットアップの手順書は dotfiles の `docs/setup/`） |
| 理解ガイド（`explain/`） | なぜそうなる？ どう動いている？ | [[ssl-inspection]]、[[ai-room-why]]、[[review-hook-why]]、[[llm-gateway-oidc]] |
| クイックリファレンス（`quickref/`） | あのコマンドは何だっけ | [[apt]]、[[git]]、[[docker]]、[[shell]]、[[ssh]]、[[markdown]] |

## この索引の更新

- `guides/` に文書を足したら、「場面から引く」に1行以上と、「種類から引く」の文書の欄に足す。消したら、両方から消す。
- 行は、やりたいこと・場面（読む人の言葉）で書く。ファイル名やコマンド名だけの行にしない。
- 場面に合う節が無ければ、節を足す。
