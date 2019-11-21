FROM python:3.8-alpine

LABEL maintainer="Marco Orfei <marcoasrorfei@gmail.com>"

RUN apk update \
	&& apk upgrade

RUN apk add --no-cache nginx \
	gcc \
	musl-dev \
	linux-headers \
	openrc \
	pcre \
	pcre-dev

EXPOSE 8080
WORKDIR /app

RUN adduser -D -g 'www' www

RUN mkdir /var/www/html
RUN chown -R www:www /var/www/html

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY nginx.conf /etc/nginx

CMD ["uwsgi", "uwsgi.ini"]
