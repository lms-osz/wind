#!/bin/bash

PIDPATH="$(dirname $0)/pid"
LOGPATH="$(dirname $0)/logs/$(date +%Y-%m-%d_%H:%M:%S).log"

if [ $# = 0 ]
then
    echo "No parameters!"
    exit
fi

start_server() {
    echo "Staring server . . ."
    nohup python app.py > $LOGPATH 2>&1 &
    echo $! > $PIDPATH
}
stop_server() {
    echo "Stopping server . . ."
    kill $(cat $PIDPATH)
    rm $PIDPATH
}

if [ $1 = "start" ]
then
    start_server
fi
if [ $1 = "stop" ]
then
    stop_server
fi

if [ $1 = "restart" ]
then
    stop_server
    start_server
fi
