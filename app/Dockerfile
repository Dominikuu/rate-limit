FROM python:3.7-alpine

WORKDIR /app

ADD . /app

COPY /requirements.txt .

RUN apk add --no-cache openssl-dev python3-dev curl gcc libpq libffi-dev musl-dev linux-headers bash; \
    apk add postgresql-dev

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .