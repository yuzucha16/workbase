---
title: apt cheatsheet
tags:
  - cheatsheet
  - apt
migrated_from: denisidoro/cheats (navi)
---

# apt cheatsheet

## Apt

**Update content listings from package repositories**

```bash
apt update
```

**List all available packages**

```bash
apt list
```

**List all installed packages**

```bash
apt list --installed
```

**Info about package (including description)**

```bash
apt show -a <package-name>
```

**Show versions and archive areas of available package**

```bash
apt list -a <package-name>
```

**Search in repository (packages and description)**

```bash
apt search <query>
```

**Check updates for installed packages**

```bash
apt list --upgradeable
```

**Update all installed packages**

```bash
apt upgrade
```

**Upgrade all installed packages (add/remove dependencies)**

```bash
apt full-upgrade
```

**Update specific/individual package**

```bash
apt install --only-upgrade <package-name>
```

**Downgrade package to a specific version**

```bash
apt install <package-name>=<package-version>
```

**Install a package from repository**

```bash
apt install <package-name>
```

**Remove/delete package**

```bash
apt remove <package-name>
```

**Remove/delete package (with config files)**

```bash
apt purge <package-name>
```

**Install local dpkg package**

```bash
apt install <filepath-deb>
```

**List dependencies of package**

```bash
apt depends <package-name>
```

**List reverse dependencies of package**

```bash
apt rdepends <package-name>
```

**Remove un-needed packages and dependencies**

```bash
apt autoremove
```
