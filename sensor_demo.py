from __future__ import print_function
from datetime import datetime
import sys
import random
import time
import mysql.connector

from mysql.connector.constants import ClientFlag

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM aqm_sensor_values WHERE id=1")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_sensor_values (id) VALUES (1)")
        mydb.commit()
    print("[V] Database CONNECTED")
except Exception as e: 
    print(e)
    
while True:
    AIN0 = random.uniform(3, 5)/100
    AIN1 = random.uniform(3, 5)/100
    AIN2 = random.uniform(3, 5)/100
    AIN3 = random.uniform(3, 5)/100
    PM25 = "b'000.0" + str(random.randrange(10, 60)) + "," + str(random.randrange(10, 30)/10) + ",+28.3,067,1007.4,00,*01543\r\n'"
    PM10 = "b'000.0" + str(random.randrange(10, 60)) + "," + str(random.randrange(10, 30)/10) + ",+28.3,067,1007.4,00,*01543\r\n'"
    WS = str(datetime.now()) + ";255;" + str(random.randrange(99999, 999999)/1000) + ";" + str(random.randrange(10, 999)/10) + ";" + str(random.randrange(10, 100)) + ";" + str(random.randrange(10, 999)/10) + ";" + str(random.randrange(10, 99)) + ";0;" + str(random.randrange(100, 600)) + ";" + str(random.randrange(10, 100)) + ";" + str(random.randrange(10, 99)/10) + ";0;" + str(random.randrange(10, 100)) + ";0.0;2127-15-31;" + str(random.randrange(10, 99)/10) + ";0.0;0.0;0.001;0.0;0.0;0;4.8515625;0;193;07:23;17:02;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0"
    sql = "UPDATE aqm_sensor_values SET AIN0 = %s, AIN1 = %s, AIN2 = %s, AIN3 = %s, PM25 = %s, PM10 = %s, WS = %s WHERE id = 1"
    val = (AIN0,AIN1,AIN2,AIN3,PM25,PM10,WS)
    mycursor.execute(sql, val)
    mydb.commit()
    time.sleep(1) 