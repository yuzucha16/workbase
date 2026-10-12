# room

AI 作業部屋の操作（`open` / `start` / `close` / `umount`）。人が Windows で実行する。**AI には実行させない**（将来、原本と対応表を読む工程（マスク・復元）を含むため）。設計の理由は `guides/explain/ai-room-why.md`、手作業の手順は `guides/howto/ai-room-setup.md`。

状態: v0（2026-10-12）。マスク・復元は未実装（次の段階）。実際の WSL（部屋）で、使い捨ての Vault を使って `open → start → close` を通した。

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
| `close` | マウントが無いこと、`ai/out/close.md`（部屋の AI が書く）を確認 → 【案件】を Area の `ai/docs/inbox.md` に追記（重複しない）→ README を `status: done`、`closed`、`reap_after` に → Area の一覧を「完了した Project」に → ファイル単位の `git mv` で `archives/` へ（追跡外の `_noai/` も移す） |
| `umount` | 部屋に残った `/mnt/room/*` のマウントを外す |

`start --adopt` は、`ai/in/` の現在のファイルを、この Project の入力として人が確認したと manifest に記録する（マスクの工程ができるまでの手段）。`--no-launch` は、起動せずにマウントしたまま待つ（Zed の WSL リモートで使うとき。Enter で、アンマウントと回収に進む）。

## 実装の決まり

- WSL へのコマンドは、標準入力で LF 固定で渡す（PowerShell の CRLF で、`umount` が壊れ、マウントが積み重なる）。値は `shlex.quote` で引用する。
- 標準ライブラリだけ。Python は uv で固定する（`.python-version`、`pyproject.toml` の `requires-python`、`uv.lock`）。
- Windows の読み取り専用ファイルは、`chmod` を戻してから消す（`rmtree` が黙って失敗するため）。

## テスト

```powershell
uv run python -m unittest discover -s tests
```

WSL は差し替えて、一時ディレクトリの git で行う（実際の部屋には触れない）。実際の部屋での通し（`open → start → close`）は、使い捨ての Vault で手動で行った（2026-10-12）。

## 未実装

- マスク・復元（`mask.toml`、zip レベルの置換、置換後の点検）
- 【汎用】の下書き（`ai/out/stock/`）の回収
- reap（期限切れの会話履歴を記録に写して消す）
- 部屋の作成（ディストロ、`wsl.conf`、道具、ログイン）の自動化
