from __future__ import print_function
import sys
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

is_HORIBA_connect = False

stx = b'\x02'
etx = b'\x03'

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] HORIBA  Database CONNECTED")
except Exception as e: 
    print("[X]  [V] HORIBA  " + e)
    
def connect_horiba():
    global is_HORIBA_connect
    try:
        # mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_horiba'")
        # rec = mycursor.fetchone()
        # for row in rec: serial_port = rec[0]
        
        # mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_horiba'")
        # rec = mycursor.fetchone()
        # for row in rec: serial_rate = rec[0]
        
        horiba = serial.Serial('/dev/ttyUSB2',38400,timeout=3.0)
        horiba.write(stx + b'DA' + etx + b'04')
        if (horiba):
            is_HORIBA_connect = True
            return str(horiba.readline())
        else:
            is_HORIBA_connect = False
            return None
                
    except Exception as e: 
        return None
    
try:
    while True :
        try:
            
            HORIBA = connect_horiba(sys.argv[1])
            if(HORIBA == None):
                HORIBA = ""
                
            sql = "UPDATE aqm_sensor_values SET LABJACK = '" + HORIBA.replace("'","''") + "' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
            
            print(HORIBA)
        except Exception as e2:
            print(e2)
            is_HORIBA_connect = False
            print("Reconnect HORIBA" + sys.argv[1]);
            sql = "UPDATE aqm_sensor_values SET " + sensor_field_name + " = '' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)