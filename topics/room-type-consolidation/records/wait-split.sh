#!/bin/sh
# 使い方: wait-split.sh <Project> <番号>  start のログに「回収」「マウント解除」が出るまで待つ
L="$HOME/works/projects/$1/_noai/run-p$2.log"
i=0
while [ $i -lt 120 ]; do
  if iconv -f cp932 -t utf-8 "$L" 2>/dev/null | tr -d '\0' | grep -q "回収\|解除\|アンマウント\|終了"; then echo done; exit 0; fi
  sleep 5; i=$((i+1))
done
echo timeout
