---
type: knowledge
title: Windows のアプリを scoop で管理し、管理外を最小にする
status: active
tags:
  - tool/scoop
  - tool/winget
  - tool/powershell
  - windows
  - setup
aliases:
  - scoop管理
  - scoopと管理外アプリ
  - アプリの整理
created: 2026-10-04
updated: 2026-10-06
sources:
  - Claude Code conversation "scoop 管理下と管理外アプリの整理" (2026-10-04)
  - "winget list / pnputil の出力（2026-10-04、Windows 11 Home 10.0.26200）"
  - Claude Code conversation "新しいアカウントでの Scoop 導入の失敗と実行ポリシー" (2026-10-06)
---

# Windows のアプリを scoop で管理し、管理外を最小にする

## Purpose

Windows 11 のアプリを「scoop で管理するもの」と「それ以外」に分け、再構築でも手で入れ直すものを最小の一覧で持てる状態にする。scoop 側の一覧は dotfiles の `manifests/apps.txt`（[[pc-setup-manuals]]）。

## Principles

- scoop を正本にする。同じアプリが scoop と他の経路（winget、手動、Store）に二重に入っている場合は、scoop 側に統一する。
- 「管理外一覧」には、自分が意図して入れたアプリだけを載せる。Windows 標準、Microsoft 製のアプリ・ランタイム、ハードウェアドライバは載せない（依存や OS 更新で変わり、手動管理の対象にならないため）。
- 削除前に、重複に見える項目が本当に別のインストールかを確認する。
- 一覧と manifest は実機の状態に合わせる。実機に無いものを manifest に残さない。

## Decisions

### 二重管理は scoop 版に統一する（2026-10-04）

- 決めたこと: winget に出る二重管理のうち、実体が別だった Notepad++（`C:\Program Files`）と Zed（`AppData\Local\Programs`）は削除し、scoop 版に統一した。
- 根拠: 実体が別で、scoop 側に設定の置き場があるため（[[notepad-plus-plus]]、[[zed-dotfiles]]）。
- 却下案: 重複を残して注記だけにする（バージョンが食い違い、更新対象が曖昧になる）。

### 削除しないもの

- AutoHotkey: winget に出る項目は scoop 自身が登録したものだった。
- Windows Terminal: Win11 標準の Store 版を残す。標準の端末で、scoop 版と並んでも実害が無い。却下案: Store 版の削除（標準アプリを消すリスクが大きい）。

### manifest は実機に合わせる方向で直す

- 未インストールの項目を外し、入っている項目を追記する。却下案: manifest に合わせて scoop install / uninstall する（使っていないものを新たに入れることになる）。

## Facts

2026-10-04、Windows 11 Home 10.0.26200 で確認。

- `winget list` には、scoop が登録した項目も出る。AutoHotkey は、アンインストーラーの場所が scoop の `apps` ディレクトリを指していた。
- 同じ Notepad++ が winget 版 8.8.7（`C:\Program Files\Notepad++`）と scoop 版 8.9.8.1 の両方に入っていた。PATH では scoop の shim が先に使われていた。
- Zed の Inno Setup 版は、アンインストールしても `%APPDATA%\Zed\settings.json` が残った。
- アンインストールしても、レジストリの登録だけが残るケースがある（Emacs で確認）。`winget list` にも残って表示される。
- 管理外一覧を最小にした結果、残ったのは winget の uv、Steam、Sunshine、ViGEm Bus Driver、Bambu Studio と、手動の Dell SupportAssist。
- 仮説（未確認）: KiCad 5.1 のアンインストーラーは KiCad 10 と同じフォルダの直下にある（10 は `10.0` サブフォルダ）ため、フォルダごと消える可能性がある。今回は両方削除済み。

## Gotchas

