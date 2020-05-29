from __future__ import print_function
from labjack import ljm
from mysql.connector.constants import ClientFlag
from pyvantagepro import VantagePro2
import sys
import time
import mysql.connector
import serial
import subprocess
import glob


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

AIN0 = 0
AIN1 = 0
AIN2 = 0
AIN3 = 0
PM10 = ""
PM25 = ""
WS = ""
cur_pump_state = "0"
is_labjack = False
is_COM_PM10 = False
is_COM_PM25 = False
is_COM_WS = False
is_COM_AIRMAR = False
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
    
try:
    labjack = ljm.openS("ANY", "ANY", "ANY")
    is_labjack = True
    print("[V] Labjack CONNECTED")
except:
    print("    [X] Labjack not connected")
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm10'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_pm10'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    if serial_port != "":
        COM_PM10 = serial.Serial(serial_port, serial_rate)
        is_COM_PM10 = True
        print("[V] COM_PM10 CONNECTED")
    else:
        print("    [X] COM_PM10 not connected")
        
except:
    print("    [X] COM_PM10 not connected")
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm25'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_pm25'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    if serial_port != "":
        COM_PM25 = serial.Serial(serial_port, serial_rate)
        is_COM_PM25 = True
        print("[V] COM_PM25 CONNECTED")
    else:
        print("    [X] COM_PM25 not connected")
        
except:
    print("    [X] COM_PM25 not connected")
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_ws'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_ws'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    if serial_port != "":
        COM_WS = VantagePro2.from_url("serial:%s:%s:8N1" % (serial_port,serial_rate))
        is_COM_WS = True
        print("[V] COM_WS CONNECTED")
    else:
        print("    [X] COM_WS not connected")
    
except:
    print("    [X] COM_WS not connected")
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_airmar'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_airmar'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    if serial_port != "":
        COM_AIRMAR = serial.Serial(serial_port, serial_rate)
        is_COM_AIRMAR = True
        print("[V] COM_AIRMAR CONNECTED")
    else:
        print("    [X] COM_AIRMAR not connected")
        
except:
    print("    [X] COM_AIRMAR not connected")
    
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
        mycursor.execute("UPDATE aqm_configuration SET content = 0 WHERE data = 'pump_state'")
        mydb.commit()
        mycursor.execute("UPDATE aqm_configuration SET content = NOW() WHERE data = 'pump_last'")
        mydb.commit()
    else:  
        print("    [X] ARDUINO not connected")
        
except:
    print("    [X] ARDUINO not connected")

AIN0_less = 9999999999999
AIN1_less = 9999999999999
AIN2_less = 9999999999999
AIN3_less = 9999999999999
    
while True:
    try:
        if is_labjack:
            try:
                AIN0 = ljm.eReadName(labjack, "AIN0")
                AIN1 = ljm.eReadName(labjack, "AIN1")
                AIN2 = ljm.eReadName(labjack, "AIN2")
                AIN3 = ljm.eReadName(labjack, "AIN3")
                if AIN0_less > AIN0: AIN0_less = AIN0;
                if AIN1_less > AIN1: AIN1_less = AIN1;
                if AIN2_less > AIN2: AIN2_less = AIN2;
                if AIN3_less > AIN3: AIN3_less = AIN3;
                AIN0_range = 0.04 - AIN0_less;
                AIN1_range = 0.04 - AIN1_less
                AIN2_range = 0.04 - AIN2_less
                AIN3_range = 0.04 - AIN3_less
                
            except Exception as e: 
                print(e)
                AIN0 = 0
                AIN1 = 0
                AIN2 = 0
                AIN3 = 0
                AIN3 = ljm.eReadName(labjack, "AIN3")
                AIN0_less = 0
                AIN1_less = 0
                AIN2_less = 0
                AIN3_less = 0
                AIN0_range = 0
                AIN1_range = 0
                AIN2_range = 0
                AIN3_range = 0
        
        if is_COM_PM10:
            try:
                PM10 = str(COM_PM10.readline());
            except Exception as e: 
                print(e)
                PM10 = ""
            
        if is_COM_PM25:
            try:
                PM25 = str(COM_PM25.readline());
            except Exception as e: 
                print(e)
                PM25 = ""
            
        if is_COM_WS:
            try:
                ws_data = COM_WS.get_current_data()
                WS = ws_data.to_csv(';',False)
            except Exception as e: 
                print(e)
                WS = ""
                
        if is_COM_AIRMAR:
            try:
                i = 0
                ws_data = ""
                while i <= 12:
                    ws_data = ws_data + str(COM_AIRMAR.readline());
                    i += 1
                
                WIMDA = ws_data.split("$WIMDA,")[1];
                WIMDA = WIMDA.split("\\r\\n")[0];
                
                WIMWV = ws_data.split("$WIMWV,")[1];
                WIMWV = WIMWV.split("\\r\\n")[0];
                
                barometer = WIMDA.split(",")[0];
                if barometer == "": barometer = "0.0";
                
                temp = WIMDA.split(",")[4];
                if temp == "": temp = "0.0";
                temp = str((9/5 * float(temp)) + 32);
                
                humidity = WIMDA.split(",")[8];
                if humidity == "": humidity = "0.0";
                
                windspeed = WIMWV.split(",")[2];
                if windspeed == "": windspeed = "0.0";
                
                winddir = WIMWV.split(",")[0];
                if winddir == "": winddir = "0.0";
                
                rainrate = "0.0";
                solarrad = "0.0";
                
                WS = ";0;" + barometer + ";" + temp + ";" + humidity + ";" + temp + ";" + windspeed + ";" + windspeed + ";" + winddir + ";" + humidity + ";" + rainrate + ";0;" + solarrad + ";0.0;0;" + rainrate + ";";
                
            except Exception as e: 
                print(e)
                WS = ""
            
        if is_Arduino:
            try:
                mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'pump_state'")
                rec = mycursor.fetchone()
                for row in rec: pump_state = rec[0]
                if pump_state != cur_pump_state:
                    cur_pump_state = pump_state
                    if cur_pump_state == "1":
                        Arduino.write(b'i');
                    else:
                        Arduino.write(b'j');
            except Exception as e: 
                print(e)
        
        sql = "UPDATE aqm_sensor_values SET AIN0 = %s, AIN1 = %s, AIN2 = %s, AIN3 = %s, PM25 = %s, PM10 = %s, WS = %s WHERE id = 1"
        val = (AIN0,AIN1,AIN2,AIN3,PM25,PM10,WS)
        mycursor.execute(sql, val)
        mydb.commit()
        
        print("AIN0 = %f ; AIN1 = %f ; AIN2 = %f ; AIN3 = %f ; PM10 = %s;  PM25 = %s ; WS = %s ; cur_pump_state = %s" % (AIN0,AIN1,AIN2,AIN3,PM10,PM25,WS,cur_pump_state))
        print("MIN ==> AIN0 = %f ; AIN1 = %f ; AIN2 = %f ; AIN3 = %f " % (AIN0_less,AIN1_less,AIN2_less,AIN3_less))
        print("RANGE ==> AIN0 = %f ; AIN1 = %f ; AIN2 = %f ; AIN3 = %f " % (AIN0_range,AIN1_range,AIN2_range,AIN3_range))
        print("=========================================================================================================================");
        
    except Exception as e: 
        print(e)

    time.sleep(1) 