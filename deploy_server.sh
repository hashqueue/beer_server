#!/bin/bash
# 获取CPU核数
cpu_core_nums=$(cat /proc/cpuinfo | grep "cores" | uniq | awk '{print $4}')

while ! nc -z mysql 3306 ; do
    echo "Waiting for the MySQL service to be deployed..................................."
    sleep 3
done

echo "The MySQL service has been deployed..............................."

while ! nc -z rabbitmq 5672 ; do
    echo "Waiting for the rabbitmq service to be deployed.............................."
    sleep 3
done

echo "The rabbitmq service has been deployed..............................."
nohup celery -A beer_server worker -l INFO >> celery.log 2>&1 &
echo "Celery asynchronous task queue service is deployed. The Django backend service will be deployed soon.................."

python3 manage.py collectstatic --noinput \
    && echo "The collection of static files is complete.............................." \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && echo "The data migration is complete.............................." \
    && python3 manage.py init_admin \
    && python3 manage.py update_global_function_content \
    && echo "The system administrator account and global function file are initialized......................................" \
    && gunicorn --workers $((cpu_core_nums * 2 + 1)) --bind 0.0.0.0 --capture-output \
    --error-logfile logs/gunicorn.log beer_server.wsgi
