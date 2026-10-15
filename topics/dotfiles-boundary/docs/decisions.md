# dotfiles-boundary: 決定

旧 `dotfiles-boundary-handover.md`（2026-10-12、モバイルでの相談と洗い出しの終了時）の決定と理由を移した。新しい決定は、この下に日付つきで足す。

## 前提（ユーザーが提示。2026-10-12）

1. workbase と dotfiles の公開範囲は未定で、よく変わる。基本は private で、使いたいときだけ public にする。**両方とも public 前提で扱う**（2026-10-12 時点は両方 public）。
2. workbase は main に直接コミットする運用。
3. AI に見せない領域の分離を検討中（`topics/ai-workspace-boundary/`）。

## 2026-10-12 方針

課題: dotfiles（別リポジトリ）を workbase に取り込むか迷っていた。ユーザーが欲しいのは、すぱっと切る理由と、疎な関係。

| # | 内容 | 決めた方法 |
|---|---|---|
| 1 | dotfiles は workbase に取り込まない。別リポジトリのまま | 発言（「進めます」） |
| 2 | 切る線: **PC に置かれる・実行されるもの**は dotfiles、**人か AI が読んで判断・作業するもの**は workbase。迷ったら「PC を作り直すときに要るか」。要るなら dotfiles | 発言（同上） |
| 3 | 依存は **dotfiles → workbase の一方向**だけ。dotfiles が workbase について知るのは、clone の URL と置き場所（`50_repos`）、スキルが読む kit のパスだけ。workbase は dotfiles を名前とリンクでしか呼ばず、スクリプトの中身や挙動を書かない | 発言（同上） |
| 4 | ネックは、dotfiles の挙動を書いた手順書（`guides/howto/`）が workbase にあること。これを dotfiles 側へ移す | 発言（「dotfiles の doc がネック」） |

### 取り込まない理由（ユーザーに示したもの）

- **立ち上げの順番**: dotfiles は新しい PC で最初に clone し、そこから `50_repos` が workbase を `resources/` に置き、`30_link` が `.obsidian` を張る。取り込むと、Vault を作るスクリプトが Vault の中に住む。
- **AI の境界**: workbase は Vault 側の AI が直接コミットする場所。dotfiles は PC を書き換えるスクリプトで、AI 作業部屋の WSL 設定も入る見込み。混ぜると、AI がノートのついでに直したものが、次の PC セットアップでそのまま実行される。
- **規約**: ルートの `AGENTS.md` の「PC ごとのデータを入れない」とぶつかる。
- 公開範囲は、両方 public 前提なので理由にしない（最初に挙げたが取り下げた）。

### 取り込む利点（捨てたもの）

手順書と dotfiles の食い違いチェック（`guides/CLAUDE.md` の付録の規則）と、kit を読むスキルの修正が1回のコミットで済む。→ 手順書を dotfiles へ移せば、手順書とスクリプトが同じリポジトリになり、同じ利点が得られる。

### 既存の原則との関係

[[app-config-placement]] の原則「設定ファイルの管理を2つのリポジトリで相互に参照させない」と、判断基準③「リポジトリ間の依存の向き」を、リポジトリ全体に広げたもの。反映先の第一候補はこのノート。
