#!/bin/bash
echo admin | sudo -S python3.5 ~/aqm_py/sensor_reader.py &
sleep 20
python3.5 ~/aqm_py/aqm_show.py