# room

AI 作業部屋の操作（`open` / `start` / `close` / `umount` / `mask` / `restore`）。人が Windows で実行する。**AI には実行させない**（原本と対応表を読む工程（マスク・復元）を含むため）。設計の理由は `guides/explain/ai-room-why.md`、手作業の手順は `guides/howto/ai-room-setup.md`。

状態: v0（2026-10-12）に、マスク・復元（`maskkit.py`）を足した（2026-10-13、モバイルで実装。**合成データの単体テストのみ。実際の Excel・WSL では未確認**）。実際の WSL（部屋）で、使い捨ての Vault を使って `open → start → close` を通した。

## 使い方

```powershell
cd <このディレクトリ>
uv run room.py open <Project> --area <Area> [--type doc|dev|research] [--boundary <印>] [--commit]
uv run room.py start <Project> [--cmd <部屋で実行するコマンド>] [--no-launch] [--adopt] [--commit]
uv run room.py close <Project> [--commit]
uv run room.py umount --area <Area>
```

- Vault は `$ROOM_VAULT`、無ければ `~/works`。`--vault <パス>` で指定できる（`--vault` はサブコマンドの前に書く）。`close` から reap までの日数は `--reap-days`（既定 14。`$ROOM_REAP_DAYS` でも指定できる）。
- 部屋（WSL のディストリビューション）は `room-<Area>`。先に作っておく（`guides/howto/ai-room-setup.md` の 3・4 章）。
- コミットは、`--commit` を付けたときだけ。対象のパス以外がステージされていたら、コミットしない。

| コマンド | すること |
|---|---|
| `open` | ワークスペースの `.gitignore`（`**/_noai/` と `!**/ai/out/`）と Area の `boundary:` を確認し、`projects/<名>/` に `README.md`、`ai/{docs,in,work,out,records}`、`_noai/{raw,map,final}` を作り、Area の一覧に足す |
| `start` | `area:` とディストロ名の一致、`boundary:`、ほかのマウントが無いこと、`ai/in/` の来歴（manifest）を確認 → README の写しを `ai/ctx/` に置く → `ai/` を `/mnt/room/<名>` に root でマウントし、`in/` を読み取り専用に → 部屋で AI を起動（一般ユーザー）→ **必ず**アンマウントして、マウント点を消し、残りを確認 → 変更の一覧と、追跡されずに無視されているファイルの警告 |
| （`start` の中） | 共有知の写し（方式 A）: `<Vault>/resources/` の `AGENTS.md`、`workflow-kit/`、`exmem/{AGENTS.md,README.md,tags.md,lessons/}`、`guides/` を tar.gz にして、部屋の `~/shared` に読み取り専用で送る（起動のたびに入れ替え。途中では更新しない）。基準コミット（と未コミットの変更の有無）を manifest の `shared` に記録し、`~/shared/ROOM.md` に案内を置く。あわせて、部屋の `~/.claude/CLAUDE.md`（Claude Code が作業ディレクトリによらず読む）に `ROOM.md` への案内を、目印（`room-shared:begin`〜`end`）で囲んだ範囲だけ入れ替えて置く（ほかの内容は変えない）。`resources/` が無ければ送らない。部屋の `~/.claude/CLAUDE.md` に案内を、`~/.claude/settings.json` に `Read(~/shared/**)` の許可（読み取りだけ）を足す |
| `close` | マウントが無いこと、`ai/out/close.md`（部屋の AI が書く）を確認 → 【案件】を Area の `ai/docs/inbox.md` に追記（重複しない）→ README を `status: done`、`closed`、`reap_after` に → Area の一覧を「完了した Project」に → ファイル単位の `git mv` で `archives/` へ（追跡外の `_noai/` も移す） |
| `mask` | `_noai/raw/` の新しい・変わった原本（csv・xlsx）を、`_noai/mask.toml` に従ってマスクし `ai/in/` へ。manifest に原本・マスク後・`mask.toml` のハッシュと対応表の版を記録。語が残っていれば止める（`start` の最初でも自動で行う） |
| `restore` | `ai/out/` を復元して `_noai/final/` へ。戻らないプレースホルダー・未知の形式があれば、何も書かずに一覧を出して止める（`start` の終わりでも自動で行う） |
| `readme` | 部屋の AI が書いた `ai/out/readme-draft.md`（本文だけ）を、`README.md` の本文に反映する（frontmatter は変えず、`updated` だけ今日にする。確認あり、`--yes` で省略）。`open` の判断部分（目的・完了条件）を AI が下書きする形 |
| `stock` | 部屋の AI の【汎用】の下書き（`ai/out/stock/*.md`）を、**1件ずつ人が確認して**（`--yes` で省略）`resources/exmem/inbox/` に運ぶ。frontmatter に `base_commit` と `observed` が要る。対応表の語を含む下書きは運ばない。基準以降に統合先の `lessons/` が変わっていれば、frontmatter に `base_stale` を足す。運んだものは manifest の `stock` に記録し（同じ内容は二度運ばない）、未追跡のまま残す（コミットしない: `stock-hook.md` の方針） |
| `umount` | 部屋に残った `/mnt/room/*` のマウントを外す |

