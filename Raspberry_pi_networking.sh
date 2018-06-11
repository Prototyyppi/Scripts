#!/bin/bash

#######################################
#                                     #
# Script for raspberrypi to start     #
# vwdial and connect to the internet. #
# Monitor also connection and try to  #
# Regain internet if it goes down     #
#                                     #
#######################################

POLL_DELAY=0
TIMEOUT=0
ERRORS=0

connect()
{
  vwdial &
  echo Started vwdial with PID $!
  #Wait for connection
  sleep 10
}

regain_connection()
{
  let "ERRORS++"
  if [ $ERRORS -ge 5 ]; then
    echo Can not regain connection. Reboot.
    reboot
    exit 1
  fi
  PID=$(ps aux | grep vwdial | awk '{print $2}')
  if [ !PID ]; then
    connect
  else
    kill -9 PID
    sleep 5
    connect
  fi
}

if [ $# -ne 1 ]; then
  echo NOK Give polling frequency
  exit 1
fi
POLL_DELAY=$1

while [ 1 ]
do
  ping -c 2 www.google.fi > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo Internet connection gone
    regain_connection
    continue
  fi
  sleep $POLL_DELAY
  ERRORS=0
done
