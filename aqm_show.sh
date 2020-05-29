#!/bin/bash
echo "Reading devices... Please wait!!"
sleep 20s
echo admin | sudo modprobe ftdi_sio &
echo admin | sudo chmod 666 /sys/bus/usb-serial/drivers/ftdi_sio/new_id &
echo admin | sudo echo 0403 cc60 >/sys/bus/usb-serial/drivers/ftdi_sio/new_id &
ls /dev/ttyUSB*
echo "wait for localhost...!!"
sleep 20s
ping 127.0.0.1 -c 5
echo admin | sudo -S python3.5 ~/aqm_py/sensor_reader.py &
sleep 10s
python3.5 ~/aqm_py/aqm_show.py