- **管理者権限のないシェルでは、Program Files のアンインストール、HKLM のレジストリ削除、ドライバの削除ができない**。管理者の PowerShell で別途実行する。
- **ドライバパッケージの `oemNN.inf` の番号は環境ごとに違う**。`pnputil /enum-drivers` の出力を Provider 名（SEGGER、Nordic など）で絞って番号を取り出してから、`pnputil /delete-driver <oemNN.inf> /uninstall /force` を使う。
- **`.vimrc` が `global`（gtags）を呼んでいる場合、manifest から `global` を外すとキーマップが動かなくなる**。外すなら `.vimrc` の記述も一緒に消す。

## Open Questions

- 「管理外一覧」の置き場。dotfiles の `manifests/` には見当たらない（2026-10-04 時点）。README か `docs/` か、どこに持つか未確認。
- Windows Terminal の scoop 版と Store 版を、今後も並べておくか。
- ViGEm Bus Driver は、Sunshine を使わなくなったら一緒に消すか。
- 削除の残骸（J-Link と Nordic のドライバ、Visual Studio Installer、Emacs の登録エントリ）の管理者での削除と、削除後の `winget list` / `pnputil /enum-drivers` での確認（作業は未完了とみられる）。

## Scoop の導入と実行ポリシー（2026-10-06 追記）

新しい Windows アカウントで、バッチ（dotfiles の `20_apps.bat`）からの Scoop 導入が「アクセスが拒否されました。」で失敗した。項目の頭の【汎用】は他の導入スクリプトにも使える内容、【この件】は `20_apps.bat`（2026-10-06）に固有の内容。

### Principles（導入）

- 【汎用】エラー文言（例: `Scoop not found`）でリポジトリを検索して、処理の所在を特定する。報告されたファイル名を、そのまま信じない（今回、`10_env.bat` と報告された処理は、実際は `20_apps.bat` にあった）。
- 【汎用】原因を再現できない失敗では、動いた手順に合わせて直し、失敗時に診断情報（例: `Get-ExecutionPolicy -List`）を出すようにする。却下した仮説は、再現試験の結果とともに残す。次に再発したとき、確認済みの範囲から調べ直せる。
- 【汎用】永続する設定変更（実行ポリシーなど）は、必要なときだけ行い、変更に失敗しても本来の処理は止めない。利用者が意図して設定した厳しい値を無確認で下げず、失敗の理由は本来の処理（インストーラ）が表示する。

### Decisions（導入）

- **Scoop の導入は、実行ポリシーの実効値が Restricted / AllSigned / Undefined のときだけ、CurrentUser を RemoteSigned にしてから行う。変更に失敗しても警告だけで続行する**（2026-10-06）
  - 根拠: Scoop のインストーラは Unrestricted / RemoteSigned / Bypass を要求するので、それ以外のときだけ変えれば足りる。ユーザーの選択。
  - 却下案: 常に `-Force` で RemoteSigned にする（意図して設定した AllSigned 等を無確認で下げる。変更に失敗すると導入が止まる）。
- **導入コマンドは `-ExecutionPolicy Bypass` + `iwr -useb get.scoop.sh | iex` をやめ、実機で成功した形（`Invoke-RestMethod -Uri 'https://get.scoop.sh' | Invoke-Expression`）にする。`powershell.exe` は完全パスで呼ぶ**（2026-10-06）
  - 根拠: 旧コマンドが新しいアカウントで失敗し、ユーザーが成功した手順がこの形だった。完全パスは、PATH とカレントの影響を避けるために足した。
  - 却下案: 旧コマンドのまま（失敗した）。

### Facts（導入）

