# <works の名前>

<この works の役割を1〜2行で。`AGENTS.md` の冒頭と同じでよい。>

works（Obsidian の Vault）のトップ。この PC だけのローカルなリポジトリ。規約は `AGENTS.md`、works 全体の規約は `resources/AGENTS.md`。

## 構成

| パス | 内容 | 管理 |
|---|---|---|
| `areas/` `projects/` `archives/` | PARA。この PC のローカルの作業 | このリポジトリ |
| `docs/` `AGENTS.md` `CLAUDE.md` `README.md` | この PC の作業ログと規約 | このリポジトリ |
| `resources/` | 共有ナレッジ（`workbase`）。`.gitignore` で除外する | 別リポジトリ（git 操作は `resources/` の中で行う） |
| `resources_p/` | PC ローカルの resources（この PC だけの情報の置き場） | 追跡しない |
| `repos/` | ghq の root（clone したリポジトリ） | それぞれが別リポジトリ |
| `.obsidian/` | Obsidian の設定。dotfiles からのジャンクション | dotfiles |