`start --adopt` は、`ai/in/` の現在のファイルを、この Project の入力として人が確認したと manifest に記録する（マスクを通さない入力用）。`start --yes` は、`mask.toml` が変わったときの `ai/in/` 作り直しの確認を省く。`--no-launch` は、起動せずにマウントしたまま待つ（Zed の WSL リモートで使うとき。Enter で、アンマウントと回収に進む）。待つ間、部屋が止まってマウントが消えないよう、部屋で `sleep infinity` を動かす（実機で未確認）。

## 実装の決まり

- WSL へのコマンドは、標準入力で LF 固定で渡す（PowerShell の CRLF で、`umount` が壊れ、マウントが積み重なる）。値は `shlex.quote` で引用する。
- 標準ライブラリだけ。Python は uv で固定する（`.python-version`、`pyproject.toml` の `requires-python`、`uv.lock`）。
- Windows の読み取り専用ファイルは、`chmod` を戻してから消す（`rmtree` が黙って失敗するため）。

## テスト

```powershell
uv run python -m unittest discover -s tests
```

実機（Excel）でマスク・復元を確かめるための架空のダミー（ピボット、コメント、定義名、通常+太字の run をまたぐ語を含む xlsx と、cp932 の csv、`mask.toml`）は、`python tests/dummy_fixture.py <Project のディレクトリ>` で `<Project>/_noai/` に作る（単体テストの対象ではない）。

WSL は差し替えて、一時ディレクトリの git で行う（実際の部屋には触れない）。実際の部屋での通し（`open → start → close`）は、使い捨ての Vault で手動で行った（2026-10-12）。

## マスク・復元（`maskkit.py`）

仕様は `mobile-session/ai-workspace-boundary/ai-room-mask-spec.md`。ファイルは Project の中に置く。

| ファイル | 内容 | git |
|---|---|---|
| `_noai/mask.toml` | 人が書く。`[terms.<種類>] キー = ["正式名", "表記ゆれ", …]`、`[columns] "シート!列名" = "種類"` | しない |
| `_noai/map/mapping.json` | `room` が書く。番号の追記専用の対応表 | しない |
| `_noai/final/` | 復元済みの成果物 | しない |

- プレースホルダー: 本文は `⟦CUST_001⟧`、シート名・定義名は ASCII の `SHEET_001` / `NAME_001`。番号は自動採番で、一度振ったら変わらない。
- 一致は広い（部分一致、大文字小文字・全角半角を区別しない）。長い語を優先して1回で置換する。1文字の語は受け付けない。
- シート名・定義名が語と同じ・語を含むときは、名前全体を `SHEET_` / `NAME_` にする（本文の同じ語もそちらに置換される）。
- xlsx: zip の中の `.xml` / `.rels` / `.vml` を置換。作成者・最終更新者・会社・管理者は常に空にする。プリンタ設定（`printerSettings*.bin`）は削除する。語が複数の書式（run）にまたがる文字列は、1つの run にまとめてから置換する（警告に出る）。点検は全 part と、run を連結した文字列で行う。
- csv: `utf-8-sig` → `cp932` の順に読み、`utf-8-sig` で書く。
- 候補: 法人格・敬称・メール・電話・URL・郵便番号の形は、対応表に無くても警告に出す（止めない）。
- 復元: csv・md・txt・bas・json・html は文字列、xlsx は zip。`ai/out/close.md` と `ai/out/stock/` は対象外。ピボットは Excel の「すべて更新」が要る（人が PC で）。

## 未実装

- reap（期限切れの会話履歴を記録に写して消す）
- 部屋の作成（ディストロ、`wsl.conf`、道具、ログイン）の自動化
