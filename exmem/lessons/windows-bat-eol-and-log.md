---
type: knowledge
title: 生成した .bat の改行とラベル、セットアップ用 .bat のログ
status: active
tags:
  - tool/wsl
  - shell
  - testing
  - windows
aliases:
  - windows-bat-eol-and-log
triggers: [bat, ラベル, CRLF, LF, 改行, call, pause, SKIP, setx, セットアップ bat, ログ, 環境変数, gitattributes]
created: 2026-10-10
updated: 2026-10-27
sources:
  - Claude Code conversation "release.bat の文字化け" (2026-10-19)
  - Claude Code conversation "セットアップ bat の pause・SKIP ログ・環境変数ログ" (2026-10-10)
---

# 生成した .bat の改行とラベル、セットアップ用 .bat のログ

全体の方針は [[windows-bat-testing]]（Windows の .bat の試験）。2026-10-27 に、windows-bat-testing から切り出した。

## 生成した .bat の改行とラベル、セットアップ用 .bat のログ（2026-10-10 追記）

ファイル作成ツールで新しい `.bat` を作ったところ、`call :LABEL` が失敗した件と、セットアップ用 `.bat`（インストーラ、環境変数の設定）の実行後に状態が分かるログの出し方。同系統（dotfiles の `scripts/windows/`）。

### Principles（改行とラベル）

- 生成ツールで作った `.bat` は、作った直後に改行を CRLF にそろえる。理由: ツールは LF で書くことがあり、`.gitattributes` の `eol=crlf` は `git add` や checkout の時にしか効かないので、作業ツリーの新規ファイルは LF のまま残る（[[git-line-endings]]）。
- ラベル（`call :X`、`goto :X`）を使う `.bat` は、作った直後に、ラベルへ飛ぶ経路を実際に実行して確認する。理由: 構文の確認では見つからず、`The system cannot find the batch label specified` は実行した時にだけ出る。
- 試験から偽のコマンドを `.cmd` で差し込むときは、`.bat` 側の呼び出しに `call` を付ける。理由: `.cmd` を `call` なしで呼ぶと、呼び出し先の終了後に元の `.bat` へ戻らず、後続の処理が実行されない（[[windows-bat-testing]] の Gotchas と同じ）。

### Principles（ログの出し方）

- セットアップ用の `.bat` は、成功・SKIP・エラーのどの経路でも、最後に `pause` で止める。理由: 終わった時点でウィンドウが閉じると、何が行われたか分からなくなる。
- 終了経路を `pause` の1か所に集める。`endlocal & exit /b N` を途中で何か所も書かず、`set "RC=N"` のあと `goto :END` で飛び、`:END` で `pause` してから `endlocal & exit /b %RC%` で終える。理由: 経路ごとに `pause` を書くと、経路を足したときに書き忘れる。
- 何かを設定しない（SKIP する）ときは、`[SKIP]` に「何を設定しなかったか」と「理由」と「どうすれば設定されるか」を書く。例: `[SKIP] <ファイル> not found. SSL bundle not set. Put the CA bundle there and run this script again.`。理由: 理由が無い SKIP は、失敗と見分けがつかない。
- SKIP は、ユーザーが `n` と答えた場合も含め、設定しない理由が何であっても出す（`answered n` と理由に書く）。理由: 設定されなかった事実を、ログだけで確認できるようにする。
- 環境変数を `setx` などで設定したら、設定した変数名と値を、最後にまとめて表示する。設定しなかった変数は `[not set]` と表示する。理由: 後から何が設定されたか把握できる。`setx` は現在のセッションに反映されないので、表示は「新しいターミナルで有効」と添える。
- 環境変数の値の表示は、スクリプト内の専用変数（例 `SHOW_X`）に、実際に設定したときだけ値を入れて行う。`%X%` を直接見ない。理由: 以前から環境に同名の変数があると、設定していないのに設定したように見える。

### Facts（改行とログ）

- 生成ツールで作った LF の `26_uv.bat` は、`call :ASKYN` で `The system cannot find the batch label specified - ASKYN` になった。CRLF に変換すると解消した（確認: 2026-10-10、根拠: 試験スクリプトの実行結果と、変換後の再実行）。
- 同時に作った 2 本（`25_awscli.bat`、`27_volta.bat`）は LF のままでも `:ASKYN` が見つかったかは、確認していない。ラベルの位置（ファイル内のオフセット）に依存する可能性がある（仮説）。
- `.gitattributes` が `*.bat text eol=crlf` でも、`git ls-files --eol` の `w/` 列は作業ツリーの実際の改行を示し、新規ファイルは `w/lf` になる（仮説）。補足: 2026-10-11 の実物では、`scripts/windows/23_claude.bat` が `i/lf w/lf attr/text eol=crlf`、`25_awscli.bat` `26_uv.bat` `27_volta.bat` は `i/lf w/crlf` だった（作業ツリーが LF のままのファイルが実在する）。
- `if defined X echo ...` を括弧のブロックにせず1行で書くと、値に `)` を含むパス（`Program Files (x86)` など）でもブロックが壊れない。`echo` の中で `(` `)` を文字として出すときは `^(` `^)` とエスケープする（確認: 2026-10-10、根拠: 3本の `.bat` を偽のコマンドで実行する試験が全件 PASS）。
- 同じ指示（最後に pause する）を、別の `.bat` を作るたびに再度受けた。先に作った2本は後から pause を足していたが、新しく作った3本には入っていなかった（確認: 2026-10-10、根拠: ユーザーの発言「前にも言った」）。
- 実物（2026-10-11 に照合）: `25_awscli.bat` `26_uv.bat` `27_volta.bat` は、`pause`、`[SKIP]` 3 か所、環境変数の表示（`[ENV]` か `not set`）を持つ。`23_claude.bat` は `pause` が無く、`[SKIP]` が 1 か所で、ラベル（`:ASK` `:SKIP` `:INSTALL`）を持つのに作業ツリーが LF のため、上の予防の対象になる。`10_env.bat` は `pause` と `[SKIP]` が 1 か所ずつで、環境変数のまとめ表示（`[ENV]` `not set`）は見当たらない。

### Gotchas（改行とログ）

- **生成ツールで `.bat` を新規作成し、ラベルを `call` したら失敗した**: ファイルが LF だけで、`cmd` がラベルを見つけられなかった。作業ツリーのファイルを CRLF に変換した（`(?<!\r)\n` を `\r\n` に置換）。
- **試験で偽の `setx.cmd`、`uv.cmd` などを PATH の先頭に置き、`.bat` から呼んだら、最初の呼び出しの後で `.bat` が終了した**: `call` なしで `.cmd` を呼んだため。外部コマンドの呼び出しに `call` を付けた（実物の `.exe` に付けても害はない）。

### Open Questions（改行とログ）

- ラベルが見つからなくなる条件（ファイルの大きさ、ラベルの位置）は特定していない。GitHub の Raw から取得した LF の `.bat` で起きるかは、未検証のまま（[[windows-bat-pitfalls]] の Facts の仮説に対し、生成ツールの LF のファイルで起きた事例が出たので、仮説の根拠は増えた）。
- 新規の `.bat` を作るときの雛形（終了経路の集約、pause、`[ENV]` 表示）を、規則や雛形のファイルに昇格するか。

## Related

- [[windows-bat-testing]]
- [[windows-bat-pitfalls]]
- [[git-line-endings]]
