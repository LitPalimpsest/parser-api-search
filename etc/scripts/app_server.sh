#!/bin/sh

PROJECT='litlong'
ADDRESS='127.0.0.1'
PORT=8001
PROJECTLOC="$HOME/dist/current"
PYENVLOC='.pyenv/versions'
GUNICORN="$HOME/$PYENVLOC/$PROJECT/bin/gunicorn"
MANAGELOC="$PROJECTLOC/manage.py"
PID="$HOME/tmp/gunicorn_$PORT.pid"
DEFAULT_ARGS="$PROJECT.production_wsgi:application --workers=5 --daemon --bind=$ADDRESS:$PORT --pid=$PID --timeout=120"
BASE_CMD="$GUNICORN $DEFAULT_ARGS"

start_server () {
  if [ -f $1 ]; then
    #pid exists, check if running
    proc_num=`cat $1`
    num_procs=`ps -p $proc_num | wc -l`
    if [ $num_procs -gt 1 ]; then
       echo "Server already running on ${ADDRESS}:${PORT}"
       return
    fi
  fi
  cd $PROJECTLOC
  echo "starting ${ADDRESS}:${PORT}"
  $BASE_CMD
}

stop_server (){
  proc_num=`cat $1`
  num_procs=`ps -p $proc_num | wc -l`
  if [ -f $1 ] && [ $num_procs -gt 1 ]; then
    echo "stopping server ${ADDRESS}:${PORT}"
    kill -9 `cat $1`
    rm $1
  else
    if [ -f $1 ]; then
      echo "server ${ADDRESS}:${PORT} not running"
    else
      echo "No pid file found for server ${ADDRESS}:${PORT}"
    fi
  fi
}

case "$1" in
'start')
  start_server $PID
  ;;
'stop')
  stop_server $PID
  ;;
'restart')
  stop_server $PID
  sleep 10
  start_server $PID
  ;;
*)
  echo "Usage: $0 { start | stop | restart }"
  ;;
esac

exit 0
