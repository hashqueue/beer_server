FROM python:3.8
WORKDIR /root/beer_server
ENV LANG=C.UTF-8
COPY . .
RUN pip3 install -i https://pypi.douban.com/simple -U pip \
    && pip3 install -i https://pypi.douban.com/simple -r requirements.txt \
    && python3 manage.py collectstatic --noinput \
    && echo "收集静态文件完毕。" \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && echo "项目数据迁移完毕。" \
    && python3 manage.py init_admin \
    && python3 manage.py update_global_function_content \
    && echo "初始化系统管理员数据和全局函数文件完毕。"
    && nohup celery -A beer_server worker -l INFO >> celery.log 2>&1 &
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0", "beer_server.wsgi"]