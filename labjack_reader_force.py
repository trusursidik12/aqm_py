from __future__ import print_function
from labjack import ljm
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

AIN0 = 0
AIN1 = 0
AIN2 = 0
AIN3 = 0
AIN4 = 0
AIN5 = 0
AIN6 = 0
AIN7 = 0

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] Labjack Force Database CONNECTED")
except Exception as e: 
    print("[X]  Labjack Force " + e)

while True:
    try:
        labjack = ljm.openS("ANY", "ANY", "ANY")
        AIN0 = ljm.eReadName(labjack, "AIN0")
        AIN1 = ljm.eReadName(labjack, "AIN1")
        AIN2 = ljm.eReadName(labjack, "AIN2")
        AIN3 = ljm.eReadName(labjack, "AIN3")
        AIN4 = ljm.eReadName(labjack, "AIN4")
        AIN5 = ljm.eReadName(labjack, "AIN5")
        AIN6 = ljm.eReadName(labjack, "AIN6")
        AIN7 = ljm.eReadName(labjack, "AIN7")
        
    except Exception as e: 
        AIN0 = 0
        AIN1 = 0
        AIN2 = 0
        AIN3 = 0
        AIN4 = 0
        AIN5 = 0
        AIN6 = 0
        AIN7 = 0
        
    ljmvalue = AIN0 + ";" + AIN1 + ";" + AIN2 + ";" + AIN3 + ";" + AIN4 + ";" + AIN5 + ";" + AIN6 + ";" + AIN7;
        
    sql = "UPDATE aqm_sensor_values SET LABJACK = %s WHERE id = 1"
    val = (ljmvalue)
    mycursor.execute(sql, val)
    mydb.commit()
    #print("%s" % (ljmvalue));
    
    time.sleep(1) 