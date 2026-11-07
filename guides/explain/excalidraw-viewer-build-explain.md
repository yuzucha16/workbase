---
type: explain
title: JS・npm・React から、Excalidraw 閲覧スクリプトが HTML になるまで
tags:
  - tool/nodejs
  - tool/npm
  - tool/excalidraw
  - web-basics
  - build
triggers: [npm, npm install, node_modules, package.json, esbuild, bundle, バンドル, JSX, React, Node.js, JavaScript, excalidraw_view, Excalidraw 閲覧, viewer.js, ビルド, minify]
---

# JS・npm・React から、Excalidraw 閲覧スクリプトが HTML になるまで

## 冒頭
Web まわり（JavaScript、Node.js、npm、React、バンドル）を知らなくても、`excalidraw_view.py` が何をして、なぜ初回だけ `npm install` を走らせるのかを、自分で説明できるようにする。前提: Python は分かるが Web の道具立ては初めて。確認状況: 一般論は広く知られた内容（個別の出典は付けていない）。このスクリプトの動きは、`viewer_entry.jsx`・`build_viewer.mjs`・`excalidraw_view.py`・`package.json` を読んで確認した（確認: 2026-11-07、根拠: 4 ファイルの全文）。実際の実行は Windows で確認済み。他の PC は未確認。

## ダイジェスト
- 状況: `.excalidraw`（図の JSON）を人がブラウザで見たい。Python のスクリプトを 1 本動かすと見られるが、初回だけ `npm install` が走り、数分かかり、大きなキャッシュができる。
- 原因: 図を描く部品（Excalidraw）は React で書かれた JavaScript のライブラリで、ブラウザで動く形にするには「依存を取ってきて 1 つの JS に束ねる」作業（ビルド）が要る。その道具が npm と esbuild（どちらも Node.js 上で動く）。
- 解決: 束ねた JS（`viewer.js`）を `~/.cache/excalidraw-viewer` に 1 回だけ作る。2 回目以降は、Python が「図の JSON + viewer.js」を 1 枚の HTML に書き出してブラウザで開くだけで、Node も npm も使わない。

## 基礎知識
### 1. JavaScript と Node.js
- JavaScript（JS）は、もともとブラウザの中で動く言語。HTML の `<script>` に書く。
- Node.js は、ブラウザの外（ターミナル）で JS を動かす実行環境。Python に対する `python` コマンドが、JS では `node`。ここでは「JS で書かれた道具（ビルドツール）を動かす土台」として使う。
- 例えるなら、Node.js は `python`、ブラウザは「Python のコードを表示まで担う別のインタプリタ」。同じ言語を 2 か所で動かせる。

### 2. npm とパッケージ
- npm は Node.js に付く、パッケージ管理（pip に相当）。ライブラリを取ってくる。
- `package.json` が依存の宣言（`requirements.txt` に相当）。このスクリプトのものは 4 つ: `@excalidraw/excalidraw`、`react`、`react-dom`、`esbuild`（版は固定。すべて MIT）（確認: 2026-11-07、根拠: `package.json`）。
- `npm install` は、宣言された依存と、その依存の依存を、すべて `node_modules/` に展開する。数が多く、サイズが大きい（ここでは約 210MB と書いた記録がある。要確認事項を参照）。
- `--ignore-scripts` は、取ってきたパッケージが持つ「インストール後に自動で動くスクリプト」を動かさない指定。安全側に倒すための引数（確認: 2026-11-07、根拠: `excalidraw_view.py` の `build()`）。

### 3. なぜバンドルが要るか
- ブラウザで HTML を開くだけでは、`node_modules/` の多数のファイルを `import` で順に読めない（読めても遅く、ファイルパスの扱いも合わない）。
- バンドラ（束ねる道具）は、入口のファイルから `import` をたどり、必要な部品を 1 つの JS にまとめる。ここでは esbuild を使う。圧縮（minify）もできる。
- 結果は「依存の入った 1 本の JS」。それを HTML に貼れば、`node_modules/` は要らなくなる。これが「ビルド」。

### 4. React と JSX
- React は、画面（UI）を「部品の関数」で書くライブラリ。`<Excalidraw .../>` のような、HTML に似た書き方（JSX）が使える。ブラウザは JSX を直接読めないため、ビルドで普通の JS に変換される。
- `react-dom` は、React の部品を実際の HTML の要素に描画する担当。`createRoot(document.getElementById("root")).render(<App />)` が、HTML の `<div id="root">` に描画する、という意味（確認: 2026-11-07、根拠: `viewer_entry.jsx` の末尾）。
- 位置づけ: Excalidraw 本体が React 製のため、Excalidraw を使う側も React が必要になる。React は目的でなく、Excalidraw を動かすための土台。

### 5. このケースの全体像
役割ごとに分けると次のとおり（確認: 2026-11-07、根拠: 4 ファイルの全文）。

