#!/usr/bin/env bash

cd /opt/webapp

rm -fR db.sqlite3

/redis-stable/src/redis-server &

sleep 5

python3 manage.py collectstatic --noinput
python3 manage.py migrate
python3 manage.py load
service nginx restart

/usr/bin/supervisord