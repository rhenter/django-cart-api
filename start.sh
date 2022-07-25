#!/bin/bash

NAME="cart_api"                                      # Name of the application
SOURCE_DIR=/opt/app                                        # Source project directory
DJANGO_DIR="${SOURCE_DIR}/src"                             # Django project directory
NUM_WORKERS=6                                              # how many worker processes should Gunicorn spawn
NUM_THREADS=3                                              # how many threads processes should Gunicorn spawn
#BIND_ADDRESS=":8000"                                      # port number used by Gunicorn
BIND_ADDRESS="unix:/tmp/gunicorn.sock"                     # Unix Socket File used by Gunicorn
DJANGO_SETTINGS_MODULE=cart_api.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=cart_api.wsgi                     # WSGI module name
VIRTUALENV_DIR="${SOURCE_DIR}/env"                         # VirtualEnv Path
APPLICATION_MAX_REQUESTS=2000                              # Application max requests
APPLICATION_TIMEOUT=600                                    # Application Timeout
APPLICATION_LOG=${SOURCE_DIR}/logs/cart_api.log      # Application Log

echo "Starting ${NAME} as $(whoami)"

# Activate the virtual environment
cd $DJANGO_DIR
source $VIRTUALENV_DIR/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGO_DIR:$PYTHONPATH

echo "Run Migrations"
python manage.py migrate

echo "Update Static Files"
python manage.py collectstatic --noinput

# Create Log Folder
mkdir -p ${SOURCE_DIR}/logs
rm -rf ${SOURCE_DIR}/logs/*

echo "Run gunicorn"
# --worker-class=eventlet

export GUNICORN_CMD_ARGS="
  --name=$NAME
  --workers=$NUM_WORKERS
  --worker-class=gevent
  --bind=$BIND_ADDRESS
  --umask=777
  --max-requests=$APPLICATION_MAX_REQUESTS
  --timeout=$APPLICATION_TIMEOUT
  --keep-alive=60
  --log-file ${SOURCE_DIR}/logs/gunicorn.log
  --daemon"

echo "Args: ${GUNICORN_CMD_ARGS}"
#$VIRTUALENV_DIR/bin/ddtrace-run gunicorn ${DJANGO_WSGI_MODULE}:application
gunicorn ${DJANGO_WSGI_MODULE}:application

chmod 666 ${SOURCE_DIR}/logs

service nginx restart


tail -f ${SOURCE_DIR}/logs/*
