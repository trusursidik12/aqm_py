from __future__ import print_function
from mysql.connector.constants import ClientFlag
import sys
import time
import mysql.connector
import serial
import requests
import json


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
    
    if serial_port != "":
        Arduino = serial.Serial(serial_port, serial_rate)
        is_Arduino = True
        print("[V] ARDUINO CONNECTED")
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'sta_id'")
        rec = mycursor.fetchone()
        for row in rec: id_stasiun = rec[0]
        
        
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
  
while True:
    try:
        url = "http://localhost/ispumapapi/api/aqmoutdoor?trusur_api_key=VHJ1c3VyVW5nZ3VsVGVrbnVzYV9wVA==&id_stasiun=" + id_stasiun
        print(url)
        response = json.loads(requests.get(url).text)
        mycursor.execute("TRUNCATE TABLE aqm_data")
        mydb.commit()        
        query = "INSERT INTO aqm_data (id_stasiun,waktu,pm10,so2,co,o3,no2,ws,wd,humidity,temperature,pressure,sr,rain_intensity) VALUES ('"+response["id_stasiun"]+"','"+response["datetime"]+"','"+str(response["pm10"])+"','"+str(response["so2"])+"','"+str(response["co"])+"','"+str(response["o3"])+"','"+str(response["no2"])+"','"+str(response["wind_speed"])+"','"+str(response["wind_direction"])+"','"+str(response["humidity"])+"','"+str(response["temperature"])+"','"+str(response["pressure"])+"','"+str(response["solar_radiation"])+"','"+str(response["rain_rate"])+"')"
        mycursor.execute(query)
        mydb.commit()
        
        if is_Arduino:
            try:
                mycursor.execute("SELECT id_stasiun,waktu,pm10,so2,co,o3,no2,ws,wd,humidity,temperature,pressure,sr,rain_intensity FROM aqm_data ORDER BY id DESC LIMIT 1")
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
                print(text1_command)
                time.sleep(3)
                Arduino.write(text1_command.encode());
                
                # TEXT2
                text2_command = "2"+str(rec[2])+";"+str(rec[3])+";"+str(rec[4])+";"+str(rec[5])+";"+str(rec[6])+"] "
                print(text2_command)
                time.sleep(5)
                Arduino.write(text2_command.encode());
                
                # TEXT3
                    # 31BATAM;31 Mar 2020 14:20;11;82;235;0;0]
                    # 3233.78;1010.8;8.05;338]  SUHU:{suhu}C TEK:{tek}mBar WS: {ws}m/s WD:{wd}
                    
                if response["id_stasiun"] == "":
                    stasiun_name = rec[0]
                else:
                    stasiun_name = response["id_stasiun"]
                
                if response["datetime"] == "":
                    waktu = rec[1]
                else:
                    waktu = response["datetime"]                
                
                text3_command = "31"+stasiun_name+";"+waktu+";"+str(rec[2])+";"+str(rec[3])+";"+str(rec[4])+";"+str(rec[5])+";"+str(rec[6])+"] "
                print(text3_command)
                time.sleep(10)
                Arduino.write(text3_command.encode());
                
                text3_command = "32"+str(rec[10])+";"+str(rec[11])+";"+str(rec[7])+";"+str(rec[8])+"] "
                print(text3_command)
                time.sleep(30)
                Arduino.write(text3_command.encode());
            except Exception as e: 
                print(e)
        
        
        print("====================");
        
    except Exception as e: 
        print(e)
    
    time.sleep(600) #every 10 minutes 
    