---
type: explain
title: SSL証明書とSSLインスペクション:理解ガイド
tags:
  - explain
  - env
  - tls
  - ssl-inspection
  - tool/git
  - tool/docker
---

# SSL証明書とSSLインスペクション:理解ガイド

Netskope のようなクラウド型プロキシ（SSLインスペクション）がある業務環境で、証明書エラーが出たときに原因を切り分け、対処できるようにするための手順書。
「症状 → 原因 → 対処」を引けるようにし、自分で説明できるところまでを目的とする。

- 前提: 会社のルートCAが Windows 証明書ストアに配布済み。git / docker / WSL / 各言語ランタイムから外部に出る
- 確認状況: 内容は一般論と過去の経験に基づく。**実機での確認は未**（4.5 に要確認事項をまとめる）
- 会社名・社内のCA名・配布方法などの固有情報は、このメモに書かない

## 1. 当時の状況と解決（ダイジェスト）

**状況**

- git / docker で外部リポジトリにアクセスすると、証明書エラーで弾かれる
- Windows のブラウザは通るのに、Win 側の git や WSL では通らない

**原因**

1. Netskope が SSL インスペクションで通信を中継し、**会社CA署名の証明書**をクライアントに提示していた
2. Git for Windows の TLS 実装は OpenSSL で、**独自のCAバンドル**（`ca-bundle.crt`）を見ていた。そこには会社CAがないため「発行元不明」で拒否された
3. ブラウザは Windows 証明書ストアを見る。IT部門が配布した会社CAがそこにあるので通る

**解決**

- `git config --global http.sslBackend schannel` で、Windows 証明書ストアを見る実装に切り替えた
- もしくは、会社CAをバンドルに追加して `http.sslCAInfo` で指定する
- WSL は別のストア（`/etc/ssl/certs`）なので、会社CAを追加して `update-ca-certificates` を実行する

## 2. 理解のための基礎知識

### 証明書とCAチェーン

- 証明書は「このドメインの公開鍵は本物」という、CAによる署名つきの保証
- サーバーは **リーフ → 中間CA → ルートCA** の順に送る。ルートは通常送らず、クライアントが持っている
- クライアントは署名をたどり、**自分の信頼ストアにあるルートCAに到達できるか**を見る。これが信頼のアンカー

### 検証の項目

- 署名の連鎖、有効期限、ホスト名（SAN）、失効状態
- どれか1つでも失敗すると接続を拒否する。ルートに到達できないと `unable to get local issuer certificate` になる

### 信頼ストアは共有されない

- 「OSが信頼している」と「そのアプリが信頼している」は別
- TLS ライブラリごとに、見る場所が違う

| 実装 | 信頼ストア |
|---|---|
| schannel | Windows 証明書ストア |
| OpenSSL | 同梱バンドル、または `/etc/ssl/certs` |
| Python (requests) | certifi 同梱バンドル |
| Node | 同梱バンドル |
| Java | `cacerts` |

### 用語: ストアとバンドル

- **ストア**: OS が管理する証明書の保管場所（Windows 証明書ストアなど）。GUI や API で出し入れする
- **バンドル**: 信頼するルートCAの証明書を、PEM 形式で何枚も連結した **1つのファイル**。ライブラリが直接読み込む
  - 例: Git for Windows の `ca-bundle.crt`、Linux の `/etc/ssl/certs/ca-certificates.crt`、Python certifi の `cacert.pem`
- OpenSSL 系のツールは、OS のストアでなくバンドルのファイルを読む。会社CAを使うには、バンドルの末尾に会社CAの PEM を追記するか、会社CA入りのバンドルを指定する

### SSL インスペクション

- プロキシが TLS を2本に分ける
  - クライアント ⇔ プロキシ: 会社CAで署名したリーフ証明書を、その場で生成して提示
  - プロキシ ⇔ 本物のサーバー: 通常の TLS
- 通るかどうかの分かれ目は「会社CAを信頼しているか」だけ
- 確認は `openssl s_client -connect github.com:443 -showcerts` で行う。issuer が会社CAなら、インスペクションされている

### 自分で説明するときの一言

> プロキシが会社CA署名の証明書に差し替えている。だから、使っている TLS ライブラリの信頼ストアに会社CAがないと弾かれる。ストアはライブラリごとに別なので、対象ごとに会社CAを登録する。

## 3. チェックリスト（症状 → 原因 → 対処）

