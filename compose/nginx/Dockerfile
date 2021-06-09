FROM nginx:latest
# 删除默认配置文件
RUN rm /etc/nginx/conf.d/default.conf \
    && chown -R www-data:www-data /usr/share/nginx/html/static/media \
    && chmod -R 775 /usr/share/nginx/html/static/media
# 添加配置文件
COPY ./nginx.conf /etc/nginx/conf.d/