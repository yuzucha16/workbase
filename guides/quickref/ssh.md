---
type: quickref
title: SSH クイックリファレンス
tags:
  - quickref
  - ssh
---

# SSH

## インストール

- Manjaro

  ```shell
  sudo pacman -S openssh
  ```

  

- ubuntu

  ```shell
  sudo apt install openssh-server openssh-client
  ```

## 設定 (サーバー側)

- /etc/ssh/sshd_config

  ```
  Port 22
  PermitRootLogin no
  PasswordAuthentication yes
  ```

- SSHデーモンの起動

  ```shell
  sudo systemctl start sshd.service
  sudo systemctl status sshd.service
  sudo systemctl enable sshd.service
  ```

- ファイヤーウォール (gufw)

  ```
  port 22
  ```

- リンク
  - https://qiita.com/KOJI-YAMAMOTO/items/d0c0faea710c3c56c669
  - https://codechacha.com/ja/ubuntu-install-openssh/

## 設定 (クライアント側)

- ~/.ssh.config

  ```
  Host nuc10
  Hostname 192.168.0.150
  User a036339
  ```

  - https://techblog.nullstack.engineer/entry/ssh_hostname_setting/
