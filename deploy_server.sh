#!/bin/bash
# 获取当前容器CPU核数
# cpu_core_nums=$(cat /proc/cpuinfo | grep "cores" | uniq | awk '{print $4}')

while ! nc -z mysql 3306 ; do
    echo "正在等待MySQL服务启动..."
    sleep 3
done

echo "MySQL服务已启动完毕。"

while ! nc -z rabbitmq 5672 ; do
    echo "正在等待rabbitmq服务启动..."
    sleep 3
done

echo "rabbitmq服务已启动完毕。"
nohup celery -A beer_server worker -l INFO >> celery.log 2>&1 &
echo "启动Celery异步任务队列服务完毕。即将开始部署Django项目。"
