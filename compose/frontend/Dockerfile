FROM node:12.22.1
COPY ./ /app
WORKDIR /app
RUN yarn config set registry https://registry.npm.taobao.org/ \
    && yarn install \
    && yarn run build

FROM nginx
RUN mkdir /app
COPY --from=0 /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
COPY deploy_nginx.sh /app
RUN rm /etc/nginx/conf.d/default.conf \
    && mkdir -p /app/static/media \
    && mkdir -p /app/static/admin \
    && mkdir -p /app/static/grappelli \
    && mkdir -p /app/static/rest_framework

CMD /bin/bash deploy_nginx.sh && nginx -g daemon off