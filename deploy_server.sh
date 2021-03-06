#!/bin/bash
# è·åCPUæ ¸æ°
cpu_core_nums=$(cat /proc/cpuinfo | grep "cores" | uniq | awk '{print $4}')

while ! nc -z mysql 3306 ; do
    echo "Waiting for the MySQL service to be deployed. ð¿ ð¿ ð¿"
    sleep 3
done

echo "The MySQL service has been deployed. â"

while ! nc -z rabbitmq 5672 ; do
    echo "Waiting for the rabbitmq service to be deployed. ð¿ ð¿ ð¿"
    sleep 3
done

echo "The rabbitmq service has been deployed. â"
nohup celery -A beer_server worker -l INFO >> celery.log 2>&1 &
echo "Celery asynchronous task queue service is deployed. â The Django backend service will be deployed soon. ð¿ ð¿ ð¿"

python3 manage.py collectstatic --noinput \
    && echo "The collection of static files is complete. â" \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && echo "The data migration is complete. â" \
    && python3 manage.py init_admin \
    && python3 manage.py update_global_function_content \
    && echo "The system administrator account and global function file are initialized. â" \
    && gunicorn -w $((cpu_core_nums * 2 + 1)) -b 0.0.0.0 \
    --error-logfile logs/error-gunicorn.log --access-logfile logs/access-gunicorn.log \
    --forwarded-allow-ips="nginx" beer_server.wsgi
