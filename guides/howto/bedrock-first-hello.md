---
type: howto
title: AWS Bedrock 開通手順（個人アカウントから「こんにちは」まで）
tags:
  - setup
  - tool/aws
  - ai/claude
---

# AWS Bedrock 開通手順（個人アカウントから「こんにちは」まで）

個人の AWS アカウントを作り、Amazon Bedrock 経由で Claude Code から Claude に「こんにちは」と話しかけるまでの手順書。目的は Bedrock の経験を積むこと。認証と管理の手軽さは、Pro プランの OAuth が上。

- **ゴール（完了の目安）**: Claude Code の `/status` で、プロバイダが Amazon Bedrock、リージョンが意図どおりになっていて、「こんにちは」に応答が返る
- 範囲: AWS アカウントの作成から、Claude Code の接続まで。Zed と Obsidian からの接続は、Claude Code が通ってから（**未着手・要確認**）
- 認証の設計（どの設定ファイルに何を置くか、OAuth に戻す方法）は [[claude-code-auth-providers]]。ここには手順だけを書く
- 秘密（アクセスキー、`AWS_BEARER_TOKEN_BEDROCK`）は、チャットにも git 管理のファイルにも書かない
- 実機では未実施。公式ドキュメント（2026-10-13 に確認）をもとにした草稿

## 対応バージョン表

手順の確認日: 2026-10-13（Web で確認。実機は未確認）。

