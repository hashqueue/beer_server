#!/bin/bash

while ! nc -z beer 8000 ; do
    echo "正在等待Django后端服务启动..."
    sleep 3
done

echo "Django后端服务已启动完毕。"

