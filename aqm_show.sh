#!/bin/bash
echo admin | sudo -S python ~/aqm_py/sensor_reader.py &
sleep 8
python3.5 ~/aqm_py/aqm_show.py