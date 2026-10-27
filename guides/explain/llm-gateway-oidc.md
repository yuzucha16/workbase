---
type: explain
title: 組織の LLM ゲートウェイと OIDC サインイン:理解ガイド
tags:
  - ai/claude
  - tool/zed
  - tool/powershell
  - windows
  - security
checked: 2026-10-20
triggers: [LLMゲートウェイ, OIDC, サインイン, 認証, トークン, プロキシ, Zed, 組織]
---

# 組織の LLM ゲートウェイと OIDC サインイン:理解ガイド

管理側から「ゲートウェイのベース URL」と「発行者 URL」を渡されたとき、Claude Code（CLI）と Zed の ACP エージェントがどう認証してつながるのかを、自分で説明できるようにするためのガイド。つながらないときに、症状から原因を切り分けられることも目的にする。

- 前提: Windows 11。組織が LLM ゲートウェイを運用し、IdP は Microsoft Entra ID（発行者 URL が `login.microsoftonline.com/…/v2.0` の形）。Claude Desktop の「Configure Third-Party Inference」で、すでに同じゲートウェイにつないでいる
- 確認状況: CLI（`claude-gateway`）と Zed の両方で、接続できることを実機で確認した（2026-10-20）。**サインインの約1時間後に、トークンが自動で更新されるかは未確認**（6 に書く）
- 組織名・URL・クライアント ID・テナント ID などの固有情報は、このガイドに書かない。実装の手順は dotfiles の `windows/claude/README.md` の第4章が正

## 1. 当時の状況と解決（ダイジェスト）

**状況**

- 管理側から「ゲートウェイのベース URL」と「発行者 URL」が案内されていた。Claude Desktop はそれで使えていたが、Claude Code と Zed は未対応だった
- すでにあったのは、個人の AWS アカウントの Bedrock（IAM ユーザーのアクセスキー）への接続だけだった

**試行と原因**

1. **AWS SSO（IAM Identity Center）を試した**: 「SSO」の語から推測した。`aws configure sso` が求める「SSO start URL」は `…awsapps.com/start` の形で、案内された URL とは別物だった。**この組織の接続は AWS に直接つなぐ方式ではなかった**
2. **`/login` の Cloud gateway を試した**: 「ゲートウェイ」の語から、Anthropic の Claude apps gateway と推測した。`gateway hosts must be on your organization's private network` で拒否された。ゲートウェイの名前解決の結果が**公開アドレス**で、Claude apps gateway は**社内のプライベートアドレスにあることが前提**だったため
3. **汎用の LLM ゲートウェイ + OIDC だと分かった**: Claude Desktop の設定画面に、発行者 URL・クライアント ID・スコープ・リダイレクトポートの項目があった。Desktop が OIDC でサインインして、ID トークンをゲートウェイに送る方式だった

**解決**

- Claude Code に OIDC のサインイン機能は無いので、**`apiKeyHelper`（トークンを返すコマンド）が、OIDC のトークンを取って返す**構成にした
- ベース URL は環境変数 `ANTHROPIC_BASE_URL` に書く（Desktop の「Gateway base URL」と同じ値）

## 2. 理解のための基礎知識

### 登場人物

```
 あなたの PC                         組織の IdP (Entra ID)
 ┌──────────────────┐   ① ブラウザでサインイン    ┌──────────────┐
 │ Claude Code / Zed │ ───────────────────────▶ │ 発行者 (issuer) │
 │  apiKeyHelper     │ ◀─────────────────────── │              │
 └────────┬─────────┘   ② ID トークンを受け取る   └──────────────┘
          │ ③ Authorization: Bearer <ID トークン>
          ▼
 ┌──────────────────┐   ④ トークンを検証し、       ┌──────────────┐
 │ LLM ゲートウェイ   │      組織の資格情報で呼ぶ ▶ │ Bedrock など   │
 └──────────────────┘                          └──────────────┘
```

- 開発者は、**AWS のキーを持たない**。持つのは IdP の自分のアカウントだけ
- 上流（Bedrock など）の資格情報は、**ゲートウェイが持つ**。誰がどれだけ使ったかの記録や上限も、ゲートウェイで管理できる

### 用語

