# Almalinux

## インストール設定

- server (GUI使用)
  - その他空欄
- パーティション
  - /homeを削除して/に割り当て
- ユーザー設定
  - rootのみ．userは後程作るため不要

## セットアップ

- ユーザー作成

  - 管理者: 

  - 非管理者

    ```
    sudo useradd -m guest0
    sudo passwd guest0
    ```

- selinux無効か

  ```
  grubby --update-kernel ALL --args selinux=0
  reboot
  getenforce
  Disabled <--
  ```

- パッケージの最新化 (Kernel除く)

  ```
   dnf -y update --exclude=kernel*
  ```

- セキュリティ対策のため停止するサービス

  ```
  systemctl stop atd.service
  systemctl disable atd.service
  systemctl stop kdump.service
  systemctl disable kdump.service
  systemctl stop lvm2-monitor.service
  systemctl disable lvm2-monitor.service
  systemctl stop mdmonitor.service
  systemctl disable mdmonitor.service
  systemctl stop smartd.service
  systemctl disable smartd.service
  systemctl stop dm-event.socket
  systemctl disable dm-event.socket
  ```

- リポジトリの追加

  - aa

    ```
    dnf config-manager --set-enabled crb
    dnf -y install epel-release
    ```

    ```
    # vi /etc/yum.repos.d/epel.repo
    enabled=1
    priority=10  # ←　優先度を1~99の範囲で指定
    gpgcheck=1
    ```

  - aaa

    ```
    # dnf -y install https://rpms.remirepo.net/enterprise/remi-release-8.rpm
    # dnf -y config-manager --set-enabled remi
    ```

    ```
    # vi /etc/yum.repos.d/remi-safe.repo
    enabled=1
    priority=10   # ←　優先度を1~99の範囲で指定
    gpgcheck=1
    ```

- ネットワークの接続

  - デバイスの確認

  ```
   # nmcli dev s
   wlp0s20u3 wifi 接続済み TP-Link_C6B8
  ```

  - ホスト名の変更

  ```
  \# hostnamectl set-hostname Alma
  ```

  - aaa (nmtui)

    ```
    # sudo vi /etc/sysconfig/network-scripts/ifcfg-TP-Link_C6B8
    IPADDR=192.168.0.10
    PREFIX=24
    GATEWAY=192.168.0.1
    ```

- aaa

  - aaa

    ```
    sudo dnf -y install vim git zsh curl
    ```

    