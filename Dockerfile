FROM python:3.8
MAINTAINER anonymous
WORKDIR /root/beer_server
COPY . .
RUN apt update && apt upgrade -y && pip3 install -i https://pypi.douban.com/simple -U pip \
    && pip3 install -i https://pypi.douban.com/simple -r requirements.txt \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && python3 manage.py init_admin \
    && python3 manage.py update_global_function_content
CMD ["gunicorn", "--workers=3", "beer_server.wsgi"]