| 症状 | 原因 | 対処 |
|---|---|---|
| `unable to get local issuer certificate` / `SSL certificate problem` | 信頼ストアに会社CAがない | まず `s_client` で issuer を確認 |
| Win のブラウザは通る、git は不可 | git が OpenSSL の独自バンドルを参照 | `http.sslBackend schannel` に切替、または `http.sslCAInfo` |
| Win は通る、WSL は不可 | Linux 側のストアに会社CAがない | PEM を `/usr/local/share/ca-certificates/` に置き `update-ca-certificates` |
| docker の pull / push だけ不可 | dockerd が見るストアに会社CAがない | ホストのストアに追加、または `/etc/docker/certs.d/` |
| `docker build` 内の `apt` / `curl` が失敗 | イメージ内にCAがない | Dockerfile で会社CAをコピーして登録 |
| pip / requests が失敗 | certifi バンドルを使っている | `REQUESTS_CA_BUNDLE` / `pip config set global.cert` |
| Node / npm が失敗 | Node 同梱バンドルを使っている | `NODE_EXTRA_CA_CERTS` |
| Java が失敗 | `cacerts` に会社CAがない | `keytool -importcert` |
| 追加したのに通らない | リーフを入れた、または中間CAが欠けている | **ルート（必要なら中間）CA**を入れ直す |
| 特定アプリだけ不可 | 証明書ピンニング | Netskope 側でバイパス設定を依頼 |

`sslVerify=false` は検証を無効にするだけで、解決にならない。使わない前提とする。

## 4. 補足

### 4.1 schannel と OpenSSL

| 項目 | schannel | OpenSSL |
|---|---|---|
| 正体 | Windows 標準の TLS 実装（Secure Channel） | オープンソースの TLS / 暗号ライブラリ |
| 提供元 | Microsoft（OS 同梱） | OpenSSL Project |
| 信頼ストア | Windows 証明書ストア | 独自のCAバンドル（`ca-bundle.crt`） |
| 更新 | Windows Update で更新 | git など利用側のバージョンアップに同梱 |
| 会社CAの反映 | GPO / MDM 配布分が自動で反映 | 手動でバンドルに追加が必要 |

**schannel へ切り替えた影響**

- **良い点**: 会社CAをバンドル管理なしで反映でき、CA更新にも追従する
- **失効確認が厳しくなる**: schannel は既定で失効確認（CRL / OCSP）を行う。プロキシ環境で到達できないと `CRYPT_E_NO_REVOCATION_CHECK` で失敗することがある。その場合は `http.schannelCheckRevoke` が論点になる
- **`http.sslCAInfo` が効かなくなる**: schannel では既定で無視される（`http.schannelUseSSLCAInfo` で変更可）
- **TLS バージョンや暗号スイートが OS 依存になる**
- **影響範囲は Win 側の git だけ**: WSL、docker、node などは変わらない

### 4.2 SSL インスペクション導入の経緯（一般論）

1. **以前**: 社内ネットワークの境界（FW / プロキシ装置）が通信を検査していた。社員は社内から外へ出るので、境界で見れば足りた
2. **変化①**: 通信の大半が HTTPS 化し、暗号化されたままでは検査できなくなった。復号して検査する方式が必要になった
3. **変化②**: SaaS / クラウド利用とテレワークで、社外から直接インターネットへ出る通信が増えた。境界での検査が意味を失った
4. **現在**: 検査機能をクラウド側（SASE / SSE。Netskope など）へ移し、端末のエージェントで通信をクラウドへ誘導する。クラウドプロキシが TLS を復号し、マルウェア検知、DLP（情報漏えい防止）、SaaS 利用制御を行う

自社での導入時期や理由は、社内資料で確認して追記する（**要確認**）。

### 4.3 影響を受けやすいモジュール一覧

「システムのストアを見るか、独自バンドルを持つか」で3分類すると、原因の切り分けがしやすい。

#### A. OS / システムのストアを使う（会社CAが反映されやすい）

| モジュール | 備考 |
|---|---|
| ブラウザ（Chrome / Edge） | Windows ストア |
| git（schannel 設定時） | Win 側のみ |
| .NET | Windows ストア |
| curl（Windows 版） | ビルドによる（schannel が多い） |

#### B. システムのストアをそのまま見ない（個別対応が必要）

| モジュール | 見る場所 | 設定 |
|---|---|---|
| git（OpenSSL） | 同梱バンドル / `/etc/ssl/certs` | `http.sslCAInfo` |
| Docker（Go 製） | Linux はシステムストア + `/etc/docker/certs.d/`。Docker Desktop は挙動が異なるため **要確認** | ホストのストアに追加 |
| `docker build` 内の `apt` / `curl` | イメージ内のストア | Dockerfile で登録 |
| WSL 上のツール全般 | `/etc/ssl/certs` | `update-ca-certificates` |

#### C. 言語ランタイムや製品が独自バンドルを持つ（一番忘れやすい）

**C-1. バンドルの場所（ファイルパス）と設定**

