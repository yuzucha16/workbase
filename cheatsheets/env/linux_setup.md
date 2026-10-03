# Linuxインストール手順
***

## イメージ

- [Manjaro 22.1](https://manjaro.org/download/)
- [Ubuntu 22.04 LTS](https://linuxmint.com/edition.php?id=302)
- [kubuntu 22.04 LTS](https://kubuntu.org/getkubuntu/)
- [Mint 21.1](https://linuxmint.com/edition.php?id=302)

## インストール

- パーティション
  - EFI: FAT32/512MiB/Boot flag
  - Swap: linuxswap/8000MiB/swap flag
  - root: ext4/100000MiB

## ミラーサーバー変更

***
- Manjaro ([refs](https://turtlechan.hatenablog.com/entry/2019/08/25/194849))

  ```shell
  sudo vi /etc/pacman-mirrors.conf
  sudo pacman-mirrors --fasttrack
  sudo vi /etc/pacman.d/mirrorlist
  ```

- Ubuntu

  ```
  sudo sed -i 's/\/\/archive.ubuntu.com/\/\/jp.archive.ubuntu.com/g' /etc/apt/sources.list
  ```

## システムアップデート

***
- Manjaro (25分程度)

  ```shell
  sudo pacman -Syy && sudo pacman -Syu
  ```

- Ubuntu

  ```shell
  sudo apt update && sudo apt upgrade
  sudo apt dist-upgrade
  ```

## システム設定

- 隠しファイル

  ```
  Dolfin -> 右上の三本線 -> 隠しファイルを表示
  ```

- 日本語ディレクトリを英語表記へ変更

  - Manjaro ([refs](https://wiki.archlinux.jp/index.php/XDG_%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA))

    ```shell
    sudo pacman -S xdg-user-dirs-gtk
    LANG=C xdg-user-dirs-gtk-update --force
    ```

  - ubuntu

    ```shell
    LANG=C xdg-user-dirs-update --force
    ```

- ホスト名の変更

  ```shell
  sudo hostnamectl set-hostname littlechacha
  ```

- git
  ```shell
  git config --global user.name "kazend"
  git config --global user.email "kazuyuki.endou7@gmail.com"
  git config --global core.autocrlf false
  ```

## 基本ソフト (共通)

***
- Manjaro (sudo pacman -S)

- Ubuntu (sudo apt install)

  ```shell
  base-devel vim git make cmake gcc zsh curl patch net-tools
  gparted fzf bat ripgrep unzip
  universal-ctags global lcov 
  doxygen graphviz gufw clamtk openssh
  ```
  
  - 無いものもあるので適当に引っ張ってくること．
  - GNOME/GTKの違いで異なるパッケージの場合もあるので注意．


## 開発環境

- Go

  - [本家](https://go.dev/dl/)から最新のバイナリバージョンを取得する．(2023/06時点で 1.20.5)
  
    ```shell
    sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.20.4.linux-amd64.tar.gz
    /usr/local/go/bin/go version
    export PATH=$PATH:/usr/local/go/bin
    go version
    ```
  
    - https://go.dev/doc/install
  
- Rust

  ```shell
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  ~/.cargo/bin/cargo
  ```

  - https://rustup.rs

## 開発ツール

- Manjaro

  ```
  sudo pacman -S yay
  yay -S grub-customizer
  ```

- Ubuntu

  ```shell
  sudo apt install hardinfo nkf autokey-qt openssh-client openssh-server
  ```

- 共通

  - ghq

    ```shell
    /usr/local/go/bin/go install github.com/x-motemen/ghq@latest
    export PATH=$PATH:~/go/bin/ghq
    ```

  - onefetch

    ```shell
    ~/.cargo/bin/cargo install onefetch
    ~/.cargo/bin/onefetch
    ```


## SSH認証

- sshキー作成

  ```shell
  mkdir -p ~/.ssh
  ssh-keygen -t rsa
  vim ~/.ssh/id_rsa.pub
  ```

  - `ssh-keygen` では `$HOME`や`~`を認識しないので `/home/a036339/.ssh/id_rsa` と入力する

- [Github](https://github.com)をホスト登録する (~/.ssh/config)

  ```
  Host github github.com
      HostName github.com
      IdentityFile ~/.ssh/id_rsa
      User git
  ```


## Github接続

- [Github]()にアクセスしてsshキーを登録する

- 初期設定を行う

  ```shell
  git config --global user.name "a036339"
  git config --global user.email "kazuyuki.endo@tdk.com"
  git config --global init.defaultBranch main
  ```
  
- githubへの接続確認を行う

  ```shell
  ssh -T github.com
  ```

  ```
  Hi kazend6140! You've successfully authenticated, but GitHub does not provide shell access
  ```
  

## 日本語入力 & フォント

***
- Manjaro

  ```shell
  sudo pacman -S fcitx-im fcitx-mozc
  sudo pacman -S fcitx-configtool
  ```

- Ubuntu

  ```shell
  sudo apt install fcitx5-mozc kde-config-fcitx5
  im-config -n fcitx5
  ```

  ```shell
  sudo apt install fonts-migmix fonts-takao-pgothic fonts-takao-gothic fonts-takao-mincho
  sudo apt install language-pack-gnome-ja language-pack-gnome-ja-base language-pack-ja language-pack-ja-base firefox-locale-ja thunderbird-locale-ja libreoffice-l10n-ja libreoffice-help-ja
  # \sudo dpkg-reconfigure keyboard-configuration
  ```

- 共通

  - ~/.xprofile

    ```shell
    export GTK_IM_MODULE=fcitx
    export QT_IM_MODULE=fcitx
    export XMODIFIERS=@im=fcitx
    ```
  
  - Myricaフォントのインストール
  
    ```shell
    wget https://github.com/tomokuni/Myrica/raw/master/product/MyricaM.7zip
    unzip ~/Downloads/Myrica.7zip
    cd $HOME/Downloads/Myrica/
    sudo mkdir -p /usr/share/fonts/truetype/myrica
    sudo cp Myrica.TTC /usr/share/fonts/truetype/myrica/
    fc-cache -fv
    ```
  


## aaa

- [dotfiles](https://github.com/kazend6140/dotfiles)をセットアップする

  ```shell
  ~/go/bin/ghq get https://github.com/kazend6140/dotfiles
  cd ~/ghq/github.com/kazend6140/dotfiles/.bin
  zsh install.sh
  ls ~/.zshrc
  ```
  
- Virtual Boxの場合はutil toolをインストールする

  - Ubuntu

    ```shell
    sudo apt install virtualbox-guest-utils
    sudo adduser $USER vboxsf
    ```


- シェルを変更する

  ```shell
  chsh # ログインシェルの変更 /usr/bin/zsh
  sudo chsh -s /usr/bin/zsh
  /usr/bin/zsh # このタイミングでz-plugのインストールが始まる
  vim # このタイミングでvim-plugのインストールが始まるaa
  reboot
  ```
  

# 動作変更
***
```
sudo systemctl enable fstrim.timer # Trim有効化
```

# セキュリティ
***
- [ウイルスソフト](https://in-my-mind.hatenablog.jp/entry/clamtk-2020-06-07)の設定を行う

- [ファイヤーウォール](https://blog2.k05.biz/2020/10/ubuntu-gufw.html)の設定を行う

  

# エラーチェック
***
```
sudo systemctl --failed
sudo journalctl -p 3 -xb
```

# バックアップ
***
- Timeshift
- Grsync

# クリーンアップ

- Manjaro

  ```
  sudo pacman -Scc
  ```

- Ubuntu

  ```shell
  sudo apt autoremove
  ```


## リンク
***
- https://haruka0000.hatenablog.com/entry/2016/09/09/130400
- https://in-my-mind.hatenablog.jp/entry/12things-to-do-after-installing-manjaro-2020-04-18
- https://in-my-mind.hatenablog.jp/entry/clamtk-2020-06-07

