---
type: knowledge
title: Claude Code の認証経路とモデル指定（Anthropic 直接と Bedrock）
status: active
tags:
  - ai/claude
  - setup
  - dotfiles
  - tool/powershell
  - testing
aliases:
  - Claude Code の認証
  - Bedrock 設定
  - apiKeyHelper
  - OAuth と API キーの切り替え
created: 2026-10-11
updated: 2026-10-16
sources:
  - Claude Code conversation "Claude Code の認証経路とモデル指定" (2026-10-08)
  - Claude Code conversation "Bedrock 設定の生成と OAuth への切り替え" (2026-10-08)
  - "dotfiles の windows/claude/、tests/windows/、~/.claude/ の設定ファイルの構成（2026-10-11 に確認）"
---

# Claude Code の認証経路とモデル指定（Anthropic 直接と Bedrock）

## Purpose

OAuth（サブスク）に加えて API キー認証や Amazon Bedrock を足すとき、git 管理の設定にどの値を置き、モデルをどう選び、OAuth にどう戻すかをまとめる。権限制御の設計は [[claude-code-permissions]]、履歴の保存場所は [[claude-code-storage]]。

## Principles

- 秘密（API キー、`AWS_BEARER_TOKEN_BEDROCK`、アクセスキー）は git 管理の設定ファイルに書かない。理由: dotfiles は共有・公開されうる。
- 認証経路ごとに設定ファイルを分け、`claude --settings <file>` で選ぶ。共通の `settings.json` にプロバイダ切替の環境変数や `apiKeyHelper` を入れない。理由: それらは OAuth より優先され、共通ファイルに書くと OAuth に戻れなくなる。
- OAuth と API キー・Bedrock の切り替えは、設定ではなく起動のしかた（別の起動関数、別の `--settings` ファイル）で行う。理由: 認証の優先順位は固定（クラウドプロバイダ、`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_API_KEY`、`apiKeyHelper`、OAuth の順）で、設定で OAuth を上げられない。
- OAuth が使われないときは、優先順位の上から、環境変数、ユーザー設定、`--settings` の順に調べる。環境変数は値を出さず、名前と値の長さだけ見る。理由: 値を画面やログに残さないため。
- 環境ごとに違う値（AWS プロファイル名、リージョン、推論プロファイル ID）は、共有されうるリポジトリに実値を置かず、使う PC で一覧から選んで生成する。理由: 実値は環境ごとに違い、書き写しの間違いも防げる。
- モデル ID と利用可否は、環境ごとの一覧コマンドで確認してから設定に書く（Bedrock は `aws bedrock list-inference-profiles --region <リージョン>`、直接は `GET /v1/models`）。理由: ID も可否もアカウントとリージョンで違う。
- 認証が意図どおりかは、起動後に `/status` で確認する。理由: 複数の資格情報が同時にあると、使われているものが見えにくい。
- 外部コマンド（`aws`）に頼るスクリプトは、処理を関数に分けて dot-source し、偽の関数で試験する。実機で通せていない部分は、試験済みの範囲と分けて明記する。理由: その PC に外部コマンドが無くても、組み立ての誤りを先に潰せる（試験の一般論は [[shell-script-testing-wsl]]）。
- 設定ファイルを書き換える公式のセットアップウィザードは、使う前に書き込み先を確認する。理由: 共通の設定ファイルに書くものは、他の認証経路の設定まで変えてしまう。
- 設定名や挙動は、取得ツールの要約だけで信じず、本文で確認する。理由: 要約が `CLAUDE_CODE_USE_BEDROCK` を「fast mode を有効にする変数」と誤記した（Bedrock ページ本文と矛盾）。

## Decisions

すべて 2026-10-08。

