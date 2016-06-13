#!/usr/bin/env bash

# Has to be run separately from bootstrap.sh, reason unknown

# If Flask is upgraded to 0.11, sometimes it will just stop working, and requests to the user portal will time out
pip install numpy selenium requests django==1.7 Flask==0.10.1 pyyaml gevent
pip install gunicorn psycogreen psutil enum34 sqlalchemy alembic flask-sqlalchemy flask-migrate flask-fixtures
pip install requests --upgrade
pip install  /vagrant/data_store/data/pyarmret/