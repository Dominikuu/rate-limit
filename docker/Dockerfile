FROM python:3.7-alpine

WORKDIR /app

ADD . /app

COPY ["requirements.txt", "docker/docker-entrypoint.sh", "./"]

RUN apk add --no-cache python3-dev curl gcc libffi-dev musl-dev linux-headers bash; \
    apk add postgresql-dev; \
    pip install --upgrade pip; \
    pip install --no-cache-dir cython

RUN pip install -r requirements.txt

# CMD python app.py
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT [ "sh", "docker/docker-entrypoint.sh" ]