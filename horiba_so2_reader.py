from __future__ import print_function
import sys
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

is_EBAM_connect = False

sensor_field_name = ""


stx = b'\x02'
etx = b'\x03'

s = stx + b'DA' + etx + b'04'

ebam = serial.Serial('/dev/ttyUSB2',38400,timeout=3.0)
ebam.write(s)
print(str(ebam.readline()))


# with serial.Serial('COM17',38400,timeout=3.0) as ebam:
    # s = '\0x02' + 'DA' + '\0x03' + '04' + '\n'
    # ebam.write(b'\0x02DA\0x0304\n')
    # time.sleep(0.5)
    # res=ebam.read(2000)
    # str(res)
    
    
    
print("AAA")
    
exit()


try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] EBAM " + sys.argv[1] + " Database CONNECTED")
except Exception as e: 
    print("[X]  [V] EBAM " + sys.argv[1] + " " + e)
    
def connect_ebam(ebammode):
    global is_EBAM_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_"+ ebammode +"'")
        rec = mycursor.fetchone()
        for row in rec: serial_port = rec[0]
        
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_"+ ebammode +"'")
        rec = mycursor.fetchone()
        for row in rec: serial_rate = rec[0]
        
        
        with serial.Serial(serial_port, timeout=3.0) as ebam:
            ebam.write(b'\r\r\r')
            time.sleep(0.5)
            ebam.write(b'4')
            res=ebam.read(2000)
            if (res):
                is_EBAM_connect = True
                return str(res).split("Status")[1].split("\\r\\n")[1]
            else:
                is_EBAM_connect = False
                return None
                
    except Exception as e: 
        return None
    
try:
    if(sys.argv[1] == "ebam25"):
        sensor_field_name = "PM25"
    if(sys.argv[1] == "ebam10"):
        sensor_field_name = "PM10"
    if(sys.argv[1] == "ebamtsp"):
        sensor_field_name = "TSP"
        
    while True :
        try:
            
            EBAM = connect_ebam(sys.argv[1])
            if(EBAM == None):
                EBAM = ""
                
            sql = "UPDATE aqm_sensor_values SET " + sensor_field_name + " = '" + EBAM.replace("'","''") + "' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
            
            #print(EBAM)
        except Exception as e2:
            print(e2)
            is_EBAM_connect = False
            print("Reconnect EBAM" + sys.argv[1]);
            sql = "UPDATE aqm_sensor_values SET " + sensor_field_name + " = '' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)