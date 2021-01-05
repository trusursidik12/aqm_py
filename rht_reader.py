from __future__ import print_function
import os
import glob
import requests
import sys
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth

is_RHT_connect = False
uploaded_at = ""

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
    
def upload_log():
    global uploaded_at
    url = 'http://103.247.11.149/server_side/api/put_rht_log.php'
    apikey = "VHJ1c3VyVW5nZ3VsVGVrbnVzYV9wVA=="
    uploaded_at = datetime.today().strftime('%Y-%m-%d %H:00:00')
    print("Uploading : " + str(uploaded_at))
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'sta_id'")
    rec = mycursor.fetchone()
    for row in rec: id_stasiun = rec[0]
    date_1_hour_ago = datetime.now() - timedelta(hours=1)
    filename = "RHT_" + id_stasiun + "_" + date_1_hour_ago.strftime('%Y%m%d%H0000') + ".log"
    print(filename)
    
    headers = headers = {'Content-type': 'text/plain', 'filename': filename, 'Api-Key': apikey}
    r = requests.put(url, data=open("../"+filename, 'rb'), headers=headers, auth=('superuser', 'R2h2s12R2h2s12'))
    print(r.content)
    return r.content
    
def delete_log():
    try:
        fileList = glob.glob("../RHT_*.log", recursive=False)
        for filePath in fileList:
            if (os.stat(filePath).st_mtime < time.time() - (2 * 86400)):
                os.remove(filePath)
        
        return True
    except Exception as e: 
        print(e)
        return False
    
try:
    while True :
        try:
            waktu = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            if(not is_RHT_connect):
                COM_RHT = connect_rht()
                time.sleep(1)
            else:
                RHT = str(COM_RHT.readline()).replace("b'","").replace("\\r\\n'","")
                logwrite(RHT)
                if(str(datetime.today().strftime('%M')) == "01" and uploaded_at != datetime.today().strftime('%Y-%m-%d %H:00:00')):
                   upload_log()
                   delete_log()
            
        except Exception as e2: 
            is_RHT_connect = False
            print(e2);
        
        time.sleep(1)
        
except Exception as e: 
    print(e)