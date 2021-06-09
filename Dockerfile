FROM python:3.8
WORKDIR /root/beer_server
COPY . .
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free" > /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list \
    && apt update \
    && apt install -y netcat \
    && pip3 install --no-cache-dir -i https://pypi.douban.com/simple -U pip \
    && pip3 install --no-cache-dir -i https://pypi.douban.com/simple -r requirements.txt \
    && chmod +x ./start_server.sh
CMD ["/bin/bash", "./start_server.sh"]