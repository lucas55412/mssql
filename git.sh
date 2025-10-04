#!/bin/bash

# 檢查是否有修改
status=$(git status --porcelain)

if [ -z "$status" ]; then
    echo "沒有新的修改，工作區乾淨 ✅"
else
    # 暫存所有修改
    git add .

    # commit 訊息加上時間
    datetime=$(date '+%Y-%m-%d %H:%M:%S')
    git commit -m "自動同步更新 $datetime"
    git branch -M main
    # push 到遠端（Git 會提示輸入帳號與 Personal Access Token）
    git push origin main


    echo "已同步到遠端 GitHub ✅"
fi