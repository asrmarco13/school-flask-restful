FROM python:3.8-alpine

LABEL maintainer="Marco Orfei <marcoasrorfei@gmail.com>"

RUN apk update \
	&& apk upgrade

RUN apk add --no-cache gcc \
	musl-dev \
	linux-headers \
	pcre \
	pcre-dev

EXPOSE 8080
WORKDIR /app

RUN adduser -D -g 'www' www

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uwsgi", "uwsgi.ini"]
