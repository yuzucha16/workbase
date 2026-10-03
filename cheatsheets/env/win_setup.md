# Installer

## git
- config
  ```shell
  git config --global user.name "kazend"
  git config --global user.email "kazuyuki.endou7@gmail.com"
  git config --global core.autocrlf false
  ```
  
## 開発者向け

- シンボリックリンクが張れる

- `開発者向け設定` をオンにする．
  - `Windows`ボタンから`開発者向け`と検索する



## シンボリックリンクの割り当て権限

ローカルセキュリティポリシー

- ユーザ権利の割り当て
- シンボリックリンクの作成
  - VPNでtdk.bizに参加して`a036339`を追加する

## wsusの一時停止

WSL2(Ubuntu)のインストールで使用する．

- regedit

  ```
  HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\WindowsUpdate
  DoNotConnectToWindowsUpdateInternet = 0
  ```

  - https://penginedu.com/2023-02-04-error-0x8024500c/

## コマンドプロンプト

- 簡易編集モード

## タスクバー

- windows11仕様

  - レジストリの書き換えでタスクバー配置を変更する (TDK環境ではNG)

    ```
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3
    ```

    - 00: Left, 01, Upper, 02: Right, 03: Lower (Default)

  - [Explorer Patcher](https://github.com/valinet/ExplorerPatcher)

## NotepadをNotepad++にする

- Notepad起動時にNotepad++にする

  - レジストリの書き換えを行う

    ```
    HKLM/Software/Microsoft/Windows NT/CurrentVersion/Image File Execution Options/notepad.exe
    ```

    - 右クリック -> 新規 -> 文字列値 -> "Debugger"
    - "C:\Users\a036339\scoop\apps\notepadplusplus\current\notepad++.exe" -notepadStyleCmdline -z /ff
    - [リンク](https://itigic.com/ja/how-to-change-notepad-to-notepad-in-windows/)

## powershell

- ヒストリサイズを変更する (デフォルト: 4096)

  ```
  Set-Variable -Name MaximumHistoryCount -Value 32767
  Get-Variable -Name MaximumHistoryCount
  Get-PSReadLineOption
  ```

  