| 項目 | 内容 | 参照元 |
|---|---|---|
| Claude Code の Bedrock 設定 | `CLAUDE_CODE_USE_BEDROCK=1`、認証は AWS 標準の資格情報チェーン | [Claude Code on Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock) |
| `aws login` | AWS CLI 2.32.0 以上。最大12時間の一時認証情報 | 同上 |
| 料金（Sonnet 5.5） | 入力 $2・出力 $10 / 100万トークン。Anthropic 直接と同額（Global） | [Anthropic の料金ページ](https://platform.claude.com/docs/en/about-claude/pricing) |
| リージョン指定の割増 | 地域固定のエンドポイントは約10%増（Sonnet 5.5 が対象かは AWS の料金ページで**要確認**） | 同上、[AWS Bedrock 料金](https://aws.amazon.com/bedrock/pricing/) |

## 全体の流れ

| 章 | 区分 | 完了の目安 |
|---|---|---|
| 1. AWS アカウントを作る | 手動 | コンソールにルートユーザーでサインインできる |
| 2. ルートユーザーを守る | 手動 | MFA が有効。予算アラートが設定済み |
| 3. 普段使うユーザーを作る | 手動 | Bedrock を呼べる権限のユーザー（または SSO）でサインインできる |
| 4. Bedrock でモデルを有効化する | 手動 | Model catalog で Anthropic モデルの use case フォームを送信済み |
| 5. AWS CLI で認証する | 手動 | `aws sts get-caller-identity` が自分のユーザーを返す |
| 6. Claude Code で繋ぐ | 手動 / スクリプト | `/status` が Bedrock になり、応答が返る |

## 1. AWS アカウントを作る

1. メールアドレス、クレジットカード、電話認証を用意して、アカウントを作る
2. 作成時のユーザーは**ルートユーザー**（何でもできる強い権限）。以後の普段使いにはしない

## 2. ルートユーザーを守る

1. ルートユーザーに MFA を設定する
2. AWS Budgets で予算アラートを作る。**先にやる**（従量課金で、Claude Code の既定モデルは単価の高い Opus のため）

## 3. 普段使うユーザーを作る

| 方式 | 向く場面 | 注意 |
|---|---|---|
| IAM Identity Center（SSO） | 個人利用でも推奨。長期キーを作らずに済む | `aws configure sso` でプロファイルを作る |
| IAM ユーザー | 勤務先でやった要領でよい場合 | アクセスキー（長期）は避ける。作るなら、コンソールのパスワード + MFA だけにして、CLI は `aws login` を使う |

付ける権限（最小）:

- `bedrock:InvokeModel`、`bedrock:InvokeModelWithResponseStream`、`bedrock:ListInferenceProfiles`、`bedrock:GetInferenceProfile`
- 初回の購読用に `aws-marketplace:ViewSubscriptions`、`aws-marketplace:Subscribe`
- ポリシー全文は [公式ページの IAM configuration](https://code.claude.com/docs/en/amazon-bedrock#iam-configuration)

## 4. Bedrock でモデルを有効化する

1. [Bedrock コンソール](https://console.aws.amazon.com/bedrock/) を開き、リージョンを選ぶ（東京は `ap-northeast-1`）
2. Model catalog で Anthropic のモデルを選び、use case フォームを送る。送信すると、すぐ使える
3. **よく忘れる点**: モデルの利用可否は、アカウントとリージョンで違う。使いたいモデル（Sonnet 5.5 など）が見えるか、ここで確認する（新しい世代は、Model access での確認が要る場合がある。**要確認**）

## 5. AWS CLI で認証する

1. AWS CLI（2.32.0 以上）を入れる
2. いずれかでサインインする

   ```bash
   aws login                          # コンソールの認証情報でブラウザ認証（最大12時間）
   # または、SSO の場合
   aws sso login --profile <profile>
   export AWS_PROFILE=<profile>
   ```

3. 確かめる

   ```bash
   aws sts get-caller-identity
   aws bedrock list-inference-profiles --region <region>
   ```

- **やってはいけないこと**: アクセスキーを、チャットや git 管理のファイルに貼らない（共有・公開されうるため）
- **AI 作業部屋（専用 WSL）の中では、1Password CLI（`op`）を使わない**。解錠済みの `op` から、AI が書いたスクリプトで秘密を引き出せるため（[[ai-room-why]] の方針）

## 6. Claude Code で繋ぐ

接続方法は2つ。**この環境では、手順 A（dotfiles のスクリプト）を使う**。

| 方式 | 内容 | 注意 |
|---|---|---|
| A. `claude-bedrock`（推奨） | 専用の設定ファイル（`~/.claude/settings-bedrock.json`）を作り、`claude-bedrock` で起動する。OAuth の `claude` はそのまま残る | スクリプトは偽の `aws` で試験済み。実際の AWS では未実行（[[claude-code-auth-providers]] の Next Actions） |
| B. 公式の `/setup-bedrock` ウィザード | 認証・リージョン・モデルを対話で設定する | 共通の `~/.claude/settings.json` の `env` に書き込むため、OAuth の `claude` まで Bedrock が優先になる。使う前に書き込み先を確認する |

A の手順:

1. dotfiles の `windows/claude/claude-bedrock-setup` を実行する。プロファイル、リージョン、推論プロファイル ID を一覧から選ぶ
2. `claude-bedrock` で起動する
3. `/status` で、プロバイダが Amazon Bedrock か、リージョンが意図どおりかを確かめる
4. 「こんにちは」と送る

**完了の目安**: `/status` が Bedrock で、応答が返る。

## 判断の分かれ目

| 選ぶもの | 選択肢 | 目安 |
|---|---|---|
| モデル | Sonnet 5.5 / Opus 5.5 | 経験のためなら Sonnet 5.5（入力 $2・出力 $10）。ピン留めしないと `opus` は Opus 5.5 に解決される |
| 推論の範囲 | Global / 地域固定 | Global は割増なし。地域固定は約10%増（データの通過リージョンを固定したいときだけ） |
| 認証 | `aws login` / SSO / Bedrock API キー | 一時認証情報の `aws login` か SSO。API キーは短期（最大12時間）ならよい |

## うまくいかないとき

| 症状 | 確認すること |
|---|---|
| "on-demand throughput isn't supported" | モデルを推論プロファイル ID（`apac.` `us.` `global.` 付き）で指定する |
| モデルが見つからない・拒否される | その**リージョン**で、Model catalog のフォームと利用可否を確認する。`aws bedrock list-inference-profiles --region <region>` |
| 認証エラー | `aws sts get-caller-identity` が通るか。通らなければ `aws login` / `aws sso login` をやり直す |
| OAuth の `claude` まで Bedrock になる | `/setup-bedrock` が共通の `settings.json` に書いた可能性。`env` を確認して、A の方式に戻す |

## 要確認事項

- 実機で通していない（個人アカウントがまだ無い）。通したら、確認日と注意点を直す
- Sonnet 5.5 のリージョン指定の割増が、公式ページに明記されているか（AWS の料金ページで確認）
- Zed と Obsidian から Bedrock を使う方法
