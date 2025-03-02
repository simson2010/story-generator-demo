#!/bin/bash
# save as run_server.sh

# 启动服务并后台运行
nohup python3 app.py > server.log 2>&1 &

echo "服务已启动，PID: $!" > pid