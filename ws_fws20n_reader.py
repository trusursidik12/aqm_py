import usb.core
import time
import struct
import math
import datetime
from mysql.connector.constants import ClientFlag
import mysql.connector

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] WS FWS20N Database CONNECTED")
except Exception as e: 
    print("[X]  WS FWS20N " + e)

VENDOR = 0x1941
PRODUCT = 0x8021
WIND_DIRS = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
is_WS_connect = False

def open_ws():
    global is_WS_connect
    usb_device = usb.core.find(idVendor=VENDOR, idProduct=PRODUCT)
    if usb_device is None:
        raise ValueError('Device not found')
    
    try:
        usb_device.get_active_configuration()

        if usb_device.is_kernel_driver_active(0):
            usb_device.detach_kernel_driver(0)

        time.sleep(5)
        return usb_device
    except Exception as e:
        is_WS_connect = False
        return None
        


def read_block(device, offset):
    least_significant_bit = offset & 0xFF
    most_significant_bit = offset >> 8 & 0xFF
    # Construct a binary message
    tbuf = struct.pack('BBBBBBBB', 0xA1, most_significant_bit, least_significant_bit, 32, 0xA1, most_significant_bit, least_significant_bit, 32)
    timeout = 1000  # Milliseconds
    retval = dev.ctrl_transfer(0x21, 0x09, 0x200, 0, tbuf, timeout)
    return dev.read(0x81, 32, timeout)

try:
    while True:
        try:
            if (is_WS_connect == False):
                dev = open_ws()
                dev.set_configuration()

            fixed_block = read_block(dev, 0)

            if (fixed_block[0] != 0x55):
                raise ValueError('Bad data returned')
            else:
                is_WS_connect = True

            curpos = struct.unpack('H', fixed_block[30:32])[0]
            current_block = read_block(dev, curpos)

            indoor_humidity = current_block[1]
            tlsb = current_block[2]
            tmsb = current_block[3] & 0x7f
            tsign = current_block[3] >> 7
            indoor_temperature = (tmsb * 256 + tlsb) * 0.1

            if tsign:
                indoor_temperature *= -1

            outdoor_humidity = current_block[4]
            tlsb = current_block[5]
            tmsb = current_block[6] & 0x7f
            tsign = current_block[6] >> 7
            outdoor_temperature = (tmsb * 256 + tlsb) * 0.1

            if tsign:
                outdoor_temperature *= -1

            abs_pressure = struct.unpack('H', current_block[7:9])[0]*0.1	
            
            wind = current_block[9]
            wind_extra = current_block[11]
            wind_dir = current_block[12]

            total_rain = struct.unpack('H', current_block[13:15])[0]*0.3
            wind_speed = (wind + ((wind_extra & 0x0F) << 8)) * 0.36

            WS = str(datetime.datetime.now()) + ";0;" + str(abs_pressure/33.8639) + ";" + str((indoor_temperature*9/5)+32) + ";" + str(indoor_humidity) + ";" + str((outdoor_temperature*9/5)+32) + ";" + str(round(wind_speed,2)) + ";" + str(round(wind_speed,2)) + ";" + str(WIND_DIRS[wind_dir]) + ";" + str(outdoor_humidity) + ";" + str(total_rain) + ";0;0;0.0;0;" + str(total_rain) + ";0;0"

            print("fixed_block : " + str(fixed_block))
            print("curpos : " + str(curpos))
            print("current_block : " + str(current_block))
            print(WS)
            sql = "UPDATE aqm_sensor_values SET WS = '" + WS + "' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        except Exception as e2:
            try:
                dev.reset()
            except Exception as e3:
                print("e3 : " + str(e3))
            
            is_WS_connect = False
            print("Reconnect WS FWS20N : " + str(e2));
            sql = "UPDATE aqm_sensor_values SET WS = ';0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()

        time.sleep(30)
	

except Exception as e:
    print(e)
