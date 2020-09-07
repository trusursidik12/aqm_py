from __future__ import print_function
import sys
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

db = open("db.txt", "r").read().split("|")

is_PM_connect = False

try:
    mydb = mysql.connector.connect(host=db[0],user=db[1],passwd=db[2],database=db[3])
    mycursor = mydb.cursor()
    
    print("[V] PM" + sys.argv[1] + " Database CONNECTED")
except Exception as e: 
    print("[X]  [V] PM " + sys.argv[1] + " " + e)
    
def connect_pm(pmmode):
    global is_PM_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm"+ pmmode +"'")
        rec = mycursor.fetchone()
        for row in rec: serial_port = rec[0]
        
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_pm"+ pmmode +"'")
        rec = mycursor.fetchone()
        for row in rec: serial_rate = rec[0]
        
        COM_PM = serial.Serial(serial_port, serial_rate)
        PM = str(COM_PM.readline())
        if(PM.count(",") == 6):
            is_PM_connect = True
            return COM_PM 
        else:
            is_PM_connect = False
            return None
            
    except Exception as e: 
        return None
    
try:
    while True :
        try:
            if(not is_PM_connect):
                COM_PM = connect_pm(sys.argv[1])
        
            PM = str(COM_PM.readline())
            if(PM.count(",") != 6):
                PM = "b'000.000,0.0,+0.0,0,0,00,*0\\r\\n'"
                
            sql = "UPDATE aqm_sensor_values SET PM" + sys.argv[1] + " = '" + PM.replace("'","''") + "' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
            
            #print(PM)
        except Exception as e2: 
            is_PM_connect = False
            print("Reconnect PM" + sys.argv[1]);
            sql = "UPDATE aqm_sensor_values SET PM" + sys.argv[1] + " = '" + "b''000.000,0.0,+0.0,0,0,00,*0\\r\\n''" + "' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)