- **個人利用は、OAuth（サブスク）と、Anthropic 直接の Console API キー + `apiKeyHelper` の併用にする**（2026-10-15 追記: Bedrock も、経験を積む目的で試す。Claude Code、Zed、Obsidian から繋ぐ予定。手順は [[bedrock-first-hello]]）。根拠: ユーザーの方針（個人利用は直接、併用）。却下案: Bedrock 経由（個人では AWS を使う理由が無い）。
- **API キー側の設定は別ファイルに分け、`--settings` で読む起動関数を作る方式（案A）で進める**。根拠: `apiKeyHelper` が OAuth より認証の優先順位が高く、共通の `settings.json` に書くと常にキー認証になる。ユーザーが案Aを選んだ。却下案: `CLAUDE_CONFIG_DIR` でディレクトリごと分ける案B（設定が二重管理になる）。共通 `settings.json` に `apiKeyHelper` を書く案（OAuth に戻れない）。
- **既定のモデルは、できるだけ安い Sonnet（Sonnet 5.5、`claude-sonnet-5-5`）にする**。根拠: ユーザーが「基本は Sonnet のできるだけ安いモデル」と指示した。Sonnet 5.5 は、Sonnet のうち最安の Sonnet 5 と同額で、キャッシュ読み出しが半額。却下案: Sonnet 5（同額だがキャッシュ読み出しが倍で旧世代）。Sonnet 4.6（入力3ドル・出力15ドルで高い）。Opus / Fable（高額）。
- **Bedrock の設定は、PC ごとに生成するファイルと、セットアップスクリプト、起動関数 `claude-bedrock` にする**。根拠: ユーザーが、API キーのときと同じ要領で、Bedrock の導入もスクリプトにして dotfiles に入れるよう依頼した。方式の細部は AI が選んだ。却下案: 固定のテンプレートを置く（実値を持てず、手で直す手間が残る）。公式の `/setup-bedrock` ウィザード（共通の user settings に書き込み、OAuth の `claude` まで Bedrock 優先になる）。

## Facts

### 認証と設定（確認: 2026-10-08、根拠: code.claude.com の各ページ。特記以外）

- 認証の優先順位は、クラウドプロバイダ（`CLAUDE_CODE_USE_BEDROCK` など）、`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_API_KEY`、`apiKeyHelper`、`CLAUDE_CODE_OAUTH_TOKEN`、Anthropic プロファイル、`/login` のサブスク OAuth の順（authentication ページ）。
- `ANTHROPIC_API_KEY` が環境にあると、初回の承認後にサブスクより優先される。解除は `unset ANTHROPIC_API_KEY`（同ページ）。
- `apiKeyHelper` はシェルコマンドで、標準出力のキーを使う。10秒を超えると警告し、既定で5分ごとに再取得する（`CLAUDE_CODE_API_KEY_HELPER_TTL_MS`。settings-reference ページ）。
- 設定の優先順位は、managed、`--settings`、`.claude/settings.local.json`、`.claude/settings.json`、`~/.claude/settings.json` の順（settings ページ）。
- 設定ファイルで `${VAR}` 展開や外部ファイル参照ができるという記載は、見た範囲の公式ドキュメントに無かった。使えない前提で設計する。
- サブスクの OAuth 資格情報は Windows では `%USERPROFILE%\.claude\.credentials.json` に保存される。`CLAUDE_CONFIG_DIR` を設定するとそのディレクトリ配下になる。dotfiles に含めない（authentication ページ）。
- 公式の `/setup-bedrock` ウィザードは、認証方式、リージョン、モデルのピン留めの結果を、user settings（`~/.claude/settings.json`、`CLAUDE_CONFIG_DIR` があればその下）の `env` に書く（amazon-bedrock ページ）。
- `--settings` で渡したファイルは、既存のユーザー設定に重なって効く。`/status` の Setting sources に `User settings, Command line arguments` が並び、`apiKeyHelper` とモデルのピン留め（`sonnet` が `claude-sonnet-5-5` に解決）が効いた（根拠: ユーザーの実機の `/status`）。
- `apiKeyHelper` に、PATH 上の `.cmd`（内部で `pwsh -File` を呼び、DPAPI で暗号化したキーを復号する）を1語で指定する方式が動いた。`/status` の `Auth token` と `API key` が `apiKeyHelper` になった（根拠: ユーザーの実機の `/status`）。
- API キー認証で起動すると、`claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set and takes precedence over your claude.ai login` という警告が出る。claude.ai のアカウントに紐づく機能が無効になるという意味で、モデルの利用には影響しない（根拠: ユーザーの実機の起動表示）。
- `claude` 単独は、claude.ai の Pro プランの OAuth でログインできた（根拠: ユーザーの発言とログイン表示）。
- PowerShell の SecretManagement（`Get-Secret -AsPlainText`）を `apiKeyHelper` に使えること（仮説）。実機では未実行。

### モデルと料金（2026-10-08 時点）

