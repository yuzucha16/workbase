---
type: inbox
title: Zed の WSL リモートの Agent に、Bedrock の認証を渡す
tags:
  - tool/zed
  - tool/aws
  - ai/claude
  - tool/wsl
  - security
created: 2026-10-19
sources:
  - Claude Code conversation "Zed の Agent と Bedrock の認証（部屋）"
---

# Zed の WSL リモートの Agent に、Bedrock の認証を渡す

## Goal
分離した WSL の部屋で、IAM ユーザーのアクセスキーを使った Bedrock の認証を、`claude` の直叩きでも、Zed の Agent でも通したかった。シェルの `export` では Zed の Agent に届かないので、値の渡し方を整理する。
統合先の候補: lessons/claude-code-auth-providers.md（キーワード: bedrock, zed, 環境変数, credentials）

## Principles
- Zed の Agent に渡す値は、シェルの `export` でなく、Zed の `agent_servers` の `env` と、ファイル（`~/.aws/credentials`）で渡す。理由: 環境変数はプロセスの作成時に親から子へコピーされるだけで、手で `export` した `bash` は、Zed のサーバーが起動する Agent の祖先にいない。
- 秘密を含まない値（Bedrock を使う設定、リージョン、プロファイル名、モデル ID、証明書のパス）は `env` に、秘密（アクセスキー）はファイルに分ける。理由: Zed の設定は dotfiles などで共有されうる。SDK はファイルを読むので、Agent の起動のしかたに関係しない。
- Bedrock を IAM ユーザーのアクセスキーで使うだけなら、AWS CLI は要らない。理由: Claude Code は環境変数か `~/.aws/credentials` を直接読む。

## Decisions
- **部屋の `~/.aws/credentials` に、秘密を標準入力で渡す `aws-key <Area> --profile <名前>` を足した**（2026-10-19）
  - 根拠: ユーザーが、キーを入れるコマンドを依頼した。画面に出さず（`getpass`）、コマンドラインにもシェルの履歴にも残らず、同名の節だけを置き換え、権限は 600。
  - 却下案: 長期キーを環境変数で毎回 `export`（Zed 経由では届かない）、`op`（1Password CLI）を部屋へ持ち込む（解錠済みの `op` から、AI が秘密を引き出せる）。

## Facts
- 部屋の `claude` は、OAuth 以外の認証（IAM アカウント、SSO など）を、`claude` の画面の操作では設定できなかった。環境変数を `export` すると対応できた（確認: 2026-10-19、根拠: ユーザーの実機の報告）。
- Zed の `agent_servers` の `env` の値は、リモートサーバーの起動時にも引き継がれる。手で `export` する環境変数を減らせ、残るのは秘密（アクセスキー）だけになる（確認: 2026-10-19、根拠: ユーザーの実機の報告）。
- 長期キーのアクセスキー ID と秘密キーを環境変数で `export` すると、`claude` の直叩きでは Bedrock の認証が通った（確認: 2026-10-19、根拠: ユーザーの実機の報告）。
- Zed の `agent_servers` に custom で `command: npx`、`args: ["-y", "@agentclientprotocol/claude-agent-acp"]` と `env` を書くと、部屋の中で Agent が接続できた（確認: 2026-10-19、根拠: ユーザーの実機の報告と設定のキャプチャ）。
- `~/.aws/credentials` を手で書くと、Zed の Agent の Bedrock の認証が通った（確認: 2026-10-19、根拠: ユーザーの実機の報告）。
- 長期キーは、AI から読める場所に残る。Windows 側で `aws sts get-session-token` を使えば、12時間の一時キー（`AWS_SESSION_TOKEN` つき）にできる（仮説。実行していない）。

## Gotchas
- 状況: `aws-key` が、部屋の `~/.aws/credentials` への `touch` で失敗した
  - 原因: 不明（`~/.aws` の所有者が root だった可能性は、ユーザーが取り下げた）
  - 解決: 手で `credentials` を書くと、認証は通った。`aws-key` の失敗は未解決

## Open Questions
- `aws-key` の `touch` 失敗の原因（確認するコマンド: 部屋の中の `id`、`$HOME`、`ls -ld ~ ~/.aws`、`touch` のエラー文）。
- 提案: 長期キーを部屋に置かず、一時キーだけを入れる運用にする（AI の提案。未承認）。

## Next Actions
- `aws-key` の失敗の原因を特定して直し、実機で通す（2026-10-19 時点）。
