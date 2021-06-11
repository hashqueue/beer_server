FROM node:12.22.1
COPY ./ /app
WORKDIR /app
RUN yarn config set registry https://registry.npm.taobao.org/ \
    && yarn install \
    && yarn run build

FROM nginx
RUN mkdir /app \
    && mv /etc/apt/sources.list /etc/apt/sources.list.bak \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free" > /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list \
    && apt update \
    && apt install -y netcat \
    && mkdir -p /app/media \
    && mkdir -p /app/static/admin \
    && mkdir -p /app/static/grappelli \
    && mkdir -p /app/static/rest_framework
COPY --from=0 /app/dist /app
WORKDIR /app
COPY nginx.conf /etc/nginx/nginx.conf
COPY deploy_nginx.sh /app

CMD /bin/bash deploy_nginx.sh && nginx -g "daemon off;"