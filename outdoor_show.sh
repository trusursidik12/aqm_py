#!/bin/bash
echo "Reading devices... Please wait!!"
sleep 20s
ls /dev/ttyUSB*
echo "wait for localhost...!!"
sleep 20s
ping 127.0.0.1 -c 5
echo admin | sudo -S python3.5 ~/aqm_py/outdoor.py &