| 用語 | 意味 |
|---|---|
| ゲートウェイ（ベース URL） | Claude Code と Bedrock などの間に置く、組織のプロキシ。Anthropic の Messages API の形で受ける。`ANTHROPIC_BASE_URL` と同じ値 |
| IdP | 利用者を認証する組織の基盤（Microsoft Entra ID など） |
| 発行者 URL（issuer） | IdP の「基本の URL」。`/.well-known/openid-configuration` を足すと、認可・トークンの各 URL が書かれた文書が読める（クライアントが自分で足す。設定には足さない） |
| クライアント ID | IdP に登録された「アプリ」の ID。Entra では「アプリの登録」で発行される。サインインを求めるアプリの名札で、秘密ではないが、組織を特定できる |
| OIDC | OAuth 2.0 の上に「誰か」を表す仕組みを足した規格。サインインの結果として **ID トークン**が得られる |
| 公開クライアント + PKCE | 秘密を安全に持てないアプリ（PC のアプリ）向けの方式。使い捨ての証明（`code_verifier` とそのハッシュ `code_challenge`）で、認可コードの横取りを防ぐ |
| loopback リダイレクト | ブラウザのサインイン後の戻り先を `http://127.0.0.1:<ポート>/callback` にする。アプリがその場で1回だけ待ち受けて、認可コードを受け取る |
| ID トークン | 「この人が、このアプリ宛てにサインインした」という署名つきの JWT。約1時間で切れる。ゲートウェイは署名・発行者・宛先（`aud` = クライアント ID）を検証する |
| リフレッシュトークン | 新しいトークンをもらうための長持ちする権利。`offline_access` スコープで得る。これで再サインインなしの更新ができる |
| `apiKeyHelper` | Claude Code が呼ぶコマンド。標準出力の値を認証情報として、`Authorization: Bearer` と `x-api-key` の両方で送る。既定で5分キャッシュ |

### ゲートウェイ接続の3つの型

「ゲートウェイ」「SSO」の語は同じでも、つなぎ方は別。どれかを見分けてから設計する。

| 型 | 認証 | 宛先 | Claude Code での入口 | 見分け方 |
|---|---|---|---|---|
| AWS に直接（IAM Identity Center） | `aws sso login` | AWS（Bedrock） | `claude --settings`（Bedrock 設定）と `awsAuthRefresh` | 案内に `…awsapps.com/start`（SSO start URL）がある |
| Claude apps gateway | `/login` の Cloud gateway（ブラウザ SSO） | **社内のプライベートアドレス** | `forceLoginMethod` と `forceLoginGatewayUrl` | 案内が「`/login` で Cloud gateway を選ぶ」。名前解決の結果が社内アドレス |
| 汎用の LLM ゲートウェイ + OIDC | OIDC のトークンを Bearer で送る | 公開でも社内でもよい | `ANTHROPIC_BASE_URL` と `apiKeyHelper` | 案内に「ベース URL」と「発行者 URL」「クライアント ID」。Desktop の設定画面に Gateway SSO IdP (OIDC) の項目がある |

### サインインとトークン更新の流れ（`apiKeyHelper` の中身）

1. 初回だけ `-Login`: 認可コード + PKCE のブラウザサインイン。ID トークンとリフレッシュトークンを得て、**暗号化して保管**（Windows の DPAPI。この PC・このユーザーだけが復号できる）
2. 以降、Claude Code が `apiKeyHelper` を呼ぶたびに: 保管したトークンの期限を見て、**期限が近ければ**リフレッシュトークンで更新し、新しい ID トークンを**標準出力に返す**
3. 更新できないとき（リフレッシュトークンの失効など）は、`-Login` を促して失敗する

守ること: ヘルパーの標準出力は**トークンだけ**にする（メッセージは標準エラーへ）。`pause` や余計な出力を入れると、Claude Code がヘルパーの失敗とみなす。

### 設定の置き場所を分ける理由

`apiKeyHelper` を共通の `~/.claude/settings.json` に入れると、`claude` が常にその認証になり、サブスク（OAuth）に戻れない。そこで `CLAUDE_CONFIG_DIR` で別のディレクトリを指して起動し、ゲートウェイ用の設定とトークンを分ける。Zed の ACP エージェントも、同じディレクトリを `CLAUDE_CONFIG_DIR` に渡して起動する。

### 自分で説明するときの一言

> 組織のゲートウェイは、組織の IdP で本人確認した人のトークンを受け取って、組織の AWS の資格情報で代わりに呼ぶ。Claude Code は OIDC を話せないので、トークンを取って返す小さなコマンド（`apiKeyHelper`）を挟む。トークンは約1時間で切れるので、リフレッシュトークンで自動更新する。

## 3. チェックリスト（症状 → 原因 → 対処）

