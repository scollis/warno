#!/usr/bin/env bash

# Has to be run separately from bootstrap.sh, reason unknown

pip install numpy selenium requests django==1.7 Flask pyyaml gevent
pip install gunicorn psycogreen psutil enum34 sqlalchemy alembic flask_sqlalchemy flask_migrate
pip install requests --upgrade
pip install  /vagrant/data_store/data/pyarmret/