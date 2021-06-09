FROM python:3.8
WORKDIR /root/beer_server
ENV PYTHONUNBUFFERED=1 DJANGO_SETTINGS_MODULE=beer_server.settings
COPY . .
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free" > /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list \
    && apt update \
    && apt install -y netcat \
    && pip3 install -i https://pypi.douban.com/simple -U pip \
    && pip3 install -i https://pypi.douban.com/simple -r requirements.txt \
    && python3 manage.py collectstatic --noinput \
    && echo "收集静态文件完毕。" \
    && chmod +x ./start_server.sh \
    && /bin/bash ./start_server.sh \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && echo "项目数据迁移完毕。" \
    && python3 manage.py init_admin \
    && python3 manage.py update_global_function_content \
    && echo "初始化系统管理员数据和全局函数文件完毕。"
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0", "beer_server.wsgi"]