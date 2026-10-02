---
title: shell cheatsheet
tags:
  - cheatsheet
  - shell
migrated_from: denisidoro/cheats (navi)
---

# shell cheatsheet

## Shell Usage

**Re-call last input with sudo**

```bash
sudo !!
```

**Help**

```bash
help cd / help dir (...)
```

**Finding Help**

```bash
apropos directory / apropos search (...)
```

**Define custom startup screen**

```bash
sudo nano /etc/motd
```

**Run a script as background process**

```bash
<process> &
```

**List all running processes**

```bash
ps -A
```

**Kill a running process**

```bash
killall <Process-name>
```

## Shell System

**Get the current path**

```bash
pwd
```

**Get the current hostname**

```bash
hostname
```

**Get the current users**

```bash
users
```

**Show calendar**

```bash
cal
```

**Show today's date**

```bash
date
```

**Exit terminal**

```bash
exit
```

## Shell Permissions

**Use -R option to change permissions recursively.**

```bash
ps -ef | grep apache | grep -v grep
```

**Change group**

```bash
chgrp <group-name-from> <group-name-to>
```

## Shell Directories

**List directory contents**

```bash
ls
```

**List all directory contents**

```bash
ll
```

**List all directory contents sorted by time edited**

```bash
ls -alt
```

**List directory (wildcard matching)**

```bash
ls *.<txt>
```

**List all files of type**

```bash
find . -name '*.<txt>' -print
```

**Go back to previous directory**

```bash
cd -
```

**Make (empty) directory**

```bash
mkdir <dirname>
```

**Remove (empty) directory**

```bash
rmdir <dirname>
```

**Remove directory with all contents without prompt**

```bash
rm -rf <dirname>
```

**Remove directory contents and keep directory**

```bash
rm -rf *
```

**Change directory**

```bash
cd <dirname>
```

## Shell Symlinks

**Create symlink**

```bash
ln -s <source-dirname> <destination-dirname>
```

**Update symlink**

```bash
ln -sfn <source-dirname> <destination-dirname>
```

**Remove symlink**

```bash
unlink <sample-dirname>
```

## Shell Files

**Make (empty) file**

```bash
touch <filename-txt>
```

**Duplicate file**

```bash
cp <filename> <file-copyname>
```

**Copy/Page folder with content**

```bash
cp -a <old-folder>/ <new-folder>
```

**Move/Rename file**

```bash
mv <current-filename-path> <new-filename-path>
```

**Move/Rename file and prompt before overwriting an existing file**

```bash
mv -i <current-filename> <new-filename>
```

**Remove file**

```bash
rm <filename-txt>
```

**Write to file (will overwrite existing content)**

```bash
cat > <filename-txt>
```

**Search for a filename-(not content!) in the current directory**

```bash
find <filename-txt>
```

**Search for a string inside all files in the current directory and subdrectories**

```bash
grep -r <string> *
```

**Search and replace within file**

```bash
sed -i s/<original-text>/<new-text>/g <filename-txt>
```

**MD5 hash for files**

```bash
md5 <filename-txt>
```

**MD5 hash for folders**

```bash
tar c <folder> | md5sum
```

**Encrypt file**

```bash
openssl enc -aes-256-cbc -e -in <sample-filename-txt> -out <sample-encrypted-txt>
```

**Decrypt file**

```bash
openssl enc -aes-256-cbc -d -in <sample-encrypted> -out <sample-filename>
```

## Shell Server

**Access via ssh**

```bash
ssh <username_remote>
```

**Copy file from server to local**

```bash
scp <username_remote>:<file-to-send-path> <path-to-recieve>
```

**Copy file from local to server**

```bash
scp <file-to-send> <username_remote>:<where-to-put>
```

**Escape files with spaces in name like this**

```bash
<path-to-file>\\\ <name-png>
```

## Shell System

**Show disc space**

```bash
df -h
```

**Show disc space (inodes)**

```bash
df -i
```

**Show disc space for current directory**

```bash
du -hs
```

**Current processes (also CPS usage)**

```bash
top or htop
```

**Show running php processes**

```bash
ps aux | grep php
```

**Monitor error log (stream as file grows)**

```bash
tail error.log -f -n 0
```

## Shell Apps

**Start appliction**

```bash
xdg-open <programme>
```

**Open finder with current folder**

```bash
open .
```

## Shell Variables

**Register variable**

```bash
export <TESTING>=<Variable-text>
```

**Echo variable**

```bash
echo $<Variable>
```

**Unset variable**

```bash
unset <Variable>
```

## Shell Output & Redirects

**Write to file**

```bash
echo <Hello> > <hello-txt>
```

**Append content from a file to another file**

```bash
cat <file1-txt> >> <file2-txt>
```

**Add the amount of lines, words, and characters to <file2-txt>**

```bash
cat <file1-txt> | <word-count> | cat > <file2-txt>
```

**Sort the content of a file (like cat)**

```bash
sort <hello-txt>
```

**Save to sorted content to a new file**

```bash
cat <file1-txt> | sort > <sorted-file1-txt>
```

**Sort and remove duplicates and save to a new file**

```bash
sort <file1-txt> | uniq > <uniq-file1-txt>
```
