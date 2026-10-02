---
title: git cheatsheet
tags:
  - cheatsheet
  - git
migrated_from: denisidoro/cheats (navi)
---

# git cheatsheet

## Git

**Set global git user name**

```bash
git config --global user.name <name>
```

**Set global git user email**

```bash
git config --global user.email <email>
```

**Initializes a git repository**

```bash
git init
```

**Clone a git repository**

```bash
git clone -b <branch_name> <repository> <clone_directory>
```

**Shallow clone with depth 1 with all branches and submodules**

```bash
git clone --depth=1 --no-single-branch --recurse-submodules <repository> <clone_directory>
```

**Rebase upstream master into local/origin master (use if people don't clone your repository)**

```bash
git fetch <remote_name>
git checkout master
git rebase <remote_name>/master
git fetch --unshallow origin
git push -f origin master
```

**Merge upstream master into local/origin master (use if people clone your repository)**

```bash
git fetch <remote_name>
git checkout master
git merge <remote_name>/master
git fetch --unshallow origin
git push -f origin master
```

**View all available remote for a git repository**

```bash
git remote --verbose
```

**Adds a remote for a git repository**

```bash
git remote add <remote_name> <remote_url>
```

**Renames a remote for a git repository**

```bash
git remote rename <old_remote_name> <new_remote_name>
```

**Remove a remote for a git repository**

```bash
git remote remove <remote_name>
```

**Checkout to branch**

```bash
git checkout <branch>
```

**Displays the current status of a git repository**

```bash
git status
```

**Displays unstaged changes for file**

```bash
cd <toplevel_directory>; \
    git diff <unstaged_files>
```

**Stage single or multiple files**

```bash
cd <toplevel_directory>; \
    git add <changed_files>;
```

**Stage all files in project**

```bash
git add -A
```

**Create commit for staged files**

```bash
git commit -m "<commit_description>"
```

**Create backdated commit for staged files**

```bash
git commit --date="<number_of_days_ago> days ago" -m "<commit_description>"
```

**Pushes committed changes to remote repository**

```bash
git push -u <remote_name> <branch_name>
```

**Pushes changes to a remote repository overwriting another branch**

```bash
git push <remote_name> <branch>:<branch_to_overwrite>
```

**Overwrites remote branch with local branch changes**

```bash
git push <remote_name> <branch_name> -f
```

**Pulls changes to a remote repo to the local repo**

```bash
git pull --ff-only
```

**Merges changes on one branch into current branch**

```bash
git merge <branch_name>
```

**Abort the current conflict resolution process, and try to reconstruct the pre-merge state.**

```bash
git merge --abort
```

**Displays log of commits for a repo**

```bash
git log
```

**Displays formatted log of commits for a repo**

```bash
git log --all --decorate --oneline --graph
```

**Clear everything**

```bash
git clean -dxf
```

**Sign all commits in a branch based on master**

```bash
git rebase master -S -f
```

**Checkout a branch from a fork**

```bash
git fetch origin pull/<pr_number>/head:pr/<pr_number> \
   && git checkout pr/<pr_number>
```

**Add a new module**

```bash
git submodule add <repository> <path>
```

**Update module**

```bash
git submodule update --init
```

**Update module without init**

```bash
git submodule update
```

**Pull all submodules**

```bash
git submodule foreach git pull origin master
```

**Update all submodules**

```bash
git submodule update --init --recursive
```

**Skip git hooks**

```bash
git commit --no-verify
```

**Create new branch from current HEAD**

```bash
git checkout -b <new_branch_name>
```

**Remove commits from local repository (destroy changes)**

```bash
git reset --hard HEAD~<number_of_commits>
```

**Remove commits from local repository (keep changes)**

```bash
git reset --soft HEAD~<number_of_commits>
```
