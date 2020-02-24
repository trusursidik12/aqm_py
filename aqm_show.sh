#!/bin/bash
sleep 9
sleep 9
echo admin | sudo -S python3.5 ~/aqm_py/sensor_reader.py &
sleep 9
sleep 9
python3.5 ~/aqm_py/aqm_show.py