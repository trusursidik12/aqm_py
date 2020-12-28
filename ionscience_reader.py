from __future__ import print_function
from pymodbus.client.sync import ModbusSerialClient
import sys
import minimalmodbus
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

is_IONSCIENCE_connect = False

try:
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="trusur_aqm")
    mycursor = mydb.cursor()

    print("[V] IONSCIENCE Database CONNECTED")
except Exception as e:
    print("  [X] IONSCIENCE " + e)


def connect_ionscience(ionsciencemode):
    global is_IONSCIENCE_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_ion_science'")
        rec = mycursor.fetchone()
        for row in rec:
            serial_port = str(rec[0]).split(";")[ionsciencemode]

        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_ion_science'")
        rec = mycursor.fetchone()
        for row in rec:
            serial_rate = str(rec[0]).split(";")[ionsciencemode]
            
        print(serial_port)
        print(serial_rate)
        ion=minimalmodbus.Instrument(serial_port,1)
        ion.serial.baudrate=serial_rate
        ion.serial.parity=serial.PARITY_NONE
        ion.serial.bytesize=8
        ion.serial.stopbits=1
        ion.mode=minimalmodbus.MODE_RTU
        ion.serial.timeout=0.05
        ion.write_register(0x1248,1)
        
        response=ion.read_registers(0x1260,12,4)
        return response
        # response=ion.read_registers(0x12c0,12,4)
        # return response
        
    except Exception as e:
        print(e)
        return None


try:
    while True:
        try:
            ionscience = connect_ionscience(int(sys.argv[1]))
            print(ionscience)
        except Exception as e2:
            print(e2)
            print("Reconnect PM");
            sql = "UPDATE aqm_sensor_values SET AIN" + sys.argv[1] + " = '0' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()

        time.sleep(1)

except Exception as e:
    print(e)