FROM python:3.8
WORKDIR /root/beer_server
COPY . .
RUN apt update \
    && apt install -y netcat \
    && pip3 install -i https://pypi.douban.com/simple -U pip \
    && pip3 install -i https://pypi.douban.com/simple -r requirements.txt \
    && chmod +x ./start_server.sh
CMD ["/bin/bash", "./start_server.sh"]