from __future__ import print_function
from mysql.connector.constants import ClientFlag
import sys
import time
import datetime
import mysql.connector
import serial
import requests
import json
import glob
import subprocess


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

is_Arduino = False

def bulan(mm):
    if(mm == "01"): return "Jan"
    if(mm == "02"): return "Feb"
    if(mm == "03"): return "Mar"
    if(mm == "04"): return "Apr"
    if(mm == "05"): return "Mei"
    if(mm == "06"): return "Jun"
    if(mm == "07"): return "Jul"
    if(mm == "08"): return "Agt"
    if(mm == "09"): return "Sep"
    if(mm == "10"): return "Okt"
    if(mm == "11"): return "Nov"
    if(mm == "12"): return "Des"

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
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'controller'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'controller_baud'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'sta_id'")
    rec = mycursor.fetchone()
    for row in rec: id_stasiun = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'sta_nama'")
    rec = mycursor.fetchone()
    for row in rec: stasiun_name = rec[0]
    
    if serial_port != "":
        Arduino = serial.Serial(serial_port, serial_rate)
        is_Arduino = True
        print("[V] ARDUINO CONNECTED") 
    else:  
        print("    [X] ARDUINO not connected")
        
except:
    print("    [X] ARDUINO not connected")

mycursor.execute("TRUNCATE TABLE serial_ports")
mydb.commit()
for port in serial_ports():
    print("Adding port " + port)
    p = subprocess.Popen('dmesg | grep ' + str(port).replace('/dev/','') + ' | tail -1', stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    port_desc = output.decode("utf-8")
    if "now attached" in port_desc:
        try:
            port_desc = port_desc.split(":")[1].split(" now attached")[0]
        except:
            port_desc = port_desc
    print(port_desc)
    mycursor.execute("INSERT INTO serial_ports (port,description) VALUES ('" + port +"','" + port_desc +"')")
    mydb.commit()
    
lastexec = ""
firsttime = True;
  
while True:
    try:
        now = datetime.datetime.now()
        nowM = str(now.strftime("%M"))
        if(int(now.strftime("%S"))%15 == 0): print (now.strftime("%Y-%m-%d %H:%M:%S"))
        
        if (firsttime or nowM == "01" or nowM == "31") and now.strftime("%Y-%m-%d %H:%M") != lastexec :
            firsttime = False
            print (now.strftime("%Y-%m-%d %H:%M:%S"))
            
            url = "http://ispumaps.id/ispumapapi/api/aqmoutdoor?trusur_api_key=VHJ1c3VyVW5nZ3VsVGVrbnVzYV9wVA==&id_stasiun=" + id_stasiun
            print(url)
            response = json.loads(requests.get(url).text)
            if(response["id_stasiun"] != ""):
                mycursor.execute("TRUNCATE TABLE aqm_data")
                mydb.commit()        
                query = "INSERT INTO aqm_data (id_stasiun,waktu,pm10,so2,co,o3,no2,ws,wd,humidity,temperature,pressure,sr,rain_intensity) VALUES ('"+response["id_stasiun"]+"','"+response["waktu"]+"','"+str(response["pm10_val"])+"','"+str(response["so2_val"])+"','"+str(response["co_val"])+"','"+str(response["o3_val"])+"','"+str(response["no2_val"])+"','"+str(response["wind_speed"])+"','"+str(response["wind_direction"])+"','"+str(response["humidity"])+"','"+str(response["temperature"])+"','"+str(response["pressure"])+"','"+str(response["solar_radiation"])+"','"+str(response["rain_rate"])+"')"
                mycursor.execute(query)
                mydb.commit()
                print(query)
                mycursor.execute("TRUNCATE TABLE aqm_ispu")
                mydb.commit()        
                query = "INSERT INTO aqm_ispu (id_stasiun,waktu,pm10,so2,co,o3,no2) VALUES ('"+response["id_stasiun"]+"','"+response["waktu"]+"','"+str(response["pm10"])+"','"+str(response["so2"])+"','"+str(response["co"])+"','"+str(response["o3"])+"','"+str(response["no2"])+"')"
                mycursor.execute(query)
                mydb.commit()
                print(query)
                
                if is_Arduino:
                    try:
                        mycursor.execute("SELECT id_stasiun,waktu,pm10,so2,co,o3,no2 FROM aqm_ispu ORDER BY id DESC LIMIT 1")
                        rec = mycursor.fetchone()
                        # TEXT1
                        text1_command = "1"
                        for x in [2, 3, 4, 5, 6]:
                            if rec[x] <= 50: text1_command += "0";
                            elif rec[x] <= 100: text1_command +=  "1";
                            elif rec[x] <= 199: text1_command +=  "2";
                            elif rec[x] <= 299: text1_command +=  "3";
                            else: text1_command +=  "4";
                        
                        text1_command += " "
                        print("text1_command : " + text1_command)
                        time.sleep(3)
                        Arduino.write(text1_command.encode());
                        
                        # TEXT2
                        bar_pm10 = int(round(rec[2]))
                        bar_so2 = int(round(rec[3]))
                        bar_co = int(round(rec[4]))
                        bar_o3 = int(round(rec[5]))
                        bar_no2 = int(round(rec[6]))
                        if bar_pm10 > 500 : bar_pm10 = 500
                        if bar_so2 > 500 : bar_so2 = 500
                        if bar_co > 500 : bar_co = 500
                        if bar_o3 > 500 : bar_o3 = 500
                        if bar_no2 > 500 : bar_no2 = 500
                        text2_command = "2"+str()+";"+str(bar_so2)+";"+str(bar_co)+";"+str(bar_o3)+";"+str(bar_no2)+"] "
                        print("text2_command : " + text2_command)
                        time.sleep(5)
                        Arduino.write(text2_command.encode());
                        
                        mycursor.execute("SELECT id_stasiun,waktu,pm10,so2,co,o3,no2,ws,wd,humidity,temperature,pressure,sr,rain_intensity FROM aqm_data ORDER BY id DESC LIMIT 1")
                        rec = mycursor.fetchone()
                        # TEXT3
                            # 3SIMPANG TIGA;31 Mar 2020 14:20;11;82;235;0;0;3233.78;1010.8;8.05;338]
                            
                        
                        if response["waktu"] == "":
                            waktu = rec[1]
                        else:
                            waktu = response["waktu"]
                            
                        d = datetime.datetime.strptime(waktu, '%Y-%m-%d %H:%M:%S')
                        mm = str(datetime.date.strftime(d, "%m"))
                        
                        tanggaljam = datetime.date.strftime(d, "%d " + bulan(mm) + " %Y %H:%M")
                        
                        text3_command = "3"+stasiun_name+";"+tanggaljam+";"+str(int(round(rec[2])))+";"+str(int(round(rec[3])))+";"+str(int(round(rec[4])))+";"+str(int(round(rec[5])))+";"+str(int(round(rec[6])))+";"+str(rec[10])+";"+str(rec[11])+";"+str(rec[7])+";"+str(rec[8])+"] "
                        print("text3_command : " + text3_command)
                        time.sleep(10)
                        Arduino.write(text3_command.encode());
                    except Exception as e: 
                        print(e)
                
                lastexec = now.strftime("%Y-%m-%d %H:%M")
                print("====================================================================================================");
        
        
    except Exception as e: 
        print(e)
    
    time.sleep(1)
    