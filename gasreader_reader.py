import sys
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

is_gasreader_connect = False

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] Gas Reader Database CONNECTED")
except Exception as e: 
    print("[X]  [V] Gas Reader " + e)
    
    
def connect_gasreader():
    global is_gasreader_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_gasreader'")
        rec = mycursor.fetchone()
        for row in rec: serial_port = rec[0]
        
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_gasreader'")
        rec = mycursor.fetchone()
        for row in rec: serial_rate = rec[0]
        
        COM_GASREADER = serial.Serial(serial_port, serial_rate)
        time.sleep(3)
        GASREADER = str(COM_GASREADER.readline())
        if(GASREADER.count(";") == 8):
            is_gasreader_connect = True
            return COM_GASREADER 
        else:
            is_gasreader_connect = False
            return None
            
    except Exception as e: 
        return None


try:
    while True :
        try:
            if(not is_gasreader_connect):
                COM_GASREADER = connect_gasreader()
        
            GASREADER = str(COM_GASREADER.readline().decode("utf-8"))
            if(GASREADER.count(";") != 8):
                GASREADER = "0;0;0;0;0;0;0;0;\\r\\n'"
                
            AIN = GASREADER.split(";")
                
            sql = "UPDATE aqm_sensor_values SET AIN0 = %s, AIN1 = %s, AIN2 = %s, AIN3 = %s, AIN4 = %s, AIN5 = %s, AIN6 = %s, AIN7 = %s WHERE id = 1"
            val = (AIN[0],AIN[1],AIN[2],AIN[3],AIN[4],AIN[5],AIN[6],AIN[7])
            mycursor.execute(sql, val)
            mydb.commit()
            
            print(GASREADER)
        except Exception as e2:
            print(e2)
            is_gasreader_connect = False
            print("Reconnect GASREADER");
            sql = "UPDATE aqm_sensor_values SET AIN0 = '0', AIN1 = '0', AIN2 = '0', AIN3 = '0', AIN4 = '0', AIN5 = '0', AIN6 = '0', AIN7 = '0' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)