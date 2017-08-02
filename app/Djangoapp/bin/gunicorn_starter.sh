#!/bin/bash

NAME="wineapp"                                  # Name of the application
DJANGODIR=/home/ubuntu/app/wineapp              # Django project directory
SOCKFILE=/home/ubuntu/app/wineapp/run/gunicorn.sock  # we will communicte using this unix socket
USER=ubuntu                                       # the user to run as
GROUP=ubuntu                                      # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
TIMEOUT=6000
DJANGO_SETTINGS_MODULE=wineapp.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=wineapp.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/ubuntu/app/Djangoapp/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
##command=/home/ubuntu/app/Djangoapp/bin/gunicorn --bind localhost:8000 wineapp.wsgi:application
#exec /home/ubuntu/app/Djangoapp/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
exec /home/ubuntu/app/Djangoapp/bin/gunicorn --bind localhost:8000 wineapp.wsgi:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