| ファイル | 役割 | いつ動くか |
|---|---|---|
| `package.json` | 依存の宣言（Excalidraw・React・esbuild） | 初回ビルド |
| `viewer_entry.jsx` | 入口。React の画面（図の選択・「SVG を保存」・Excalidraw の閲覧専用表示） | 初回ビルドで束ねられる |
| `build_viewer.mjs` | esbuild を呼ぶ設定。JS と CSS を 1 つの `viewer.js` にする | 初回ビルド |
| `excalidraw_view.py` | 初回はビルドを呼ぶ。以後は、図の JSON と `viewer.js` を 1 枚の HTML にして開く | 毎回 |
| `~/.cache/excalidraw-viewer/` | `src/`（作業場。`node_modules/` を含む）、`viewer.js`、`fonts/` | 初回に作られ、以後は読むだけ |

初回ビルド（`ensure_built` → `build`）の流れ:
1. 3 つのソースを `~/.cache/excalidraw-viewer/src/` へコピーする。
2. `npm install --ignore-scripts --no-audit --no-fund` で依存を `src/node_modules/` に展開する。
3. `node build_viewer.mjs` で、`viewer.js`（JS と CSS を 1 本に束ねたもの）を作る。CSS は、JS が起動時に `<style>` として差し込む形にして、HTML を 1 本のスクリプトで済ませている。
4. Excalidraw が使うフォントを `fonts/` にコピーする。

毎回の流れ（`make_html` → `open_in_browser`）:
1. `.excalidraw` を JSON として読む。
2. HTML を 1 枚の文字列で組み立てる。図の JSON は `window.__EXV_FILES__` に、`viewer.js` は `<script>` の中に、そのまま埋める。フォントの場所は `window.EXCALIDRAW_ASSET_PATH`（キャッシュの `fonts/`）で伝える。
3. 一時ディレクトリの `excalidraw-view.html` に書き、既定のブラウザで開く。
4. ブラウザ側では、`viewer.js` が `window.__EXV_FILES__` を読み、React が図を描く。サーバーは立てていない（`file://` で開くだけ）。

小さな配慮: JSON や JS の中に `</` や `</script` があると HTML が途中で閉じてしまうので、`<\/` に置き換えている（確認: 2026-11-07、根拠: `make_html`）。

- 自分で説明するときの一言: 「Excalidraw は React 製の JS ライブラリなので、npm で取ってきて esbuild で 1 本の `viewer.js` に束ね、キャッシュに置いておく。以後は Python が図の JSON とその `viewer.js` を 1 枚の HTML に埋めてブラウザで開くだけなので、Node は初回しか要らない」

## チェックリスト
| 症状 | 原因 | 対処 |
|---|---|---|
| 「npm が見つかりません」で止まる | Node.js（npm）が PATH に無い | Node.js を入れる。入れたら新しいターミナルを開く |
| 初回の `npm install` が証明書のエラーで失敗する | SSL 検査（仮説）。npm が検査用の証明書を知らない | 出力を残して [[ssl-inspection]] に沿って切り分ける（未確認） |
| 2 回目以降も毎回ビルドが走る | `viewer.js` か `fonts/` がキャッシュに無い | キャッシュの中身を確認する。`--rebuild` で作り直す |
| ページは開くが図の文字が化ける・違う字体になる | `fonts/` の場所がずれている、または消えた | `--rebuild` でフォントを入れ直す |
| 版を上げたい・壊れた疑いがある | キャッシュが古い、または壊れた | `python -I excalidraw_view.py --rebuild` |
| WSL で動かすと node が壊れている | Windows の Volta の node が PATH に漏れている | WSL では動かさない。Windows で動かす。仕組みは [[wsl-windows-path-shim-explain]] |

## 補足
| 用語 | Python での近い対応 | ここでの実体 |
|---|---|---|
| Node.js | `python` コマンド | `node` |
| npm | pip | `npm install` |
| `package.json` | `requirements.txt` | 4 つの依存 |
| `node_modules/` | `site-packages` | キャッシュの `src/node_modules/` |
| バンドラ（esbuild） | 近いものは zipapp / PyInstaller（束ねる点だけ似る） | `build_viewer.mjs` |
| JSX | 無い（テンプレートに近い） | `viewer_entry.jsx` |

- AI がこの HTML を見られるわけではない。ターミナルの AI にはブラウザの描画結果が出ないので、閲覧の目的は人間側にある（ユーザーとの会話で確認した前提）。
- 経緯: Excalidraw の公式 MCP 方式は、ターミナルでは画像・ファイルが出ないため外した（`topics/revealjs-slides` の記録）。

## 要確認事項
- キャッシュの大きさ: スクリプトの冒頭の説明は「約 40MB」、`log.md` は「約 210MB」と書いていて食い違う。PC で実測して直す。
- SSL 検査のある環境で、`npm install` が通るか（未確認）。
- `--ignore-scripts` を付けても Excalidraw のビルドに支障が出ないこと。Windows では支障なし（確認: 2026-11-07、根拠: ユーザーが Windows で表示を確認）。他の PC は未確認。
