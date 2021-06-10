FROM node:12.22.1
COPY ./ /app
WORKDIR /app
RUN npm install && npm run build

FROM nginx
RUN mkdir /app
COPY --from=0 /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf \
    && mkdir -p /app/static/media \
    && mkdir -p /app/static/admin \
    && mkdir -p /app/static/grappelli \
    && mkdir -p /app/static/rest_framework