| 症状 | 原因 | 対処 |
|---|---|---|
| `gateway hosts must be on your organization's private network`（`/login`） | Claude apps gateway の `/login` は、社内のプライベートアドレスのゲートウェイだけを受け付ける。宛先が公開アドレス | ゲートウェイの名前解決の結果を確認する。公開アドレスなら、汎用ゲートウェイ（OIDC + `apiKeyHelper`）の型。社内アドレスなのに出るなら、VPN・プロキシ・IPv6・管理設定を確認する |
| `aws configure sso` で `SSO start URL` に入れる値が無い | AWS の IAM Identity Center ではない。案内された URL は別の仕組み | 案内の資料が「ベース URL と発行者 URL」なら、汎用ゲートウェイの型 |
| `Your apiKeyHelper script is failing` | ヘルパーがトークンを返せない（未サインイン、更新失敗）、または標準出力に余計な文字が混ざる | ヘルパーを直接実行し、標準出力がトークンだけか見る。`not signed in` / `expired` なら `-Login` |
| ヘルパーが終わらない・固まる | `.cmd` の末尾の `pause` が、標準入力を待ち続ける | ヘルパーの入口に `pause` を入れない。対話の `-Login` のときだけ入れる |
| 約1時間でまた `401` | 更新できていない（リフレッシュトークンが無い・失効） | スコープに `offline_access` があるか確認し、`-Login` をやり直す |
| `-Login` で `AADSTS50011` | リダイレクト URI が登録と合わない | 登録の URI は `http://127.0.0.1/callback`（パスまで）。IdP の管理者に確認する。ポートは Entra では問われない |
| `-Login` で `AADSTS65001` | アクセストークンの型（`access_token`）で、API の権限に同意が無い | 管理者に権限の付与を依頼する。ID トークンの型なら出ない |
| `401`（ゲートウェイから） | トークンの種類（ID / アクセス）、スコープ、宛先（`aud`）が、ゲートウェイの期待と違う | Desktop の設定と同じ値にそろえる |
| モデルが見つからない | ゲートウェイが提供するモデル ID と違う（`/v1/models` が無いゲートウェイは自動検出されない） | Desktop の「推論モデルの一覧」と同じ ID を、`opus` / `sonnet` / `haiku` に割り当てる |
| 接続できない（`ENOTFOUND`、タイムアウト） | VPN の外、プロキシの設定、名前解決 | `Resolve-DnsName` と `Test-NetConnection <ホスト> -Port 443` で、宛先アドレスと到達を確認する。社外へはプロキシ経由なら `HTTPS_PROXY` が要る場合がある |
| `claude` なのにゲートウェイ（または逆） | 環境変数・設定の混在 | 設定を分ける（`CLAUDE_CONFIG_DIR`）。`claude-oauth` で OAuth に戻れる。`/status` で認証元を見る |

切り分けの順序の目安:

1. 宛先の名前解決（社内アドレスか、公開アドレスか）
2. 案内の用語（SSO start URL、ベース URL、発行者 URL）で、3つの型のどれかを決める
3. 型に合う入口で、いちばん小さい接続（`/status` と1メッセージ）を試す

## 4. 補足

### 4.1 トークンの種類

| 種類 | 何を表すか | 送る先 | 備考 |
|---|---|---|---|
| ID トークン | 「この人が、このアプリにサインインした」 | Desktop の既定。ゲートウェイが `aud`（クライアント ID）を検証する | 約1時間。この構成で使った |
| アクセストークン | 「このアプリが、この API を呼んでよい」 | API を保護するゲートウェイ（リソースサーバーとして検証する型） | スコープに API の識別子が必要。Entra では API の権限への同意が要る |
| リフレッシュトークン | 新しいトークンをもらう権利 | IdP のトークンエンドポイントだけ（ゲートウェイには送らない） | `offline_access` で得る。保管は暗号化する |

### 4.2 URL とクライアント ID を公開しない理由

ゲートウェイの URL・発行者 URL（テナント ID を含む）・クライアント ID は、組織を特定できる。公開リポジトリには置かず、セットアップのプロンプトで入力して、この PC のファイルにだけ書く。トークンの保管ファイルも、リポジトリの外に置く。

### 4.3 dotfiles の実装との対応

| 役割 | 入口 |
|---|---|
| 設定を作る（値はプロンプトで入力） | `claude-gateway-setup.cmd` |
| サインイン・トークンを返す | `claude-gateway-token.cmd`（初回は `-Login`） |
| CLI で起動 | `claude-gateway`（`claude-pick gateway`） |
| Zed で起動 | エージェント「Claude Gateway」（`claude-acp-gateway.cmd`） |

手順・ファイルの役割・症状別の対処は、dotfiles の `windows/claude/README.md` の第4章が正。

## 5. 経緯（なぜ遠回りしたか）

用語の見かけが似ていたので、「SSO ならAWS SSO」「ゲートウェイなら Claude apps gateway」と推測して実装を始め、2回作り直した。決め手になったのは、(1) エラー文言（公開アドレスの拒否）、(2) ゲートウェイの名前解決の結果、(3) すでに動いている Claude Desktop の設定画面の項目、の3つ。**案内の用語から推測せず、動いている別のクライアントの設定を先に見る**と、早く正しい型にたどり着ける。

## 6. 要確認事項

- サインインの約1時間後に、`apiKeyHelper` の無音更新が働くか（CLI と Zed の両方）
- Zed の ACP エージェントが、どの時点で `apiKeyHelper` を再実行するか
- 共通の `~/.claude` の設定（permissions、hooks）を、ゲートウェイ用のディレクトリへ引き継ぐ方法
- 組織として、Claude Code からの利用を許可する範囲（ゲートウェイ側で Claude Code のリクエストを許可しているか）
