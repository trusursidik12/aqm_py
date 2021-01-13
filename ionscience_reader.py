from __future__ import print_function
from pymodbus.client.sync import ModbusSerialClient
import sys
import minimalmodbus
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time
import struct

is_IONSCIENCE_connect = False
data_i = 0
counter = 0
total = 0.0

try:
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="trusur_aqm")
    mycursor = mydb.cursor()

    print("[V] IONSCIENCE " + sys.argv[1] + " Database CONNECTED")
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
            try:
                serial_rate = str(rec[0]).split(";")[ionsciencemode]
            except Exception as e2:
                serial_rate = str(rec[0]).split(";")[0]
            
        if(serial_rate == ""):
            serial_rate = str(rec[0]).split(";")[0]
            
        ion=minimalmodbus.Instrument(serial_port,1)
        ion.serial.baudrate=serial_rate
        ion.serial.parity=serial.PARITY_NONE
        ion.serial.bytesize=8
        ion.serial.stopbits=1
        ion.mode=minimalmodbus.MODE_RTU
        ion.serial.timeout=0.1
        ion.write_register(0x1248,1)
        print(ion.read_registers(0x12c0,8,4))
        
        try:
            h=ion.read_register(0x12c8,0,4,False)
            i=ion.read_register(0x12ca,0,4,False)
            
            c=hex(h).split('x')[1]
            d=hex(i).split('x')[1]
            r=d+c
            response = struct.unpack('!f',bytes.fromhex(r))[0];
            return response
        except Exception as ex2:
            ion.write_register(0x1248,0)
            time.sleep(2)
            return 0
        
    except Exception as e:
        print(e)
        return None


try:
    while True:
        try:
            IONSCIENCE = connect_ionscience(int(sys.argv[1]))
            if(str(IONSCIENCE).count("None") == 1):            
                sql = "UPDATE aqm_sensor_values SET AIN" + sys.argv[1] + " = '0' WHERE id = 1"
                mycursor.execute(sql)
                mydb.commit()
                
            else:
                if(float(IONSCIENCE) > 0):
                    total = total + float(IONSCIENCE)
                    data_i = data_i + 1
                    
            if(counter >= 60):
                ain_val = total / data_i
                total = 0.0
                data_i = 0
                counter = 0
                sql = "UPDATE aqm_sensor_values SET AIN" + sys.argv[1] + " = '" + str(ain_val) + "' WHERE id = 1"
                mycursor.execute(sql)
                mydb.commit()
            
            
            print(ain_val)
        except Exception as e2:
            print(e2)
            print("Reconnect IONSCIENCE");
            sql = "UPDATE aqm_sensor_values SET AIN" + sys.argv[1] + " = '0' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        counter = counter + 1

        time.sleep(1)

except Exception as e:
    print(e)