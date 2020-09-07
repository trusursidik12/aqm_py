from __future__ import print_function
import sys
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

db = open("db.txt", "r").read().split("|")

is_HC_connect = False

try:
    mydb = mysql.connector.connect(host=db[0],user=db[1],passwd=db[2],database=db[3])
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM aqm_sensor_values WHERE id=1")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_sensor_values (id) VALUES (1)")
        mydb.commit()
    
    print("[V] HC Database CONNECTED")
except Exception as e: 
    print("[X]  [V] HC " + e)
    
def connect_hc():
    global is_HC_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_hc'")
        rec = mycursor.fetchone()
        for row in rec: serial_port = rec[0]
        
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_hc'")
        rec = mycursor.fetchone()
        for row in rec: serial_rate = rec[0]
        
        COM_HC = serial.Serial(serial_port, serial_rate)
        HC = str(COM_HC.readline())
        if(HC.count(",") == 0 and HC.count("\\r\\n") == 1 and HC.count("b'") == 1):
            is_HC_connect = True
            return COM_HC 
        else:
            is_HC_connect = False
            return None
            
    except Exception as e: 
        return None
    
try:
    while True :
        try:
            if(not is_HC_connect):
                COM_HC = connect_hc()
        
            HC = str(COM_HC.readline())
            if(HC.count(",") == 0 and HC.count("\\r\\n") == 1 and HC.count("b'") == 1):
                HC = HC.split("\\r\\n")[0];
                HC = HC.split("b'")[1];
            else:
                HC = "0"
                
            sql = "UPDATE aqm_sensor_values SET HC = '" + HC + "' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
            
            #print(HC)
        except Exception as e2: 
            is_HC_connect = False
            print("Reconnect HC");
            sql = "UPDATE aqm_sensor_values SET HC = '0' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)