- 【汎用】Scoop のインストーラ（`get.scoop.sh`、28,743 バイト）は、PowerShell 5 以上、.NET Framework 4.5 以上、`Robocopy.exe`、管理者でないこと（既定）、実行ポリシーが Unrestricted / RemoteSigned / Bypass のいずれかであること、Scoop が未導入であること、を最初に検査する。失敗時のメッセージは英語で、最初の表示は `Initializing...`（確認: 2026-10-06、根拠: インストーラのスクリプトを取得して読んだ。実行はしていない）。
- 【汎用】`Get-ExecutionPolicy`（引数なし）は、Process スコープも含めた実効値を返す。`powershell.exe -ExecutionPolicy <値>` は Process スコープに設定されるので、レジストリを書かずに実効ポリシーを変えられる（確認: 2026-10-06、根拠: 試験で `Restricted` と `AllSigned` を作り、実機の CurrentUser は RemoteSigned のまま）。
- 【汎用】`Set-ExecutionPolicy -Scope CurrentUser` は、そのアカウントのレジストリ（HKCU）に書く。他のユーザーや LocalMachine には影響せず、管理者権限も要らない。グループポリシー（MachinePolicy / UserPolicy）があると、設定は失敗する（仮説）。
- 【この件】失敗の出力に `Initializing...` が無く、「アクセスが拒否されました。」だけが出ていた（確認: 2026-10-06、根拠: ユーザーが貼った出力）。このためインストーラ内の失敗とは考えにくい（仮説）。
- 【この件】「カレントに `powershell` という名前のフォルダがあると、cmd が `powershell` を実行できない」という仮説は、再現せず却下した（確認: 2026-10-06、根拠: Windows 11 10.0.26200 で、`cmd /c` から実行して終了コード0）。
- 【この件】原因は未特定。未検証の候補は、セキュリティ製品や AppLocker によるブロック、新アカウント側から見た `C:\vault` の ACL、新アカウントの LocalMachine の既定が Restricted であること（仮説）。このPCの LocalMachine は RemoteSigned。
- 【この件】効いた原因が RemoteSigned の設定か、`iwr -useb` と `Invoke-RestMethod` の違いかは、切り分けていない（仮説）。
- 【この件】dotfiles の `scripts/windows/20_apps.bat` は、上の Decisions のとおりになっている（確認: 2026-10-06、根拠: バッチの24行目の `Get-ExecutionPolicy` の条件、`Invoke-RestMethod`、`PS_EXE` の完全パス）。

### Gotchas（導入）

