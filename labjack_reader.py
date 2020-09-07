from __future__ import print_function
from labjack import ljm
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

db = open("db.txt", "r").read().split("|")

AIN0 = 0
AIN1 = 0
AIN2 = 0
AIN3 = 0
AIN4 = 0
AIN5 = 0
AIN6 = 0
AIN7 = 0

try:
    mydb = mysql.connector.connect(host=db[0],user=db[1],passwd=db[2],database=db[3])
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM aqm_sensor_values WHERE id=1")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_sensor_values (id) VALUES (1)")
        mydb.commit()
    
    print("[V] Labjack Database CONNECTED")
except Exception as e: 
    print("[X]  Labjack " + e)

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
        
    sql = "UPDATE aqm_sensor_values SET AIN0 = %s, AIN1 = %s, AIN2 = %s, AIN3 = %s, AIN4 = %s, AIN5 = %s, AIN6 = %s, AIN7 = %s WHERE id = 1"
    val = (AIN0,AIN1,AIN2,AIN3,AIN4,AIN5,AIN6,AIN7)
    mycursor.execute(sql, val)
    mydb.commit()
    #print("%s;%s;%s;%s;%s;%s;%s;%s" % (AIN0,AIN1,AIN2,AIN3,AIN4,AIN5,AIN6,AIN7));
    
    time.sleep(1) 