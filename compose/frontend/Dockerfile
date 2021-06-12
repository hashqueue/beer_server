FROM node:12.22.1
COPY ./ /app
WORKDIR /app
RUN yarn config set registry https://registry.npm.taobao.org/ \
    && yarn install \
    && yarn run build

FROM nginx
RUN mkdir -p /app/media \
    && mkdir -p /app/static/admin \
    && mkdir -p /app/static/grappelli \
    && mkdir -p /app/static/rest_framework \
    && mv /etc/apt/sources.list /etc/apt/sources.list.bak \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free" > /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list \
    && apt update \
    && apt install -y netcat
COPY --from=0 /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
WORKDIR /app
COPY deploy_nginx.sh .
RUN chmod +x deploy_nginx.sh

ENTRYPOINT /bin/bash deploy_nginx.sh && echo "The Nginx service is deployed." && nginx -g "daemon off;"