- **PowerShell のツール経由で、バッククォートや `\t` を含む日本語の Markdown を、二重引用符の文字列で書き込んだら、文書が壊れた**（`` `20_apps.bat` `` のバッククォートが消え、`` `tests/... `` が「タブ + `ests/...`」になった）: 二重引用符の文字列では、バッククォートがエスケープ文字になる。書き込む本文は、単一引用符のヒアドキュメント（`@'...'@`）か、ファイル書き込み用のツールで渡し、書いた後にタブ文字とバッククォートの有無を検索して確認する。

### Open Questions（導入）

- 新しい Windows アカウントで、修正後の `20_apps.bat` が導入を通すか（未確認）。通らなければ、表示される `Get-ExecutionPolicy -List` と、旧コマンドを手で実行した結果から、原因を絞る。
- 「アクセスが拒否されました。」の原因（上の未検証の候補のどれか）。
- 試験の方法は [[shell-script-testing-wsl]] の「Windows のバッチ」の節。

## suggest と VC++ ランタイム（vcredist2022。2026-10-06 追記）

`scoop install` で、複数のアプリが `extras/vcredist2022` の導入を提案する表示が出る。

### Principles（suggest）

- scoop の `suggest` は任意の提案で、必須の依存（`depends`）ではない。マニフェストの `depends` が空で、表示だけでアプリは動く。表示を失敗として扱わない。
- 管理者権限（UAC）が要る導入は、ユーザースコープのセットアップに自動で組み込まず、必要性の検出と警告にとどめる。管理者権限なしで再現する原則と衝突し、会社の PC で権限が無いと全体が止まる。
- 「入れる判断基準」を先に作り、満たしたときだけ手で入れる。Windows 11 には、他のアプリの導入で既にランタイムが入っていることが多い（仮説）。
- 見落としやすい警告は、色などで目立たせる。長いインストールの出力の中で、1行の警告が流れる。

### Decisions（suggest。すべて 2026-10-06）

- **vcredist2022 は自動導入せず、ランタイムが無いときだけ警告する**。根拠: `extras/vcredist2022` の導入は昇格（UAC）を要し、ユーザースコープ運用と衝突する。ユーザーの依頼（判断基準を作って対応する）に沿って実装し、新しい Windows アカウントで通して問題なしと報告された。ユーザーが現時点の決定として承認した（必要になったら解除する。解除するときは、現在形の記述（スクリプトと README）を直し、この記録は書き換えずに「撤回済み」と理由を足す）。却下案: 一覧（`apps.txt`）に足す（会社 PC で権限が無いと止まる）、`winget install Microsoft.VCRedist.2015+.x64`（これも昇格が要り、経路が増える）、`suggest` の表示を抑える（scoop に抑止の設定は確認できなかった）。
- **入れる判断基準は、次のどれかに当てはまるときだけ**。基準: アプリの起動時に `VCRUNTIME140*.dll` / `MSVCP140*.dll` が無い、または `0xc000007b` のエラー。レジストリの確認が警告になった（x64 が無い）。新品の Windows や VM での最初の通し実行。根拠: 該当しなければ、既にあるランタイムで動く。却下案: 常に入れる。
- **警告と「入っている」の両方の行をオレンジで表示する**。根拠: ユーザーの依頼。見落としがちなため。却下案: 色を付けない。

### Facts（suggest）

- 次のアプリが `suggest` で `extras/vcredist2022` を挙げる: lsd、ripgrep、bat、windows-terminal、starship、chatgpt（確認: 2026-10-06、根拠: 各 `buckets\*\bucket\<app>.json` の `suggest` と、空の `depends`）。bat は `less` も、vim は `vimtutor` も提案する。
- `extras/vcredist2022` は「Microsoft Visual C++ 2015-2022 再頒布可能パッケージ」で、`post_install` が x64 と x86 のインストーラを `-RunAs`（昇格）で動かす。ライセンスは、マニフェストでは `Freeware`（確認: 2026-10-06、根拠: マニフェストの `license` と `post_install`）。
- ランタイムの有無は、レジストリ `HKLM\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\X64` の `Installed` が `1` かで判定できる（確認: 2026-10-06、根拠: Windows 11 10.0.26200 で `reg query` が存在と不存在の両方を正しく判定した）。
- 検査した PC は、scoop に vcredist2022 が入っていなくても、x64 / x86 の「Microsoft Visual C++ v14 Redistributable」14.50.35719 が入っていた（Visual Studio や Build Tools は無し）（確認: 2026-10-06、根拠: アンインストールのレジストリ一覧と `System32\vcruntime140.dll`）。インストールの経路は不明（仮説: アプリのインストーラの同梱か Windows Update）。
- 新しい Windows アカウントでは、ランタイムの警告は出なかった（確認: 2026-10-06、根拠: ユーザーの報告）。
- `less` は、Git for Windows 同梱の `less.exe` が `scoop\apps\git\current\usr\bin\` にあるが、PATH には無い（確認: 2026-10-06、根拠: ファイルの存在と `Get-Command less`）。`bat` が `less` 無しで対話端末のページャをどう扱うかは、未確認（仮説: 出力は出る。パイプ経由では出力が出た）。
- ランタイムが無い環境で警告が実際に表示される（仮説）。「無い」側の判定は、存在しないレジストリキーでの `reg query` でしか確認していない。

### Open Questions / Next Actions（suggest）

- 企業の PC に、この再頒布可能パッケージを入れてよいか（ライセンスと、会社の導入ポリシー）。マニフェストの `Freeware` の表記以上は未確認で、会社の判断になる。
- ランタイムが無い環境で警告が出たとき、`scoop install extras/vcredist2022` で解消するか（UAC が出る）。
- ランタイムが無い環境（新品の Windows や VM）で、警告の表示を確認する（2026-10-06 時点）。

## Related

- [[shell-script-testing-wsl]]
- [[pc-setup-manuals]]
- [[notepad-plus-plus]]
- [[zed-dotfiles]]
