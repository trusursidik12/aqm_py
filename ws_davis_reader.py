from __future__ import print_function
from pyvantagepro import VantagePro2
from mysql.connector.constants import ClientFlag
import mysql.connector
import sys
import time

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] DAVIS Database CONNECTED")
except Exception as e: 
    print("[X]  DAVIS " + e)
    
try:
    while True :
        try:
            COM_WS = VantagePro2.from_url("serial:%s:19200:8N1" % (sys.argv[1]))
            ws_data = COM_WS.get_current_data()
            WS = ws_data.to_csv(';',False)
        except:
            WS = ";0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0";
            
        sql = "UPDATE aqm_sensor_values SET WS = '" + WS + "' WHERE id = 1"
        mycursor.execute(sql)
        mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)