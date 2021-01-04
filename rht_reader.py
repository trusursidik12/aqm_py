from __future__ import print_function
import sys
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time
from datetime import datetime

is_RHT_connect = False

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] RHT Database CONNECTED")
except Exception as e: 
    print("[X]  [V] RHT " + e)
    
def connect_rht():
    global is_RHT_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_rht'")
        rec = mycursor.fetchone()
        for row in rec: serial_port = rec[0]
        
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_rht'")
        rec = mycursor.fetchone()
        for row in rec: serial_rate = rec[0]
        
        COM_RHT = serial.Serial(serial_port, serial_rate)
        RHT = str(COM_RHT.readline())
        if(RHT.count("ready") == 1):
            is_RHT_connect = True
            COM_RHT.write(b'start');
            time.sleep(1)
            return COM_RHT
        else:
            return None
    except Exception as e: 
        return None
        
def logwrite(data):
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'sta_id'")
    rec = mycursor.fetchone()
    for row in rec: id_stasiun = rec[0]
    waktu = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    filename = "RHT_" + id_stasiun + "_" + datetime.today().strftime('%Y%m%d%H0000') + ".log"
    f = open("../"+filename, 'a+')
    f.write(waktu + " => " + data + "\n")
    f.close()
    
try:
    while True :
        try:
            if(not is_RHT_connect):
                COM_RHT = connect_rht()
        
            RHT = str(COM_RHT.readline())
            
            logwrite(str(RHT))
            print(RHT)
        except Exception as e2: 
            is_RHT_connect = False
            print(e2);
        
        time.sleep(1)
        
except Exception as e: 
    print(e)