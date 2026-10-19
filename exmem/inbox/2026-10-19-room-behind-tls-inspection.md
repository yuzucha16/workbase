---
type: inbox
title: TLS 検査のある PC で、分離した WSL の部屋を立ち上げるときの関所
tags:
  - tool/wsl
  - tls
  - setup
  - security
  - windows
  - tool/zed
created: 2026-10-19
sources:
  - Claude Code conversation "PC1 での room init の障害（証明書・WSLENV・Node）"
---

# TLS 検査のある PC で、分離した WSL の部屋を立ち上げるときの関所

## Goal
`/mnt/c` と interop を切った専用 WSL（AI 作業部屋）を、TLS 検査のある会社 PC で立ち上げたとき、素の環境（検査なし）では出ない障害が連続した。次の PC で、先回りして避けるための関所と対処を残す。
統合先の候補: lessons/ai-isolated-work-room.md（キーワード: wsl, 部屋, 証明書, WSLENV）。広い候補: guides/explain/ssl-inspection.md への1行の追記（ツール別の証明書の一覧は、そこが既にある）

## Principles
- 分離した部屋では、Windows 側の CA bundle を「指定する」方式を取れない（`/mnt/c` が見えない）。会社のルート証明書は、人が指定した少数の証明書だけを、root が部屋のシステムストアへ入れる。理由: 信頼先を最小にでき、`ai` ユーザーは読めても書き換えられない。
- Windows のストア全体を入れない。理由: 数百枚が AI から見える領域に入り、信頼先が不必要に広がる。
- 部屋へ入る `wsl.exe` には、Windows の `WSLENV` を渡さない。理由: `/p` 付きのパスが `/mnt/c` の無い部屋で変換できず、壊れた `SSL_CERT_FILE` などが残って curl が失敗する。環境変数の漏れは、分離の面でも望ましくない。
- 新しい PC では、障害を1つずつ踏む前に、関所を順に確かめる（Facts の一覧）。理由: 今回は、証明書、環境変数の漏れ、Node、環境変数の引き継ぎ、資格情報の5つを順に踏み、検査のない PC では1つも出なかった。

## Decisions
- **会社のルート証明書は、`init --ca-cert <PEM、5枚まで>` で、人が指定したときだけ、root が `/usr/local/share/ca-certificates/` へ入れる**（2026-10-19）
  - 根拠: ユーザーが承認した。入れる前に SHA-256 を表示し、秘密鍵の混入と枚数の超過は、部屋を触る前に止める。
  - 却下案: Windows のストア丸ごと（信頼先が広がる）、環境変数でツールごとに指す（漏れが出て、`ai` が書き換えられる場所に置く）。
- **Node.js は、apt でなく、公式の tarball をチェックサム確認つきで `/usr/local` へ入れる**（2026-10-19）
  - 根拠: ユーザーが依頼した。Zed の Agent が Node 22 以上を要り、Ubuntu 24.04 の apt は 18。
  - 却下案: NodeSource（取得したスクリプトを root で実行する）、apt の版のまま（足りない）。

## Facts
- 部屋の中の `curl https://…` が終了コード 60 で失敗し、部屋から見える証明書の発行元が会社名だった。検査のない PC（PC2）では、同じ手順がそのまま通った（確認: 2026-10-19、根拠: ユーザーの実機の報告）。
- 失敗の直前の apt は通る（http のミラーを使うため）。最初に失敗するのは、uv の取得の `curl https://`（仮説）。
- 入るたびに「failed to translate」が出るのは、`WSLENV` の `/p` 付きのパスが原因。動作には影響しない。`WSLENV` を外して入ると出ない（確認: 2026-10-19、根拠: ユーザーの実機の報告。外して入る確認は未了のため、後半は仮説）。
- 部屋に Node が無いと、Zed の Agent が「npx を知らない」と言う（確認: 2026-10-19、根拠: ユーザーの実機の報告）。
- Node は `npm` も `node` も、システムの証明書ストアを見ない。`npm config set cafile`、`NODE_EXTRA_CA_CERTS` で、システムのバンドル（`/etc/ssl/certs/ca-certificates.crt`）を指す（仮説。ツール別の一覧は `ssl-inspection.md`）。
- Node の公式 tarball（`latest-v24.x` の `SHASUMS256.txt` と照合）の展開と、`node -v` の確認は、Linux のサンドボックスで動いた（確認: 2026-10-19、根拠: スクリプトを実行して v24 を得た）。

関所の一覧（先回り用）:
1. curl の証明書（終了コード 60）→ 会社のルート証明書を部屋へ
2. `WSLENV` の漏れ（failed to translate）→ `WSLENV` を外す
3. Node が無い／古い（Agent の `npx`）→ Node 22 以上を入れる
4. Node・npm・AWS SDK の証明書 → システムのバンドルを指す
5. 資格情報（Bedrock など）。部屋の `claude` は OAuth 以外（IAM アカウント、SSO）の認証を設定できず、環境変数で対応した → 別メモ（`2026-10-19-bedrock-credentials-zed-remote.md`）

## Gotchas
- 状況: 部屋に入るたびに「failed to translate」が出る
  - 原因: Windows の `WSLENV` の `/p` 付きのパスが、`/mnt/c` の無い部屋で変換できない
  - 解決: `WSLENV` を外して `wsl.exe` を起動する（`room shell` を足した。実機の確認は未了）
- 状況: 部屋の curl が証明書エラー（60）になる
  - 原因: TLS 検査のプロキシのルート証明書が部屋に無い。`WSLENV` 経由の壊れた `SSL_CERT_FILE` も重なる
  - 解決: `--ca-cert` で会社のルート証明書を入れた。通った

## Open Questions
- 部屋を Area ごとでなく works 単位にすると、証明書と Bedrock の認証を渡す手間が減るか（ユーザーは様子見）。
- Ubuntu 26.04 LTS をベースにしてよいか（長く使うため）。調べる途中で中断した。
- 提案: 検査のある PC では、`init` が最初に、部屋の curl の発行元を表示して、`--ca-cert` の要否を案内する（AI の提案。未承認）。

## Next Actions
- 次の新しい PC で、関所の一覧どおりに、`init --ca-cert` から Node、Bedrock までを通して、順序と所要を確かめる。
