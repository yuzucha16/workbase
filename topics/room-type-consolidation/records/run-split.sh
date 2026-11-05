#!/bin/sh
# 使い方: run-split.sh <Project> <番号>   ai/records/p/p<番号>.txt を stdin で渡して部屋の claude -p を1回動かす
cd "$HOME/works/resources/workflow-kit/room" || exit 1
uv run room.py start "$1" --cmd "claude -p --permission-mode acceptEdits --allowedTools 'Bash WebFetch WebSearch Read Write Edit Glob Grep' < records/p/p$2.txt" > "$HOME/works/projects/$1/_noai/run-p$2.log" 2>&1