- モデル指定の環境変数は `ANTHROPIC_MODEL`（セッション）、`ANTHROPIC_DEFAULT_OPUS_MODEL` `_SONNET_MODEL` `_HAIKU_MODEL` `_FABLE_MODEL`（エイリアスの解決先）。優先順位は `--model`、`ANTHROPIC_MODEL`、settings の `model` の順（model-config ページ）。
- `ANTHROPIC_SMALL_FAST_MODEL` は非推奨で、後継は `ANTHROPIC_DEFAULT_HAIKU_MODEL`。`ANTHROPIC_MODEL_FAST_MODE` という変数は model-config と amazon-bedrock のページに記載が無かった。
- Anthropic 直接の料金（USD / 100万トークンの入力・出力）は、Fable 5.1 が 10・50、Opus 5.5 が 4・20、Sonnet 5.5 が 2・10、Haiku 4.5 が 1・5、Haiku 5.5 が 0.10・0.50（100k トークン超のプロンプトは 0.50・2.50）（根拠: platform.claude.com の pricing ページ）。
- Sonnet 5.5 と Sonnet 5 は同額（入力2ドル・出力10ドル）で、キャッシュ読み出しは Sonnet 5.5 が0.10ドル、Sonnet 5 が0.20ドル。Sonnet 4.6 は3ドル・15ドル（同ページ）。
- 設定例で使った直接用のモデル ID は `claude-opus-5-5` `claude-sonnet-5-5` `claude-haiku-4-5`（根拠: claude-api スキルのモデル表）。
- `GET /v1/models?limit=100` は13モデルを返した（`claude-haiku-5-5` を含む）。Opus 4.5 と Haiku 4.5 以外は入力 1,000,000・出力 128,000 トークン、その2つは入力 200,000・出力 64,000。ID に日付が付くのは `claude-opus-4-5-20251101` と `claude-haiku-4-5-20251001`（根拠: ユーザーが実行した `/v1/models` の出力）。
- Anthropic 直接の推論リージョンは `global`（既定）と `us`（1.1 倍）の2択で、日本は選べない。データ保存先（workspace geo）も `us` のみ（data-residency ページ）。
- fast mode は Anthropic 直接（Claude API）のみで、Bedrock では使えない。WebSearch も Bedrock では使えない（pricing ページと Claude Code の amazon-bedrock ページ）。

### Bedrock（確認: 2026-10-08、根拠: amazon-bedrock ページと claude-in-amazon-bedrock ページ）

- 経路が2つある。既定の Invoke API は推論プロファイル ID（`us.anthropic.claude-...`）を使う。Mantle は `CLAUDE_CODE_USE_MANTLE=1` で有効にし、`anthropic.claude-...` をそのまま指定する。
- Global エンドポイントは割増なし、地域固定は 10% 割増。東京 `ap-northeast-1` は Global・JP・単一リージョン、大阪 `ap-northeast-3` は Global・JP に対応する。
- Claude Code は `ap-*` のリージョンで推論プロファイルの接頭辞に `apac.` を優先する。`ANTHROPIC_BEDROCK_REGION_PREFIX`（`us` `eu` `apac` `jp` `au` `global`）で変えられる。
- 認証は、IAM Identity Center の SSO（`aws sso login` と `AWS_PROFILE`）が推奨。`AWS_BEARER_TOKEN_BEDROCK`（短期は最大12時間）が設定されていると、AWS の資格情報チェーンは使われない。期限切れの自動更新は設定の `awsAuthRefresh` に書く。
- IAM には `bedrock:InvokeModel` `InvokeModelWithResponseStream` `ListInferenceProfiles` `GetInferenceProfile` が必要。初回に、Anthropic モデルの use case form の提出が要る。
- ピン留めしないと、`opus` は Opus 5.5、`sonnet` は Sonnet 4.5 に解決され、使えないときは起動時に下位モデルへフォールバックする。Opus だけをピン留めすると、バックグラウンド処理にも Opus が使われうる。
- モデル ID は `anthropic.claude-<モデル>` の形。アカウントの利用可否は、Fable 5.1・Fable 5・Opus 4.8・Sonnet 5・Opus 4.7・Haiku 4.5 が全アカウントに開放、Opus 5.5・Sonnet 5.5・Haiku 5.5 は Model access で確認が必要。
- 推論プロファイルの一覧は、`aws bedrock list-inference-profiles --region <リージョン> --output json` の `inferenceProfileSummaries[].inferenceProfileId` から取れる想定。プロファイルの一覧は `aws configure list-profiles`（仮説）。実際の AWS では未実行。

### 生成スクリプトの試験（確認: 2026-10-08、根拠: 試験スクリプトの実行）

- 生成スクリプトの試験24項目（偽の `aws`、非対話の実行、既存ファイルの拒否、`-DryRun`、不正な接頭辞の拒否、選択の入力）がすべて通る。
- PowerShell で `$null | pwsh -File <script>` のように子プロセスを起こすと、子の `[Console]::IsInputRedirected` が true になり、対話の入力を省いた非対話の経路を試験できる。
- スクリプトが dot-source されたかは、トップレベルで `$MyInvocation.InvocationName -eq '.'` により判定でき、関数だけ定義して `return` で終えられる。

