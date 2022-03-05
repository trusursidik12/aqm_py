#!/bin/bash
echo "Reading devices... Please wait!!"
sleep 10s
echo raspberry | sudo -S modprobe ftdi_sio
sleep 1s
echo raspberry | sudo -S chmod 666 /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sleep 1s
echo raspberry | sudo -S echo 0403 cc60 >/sys/bus/usb-serial/drivers/ftdi_sio/new_id
sleep 1s
ls /dev/ttyUSB*
echo "wait for localhost...!!"
sleep 1s
ping 127.0.0.1 -c 5
echo raspberry | sudo -S python3 /home/pi/aqm_py/sensor_reader.py &
sleep 5s
chromium-browser --kiosk http://127.0.0.1/aqmmaster?unit=ug
# python3 /home/pi/aqm_py/aqm_show.py