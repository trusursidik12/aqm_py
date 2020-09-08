from __future__ import print_function
from pyvantagepro import VantagePro2
from mysql.connector.constants import ClientFlag
import mysql.connector
import sys
import time

is_WS_connect = False

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] DAVIS Database CONNECTED")
except Exception as e: 
    print("[X]  DAVIS " + e)
    
def connect_ws():
    global is_WS_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_ws'")
        rec = mycursor.fetchone()
        for row in rec: serial_port = rec[0]
        
        try:
            COM_WS = VantagePro2.from_url("serial:%s:19200:8N1" % (serial_port))
            ws_data = COM_WS.get_current_data()
            WS = ws_data.to_csv(';',False)
            is_WS_connect = True
            return COM_WS 
        except:
            is_WS_connect = False
            return None
            
    except Exception as e: 
        return None
    
try:
    while True :
        try:
            if(not is_WS_connect):
                COM_WS = connect_ws()
        
            ws_data = COM_WS.get_current_data()
            WS = ws_data.to_csv(';',False)
            
            sql = "UPDATE aqm_sensor_values SET WS = '" + WS + "' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()            
            #print(WS)
        except Exception as e2: 
            is_WS_connect = False
            print("Reconnect WS Davis");
            sql = "UPDATE aqm_sensor_values SET WS = ';0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)