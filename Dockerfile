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
    && python3 -m venv venv \
    && source venv/bin/activate \
    && pip3 install -i https://pypi.douban.com/simple -U pip \
    && pip3 install -i https://pypi.douban.com/simple -r requirements.txt \
    && python3 manage.py collectstatic --noinput \
    && echo "收集静态文件完毕。" \
    && chmod +x ./deploy_server.sh
CMD ["/bin/bash", "./deploy_server.sh"]