### この PC の実物（確認: 2026-10-11、根拠: ファイルと環境変数の取得。値は出していない）

- 起動関数と設定ファイルの実体（`claude-api-key`、`claude-bedrock-setup`、`settings-api.json`、ACP 用のランチャー）と試験は、dotfiles の `windows/claude/README.md` が正（2026-10-16 に、ファイル一覧とモデルのピン留めの写しを削った）。`settings-api.json` は `~/.claude/` にリンクされ、`apiKeyHelper`、`model`、`env` のモデルのピン留めを持つ。Bedrock の設定は `~/.claude/settings-bedrock.json`（この PC 専用。リポジトリには置かない。秘密を含まない）に生成される。
- PowerShell のプロファイルの起動関数は `claude-api`（`claude --settings "$HOME\.claude\settings-api.json"`）、`claude-bedrock`、`claude-oauth`、`claude-pick`。
- 共通の `~/.claude/settings.json` のキーは `theme` と `permissions` だけで、`env`・`apiKeyHelper` は無い。ユーザー環境変数に `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN`、`CLAUDE_CODE_USE_BEDROCK` は無い。`~/.claude/settings-api-key.dpapi` と `.credentials.json` がある。
- Zed 経由の Claude Code（ACP）のプロセスの環境に、値が空の `ANTHROPIC_API_KEY` が存在する（確認: 2026-10-08、根拠: `Get-ChildItem Env:` の実行。転記元の記録で、再確認は未実施）。

## Gotchas

- **公式ドキュメントを、取得ツールの要約経由で読んだら、`CLAUDE_CODE_USE_BEDROCK` を「fast mode を有効にする変数」と誤記された**: 要約が Bedrock ページ本文と矛盾していた。本文を取得し直して照合した。設定名や挙動は要約だけで信じず、本文で確認する。
- **PowerShell の二重引用符の文字列に `"$Title: ..."` と書いたスクリプトが、読み込み時に構文エラーになった**: `$Title:` が、スコープやドライブの修飾子（`$env:` のような形）として解釈された。変数名を `${Title}` で囲み、`"${Title}: ..."` にした（[[windows-cli-pitfalls]] にも同種の変数の落とし穴がある）。

## Open Questions

- 解決（2026-10-11）: 起動関数の名前の提案（AI の提案、`claude-api`）は、実物のプロファイルに `claude-api` として入っている。明示の承認は未確認のまま、実装され使われている。
- 提案（AI の提案。実機では動いたが、明示の承認は未確認）: キーの保管は DPAPI で暗号化したファイルにする。SecretManagement と 1Password CLI との比較表は、dotfiles の手順書にある。
- Opus と Haiku のピン留めをどのモデルにするか。現在の `settings-api.json` は `claude-opus-5-5` と `claude-haiku-4-5`（暫定と同じ）。一覧には、より安い `claude-haiku-5-5` もあるが、思考を切れない点を含めて未判断。
- 解決（2026-10-15、一部）: Bedrock の Sonnet 5.5 は、Global で Anthropic 直接と同額（入力 $2・出力 $10 / 100万トークン）。地域固定は約10%増と公式ページにあるが、Sonnet 5.5 が対象かは AWS の料金ページで未確認（根拠: platform.claude.com の pricing ページ）。
- 「API キーが優先される」と感じた場面は、ターミナルの `claude` 単独か、`claude-api` を使っているときか。前者なら、その端末の環境変数（`ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN`、`CLAUDE_CODE_USE_BEDROCK`）を調べる。2026-10-11 のこの PC では、ユーザー環境変数にいずれも無い。
- 同じセッションの中で、API キー認証から OAuth へ切り替える手段はあるか（未確認）。
- Bedrock の実際の AWS 環境で、一覧の取得、設定の生成、`claude-bedrock` の起動が通るか。

## Next Actions

- `claude` 単独で起動して `/status` を実行し、OAuth のログインになっていることを確認する（2026-10-08 時点）。
- AWS CLI を入れた PC で、Bedrock のセットアップスクリプトを通し、一覧の出力の形が想定どおりか確認する（2026-10-08 時点）。
- dotfiles のリポジトリに `.credentials.json` が含まれないことを `.gitignore` で確認する。

## Related

- [[claude-code-permissions]]
- [[claude-code-storage]]
- [[claude-code-project-settings]]
- [[shell-script-testing-wsl]]
- [[windows-cli-pitfalls]]