| モジュール | バンドルの場所 | 設定 |
|---|---|---|
| Node.js / npm | 実行ファイルに**埋め込み**（ファイルではない） | `NODE_EXTRA_CA_CERTS`、npm は `cafile` |
| Python (requests / pip) | `<site-packages>/certifi/cacert.pem` | `REQUESTS_CA_BUNDLE`、`pip config set global.cert` |
| Java / Maven / Gradle | `$JAVA_HOME/lib/security/cacerts`（JDK8 は `jre/lib/security/cacerts`） | `keytool -importcert` |
| AWS CLI | 同梱（インストール方式でパスが異なる） | `AWS_CA_BUNDLE` |
| Rust (cargo) | OS 依存（Linux は通常 `/etc/ssl/certs/ca-certificates.crt`） | `CARGO_HTTP_CAINFO` |
| Git for Windows（参考） | `C:\Program Files\Git\mingw64\etc\ssl\certs\ca-bundle.crt`（版により `ssl\certs`） | `http.sslCAInfo` |

**C-2. 場所・内容を確認するコマンド**

| モジュール | コマンド |
|---|---|
| Node.js | `node -p "require('tls').rootCertificates.length"`（組込みCAの数）、`echo $NODE_EXTRA_CA_CERTS`（追加分） |
| npm | `npm config get cafile` |
| Python | `python -m certifi`（パス表示）、`python -c "import requests; print(requests.certs.where())"` |
| pip | `pip config list`、`pip config debug` |
| Java | `keytool -list -cacerts`（JDK9 以降。初期パスワードは `changeit`） |
| AWS CLI | `aws configure get ca_bundle`、`echo $AWS_CA_BUNDLE` |
| cargo | `echo $CARGO_HTTP_CAINFO` |
| Git | `git config --list --show-origin`（`sslCAInfo` / `sslBackend` を確認） |
| OpenSSL 全般 | `openssl version -d`（OPENSSLDIR の場所）、`curl -v https://...`（出力の `CAfile:` で使用バンドルを確認） |

**注意点**

- Node はバンドルがファイルではないため、中身は `tls.rootCertificates` で取得する。会社CAは `NODE_EXTRA_CA_CERTS` で**追加**する形になる
- Node 製のツール（VS Code の拡張、AI 系 CLI など）は、`NODE_EXTRA_CA_CERTS` が効くことが多い
- 新しめの Node には、システムストアを使うオプションがある。バージョンによるので **要確認**
- cargo は Windows では schannel を使うビルドが多く、その場合は実質グループ A になる。OS によって分類が変わる
- パスはバージョン・インストール方式で変わる。実機で C-2 のコマンドを実行して確認し、実際の値を追記する

### 4.4 PEM ファイルの要件（拡張子・改行・文字コード）

- `.pem` と `.crt` は慣習的な拡張子で、中身が PEM 形式（Base64 テキスト）なら同じもの。ただし `.crt` は PEM と DER（バイナリ）の両方がありうる
  - 見分け方: `file cert.crt`、または先頭が `-----BEGIN CERTIFICATE-----` か
  - DER → PEM の変換: `openssl x509 -inform der -in cert.crt -out cert.pem`
- **文字コード**: 実質 ASCII のみ。**BOM 付き UTF-8 と UTF-16 は避ける**
  - PowerShell のリダイレクト（`>`）は、バージョンによって UTF-16 で書き出す。`Out-File -Encoding ascii` を使うか、エディタで UTF-8（BOM なし）を指定する
- **改行コード**: LF が標準。CRLF は多くのパーサーで通るが、keytool などで失敗する報告がある。Linux / WSL で使う PEM は LF にする
- **崩れ**: 改行が全くない、行の途中で切れている（Base64 は通常 64 文字で折り返す）と読めない
- **バンドルへの追記**: `cat corp-ca.pem >> ca-bundle.crt`。前の証明書の末尾が改行で終わっていることを確認する（無いと `-----END CERTIFICATE----------BEGIN CERTIFICATE-----` と繋がって壊れる）
- **Windows GUI からのエクスポート**: 証明書エクスポートウィザードで「Base64 encoded X.509 (.CER)」を選ぶと PEM、「DER encoded binary」を選ぶとバイナリ。拡張子ではなく、選んだ形式が中身を決める

### 4.5 要確認事項

- Docker Desktop が会社CAをどこから取り込むか（Linux の dockerd とは挙動が異なる可能性）
- 各ツールの最新バージョンでの仕様（特に Node のシステムストア対応、git の schannel 関連設定）
- schannel 運用時の失効確認（`http.schannelCheckRevoke`）の扱い
- 自社での SSL インスペクション導入の経緯と、会社CAの配布方法
