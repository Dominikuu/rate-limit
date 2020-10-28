  
#!/bin/bash

target=${1-:app}

printf "Running ${target} ...\n"

if [[ "${target}" == celery-worker ]] ; then
    exec celery worker -A app.app:celery -P gevent --concurrency=1000 --loglevel=info
else
    exec gunicorn app.app:app --bind 0.0.0.0:5000 --timeout 180 --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker --worker-connections 1000 --log-level=debug
fi