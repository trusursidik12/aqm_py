#!/bin/bash
echo "Reading devices... Please wait!!"
sleep 20s
ls /dev/ttyUSB*
sleep 20s
echo admin | sudo -S python3.5 ~/aqm_py/sensor_reader.py &
sleep 20s
echo "Please wait!!"
python3.5 ~/aqm_py/aqm_show.py