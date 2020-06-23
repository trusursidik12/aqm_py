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
HC = "0"
PM10 = ""
PM25 = ""
WS = ""
pump_speed = 0;
cur_pump_state = "0"
is_labjack = False
is_COM_PM10 = False
is_COM_PM25 = False
is_COM_HC = False
is_COM_WS = False
is_COM_AIRMAR = False
is_Arduino = False
is_Pump_pwm = False
serial_port_WS = ""
serial_rate_WS = ""
serial_port_WS2 = ""


try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM aqm_sensor_values WHERE id=1")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_sensor_values (id) VALUES (1)")
        mydb.commit()
    mycursor.execute("SELECT id FROM aqm_configuration WHERE data='com_hc'")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_configuration (data,content) VALUES ('com_hc','COM5')")
        mydb.commit()
    mycursor.execute("SELECT id FROM aqm_configuration WHERE data='baud_hc'")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_configuration (data,content) VALUES ('baud_hc','9600')")
        mydb.commit()
        
    mycursor.execute("SELECT id FROM aqm_configuration WHERE data='com_pump_pwm'")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_configuration (data,content) VALUES ('com_pump_pwm','')")
        mydb.commit()
    mycursor.execute("SELECT id FROM aqm_configuration WHERE data='baud_pump_pwm'")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_configuration (data,content) VALUES ('baud_pump_pwm','9600')")
        mydb.commit()
    mycursor.execute("SELECT id FROM aqm_configuration WHERE data='pump_speed'")
    mycursor.fetchall()
    if mycursor.rowcount <= 0:    
        mycursor.execute("INSERT INTO aqm_configuration (data,content) VALUES ('pump_speed','80')")
        mydb.commit()
        
    try:
        mycursor.execute("ALTER TABLE `aqm_sensor_values` ADD COLUMN `HC` double AFTER `AIN3`")
        mydb.commit()
    except Exception as e2:
        print("")
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
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_hc'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_hc'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    if serial_port != "":
        COM_HC = serial.Serial(serial_port, serial_rate)
        is_COM_HC = True
        print("[V] COM_HC CONNECTED")
    else:
        print("    [X] COM_HC not connected")
        
except:
    print("    [X] COM_HC not connected")
    
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
    for row in rec: serial_port_WS = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_ws'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate_WS = rec[0]
    
    if serial_port_WS != "":
        if ";" in serial_port_WS:
            serial_port_WS2 = serial_port_WS.split(';')[1];
            serial_port_WS = serial_port_WS.split(';')[0];
            try:
                COM_WS = VantagePro2.from_url("serial:%s:%s:8N1" % (serial_port_WS,serial_rate_WS))
                is_COM_WS = True
                print("[V] COM_WS CONNECTED with " + serial_port_WS)
            except:                
                COM_WS = VantagePro2.from_url("serial:%s:%s:8N1" % (serial_port_WS2,serial_rate_WS))
                is_COM_WS = True
                print("[V] COM_WS CONNECTED with " + serial_port_WS2)
        else:
            COM_WS = VantagePro2.from_url("serial:%s:%s:8N1" % (serial_port_WS,serial_rate_WS))
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
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pump_pwm'")
    rec = mycursor.fetchone()
    for row in rec: serial_port = rec[0]
    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_pump_pwm'")
    rec = mycursor.fetchone()
    for row in rec: serial_rate = rec[0]
    
    if serial_port != "":
        Pump_pwm = serial.Serial(serial_port, serial_rate)
        is_Pump_pwm = True
        print("[V] PUMP PWM CONNECTED")
        
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'pump_speed'")
        rec = mycursor.fetchone()
        for row in rec: pump_speed = int(rec[0])
        Pump_pwm.write(pump_speed.encode());
        
        mycursor.execute("UPDATE aqm_configuration SET content = 0 WHERE data = 'pump_state'")
        mydb.commit()
        mycursor.execute("UPDATE aqm_configuration SET content = NOW() WHERE data = 'pump_last'")
        mydb.commit()
    else:  
        print("    [X] PUMP PWM not connected")
        
except:
    print("    [X] PUMP PWM not connected")
    
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
                AIN0_less = 0
                AIN1_less = 0
                AIN2_less = 0
                AIN3_less = 0
                AIN0_range = 0
                AIN1_range = 0
                AIN2_range = 0
                AIN3_range = 0
        
        if is_COM_HC:
            try:
                HC = str(COM_HC.readline());
                HC = HC.split("\\r\\n")[0];
                HC = HC.split("b'")[1];
            except Exception as e: 
                print(e)
                HC = "0"
        
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
                try:
                    try:
                        print("Retry COM_WS CONNECTING " + serial_port_WS + " ..")
                        COM_WS = VantagePro2.from_url("serial:%s:%s:8N1" % (serial_port_WS,serial_rate_WS))
                        print("[V] COM_WS CONNECTED with " + serial_port_WS)
                        ws_data = COM_WS.get_current_data()
                        WS = ws_data.to_csv(';',False)
                    except:                
                        print("Retry COM_WS CONNECTING " + serial_port_WS2 + " ..")
                        COM_WS = VantagePro2.from_url("serial:%s:%s:8N1" % (serial_port_WS2,serial_rate_WS))
                        print("[V] COM_WS CONNECTED with " + serial_port_WS2)
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
                
                GPGGA = ws_data.split("$GPGGA,")[1];
                GPGGA = GPGGA.split("\\r\\n")[0];
                
                barometer = WIMDA.split(",")[0];
                if barometer == "": barometer = "0.0";
                
                temp = WIMDA.split(",")[4];
                if temp == "": temp = "0.0";
                temp = str((9/5 * float(temp)) + 32);
                
                humidity = WIMDA.split(",")[8];
                if humidity == "": humidity = "0.0";
                
                windspeed = WIMWV.split(",")[2];
                if windspeed == "": windspeed = "0.0";
                windspeed = '{:.{}f}'.format(1.852 * float(windspeed), 1);
                
                winddir = WIMWV.split(",")[0];
                if winddir == "": winddir = "0.0";
                
                rainrate = "0.0";
                solarrad = "0.0";
                
                lat = GPGGA.split(",")[1];
                ns = GPGGA.split(",")[2];
                lon = GPGGA.split(",")[3];
                ew = GPGGA.split(",")[4];
                
                if lat != "" and lon != "":
                    lat = str(float(lat) / 100);
                    lon = str(float(lon) / 100);
                    lat1 = lat.split(".")[0];
                    lat2 = str(float("0." + lat.split(".")[1]) / 60).replace("0.00","");
                    lat = lat1 + "." + lat2;
                    lon1 = lon.split(".")[0];
                    lon2 = str(float("0." + lon.split(".")[1]) / 60).replace("0.00","");
                    lon = lon1 + "." + lon2;
                    
                    if ns == "S": lat = "-" + lat;
                    if ew == "W": lon = "-" + lon;
                    
                WS = ";0;" + barometer + ";" + temp + ";" + humidity + ";" + temp + ";" + windspeed + ";" + windspeed + ";" + winddir + ";" + humidity + ";" + rainrate + ";0;" + solarrad + ";0.0;0;" + rainrate + ";" + lat + ";" + lon;
                    
                sql = "UPDATE aqm_configuration SET content='" + lat + "' WHERE data = 'sta_lat'";
                mycursor.execute(sql)
                mydb.commit()
                sql = "UPDATE aqm_configuration SET content='" + lon + "' WHERE data = 'sta_lon'";
                mycursor.execute(sql)
                mydb.commit()
                
            except Exception as e: 
                print(e)
                WS = ""
            
        if is_Pump_pwm:
            try:
                mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'pump_state'")
                rec = mycursor.fetchone()
                for row in rec: pump_state = int(rec[0])
                speed = (pump_state * 100) + pump_speed;
                print("speed : " + str(speed))
                if pump_state != cur_pump_state:
                    cur_pump_state = pump_state
                    Pump_pwm.write(speed.encode());
            except Exception as e: 
                print(e)
        
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
        
        sql = "UPDATE aqm_sensor_values SET AIN0 = %s, AIN1 = %s, AIN2 = %s, AIN3 = %s, HC = %s, PM25 = %s, PM10 = %s, WS = %s WHERE id = 1"
        val = (AIN0,AIN1,AIN2,AIN3,HC,PM25,PM10,WS)
        mycursor.execute(sql, val)
        mydb.commit()
        
        print("AIN0 = %f ; AIN1 = %f ; AIN2 = %f ; AIN3 = %f ; HC = %s; PM10 = %s;  PM25 = %s ; WS = %s ; cur_pump_state = %s" % (AIN0,AIN1,AIN2,AIN3,HC,PM10,PM25,WS,cur_pump_state))
        print("MIN ==> AIN0 = %f ; AIN1 = %f ; AIN2 = %f ; AIN3 = %f " % (AIN0_less,AIN1_less,AIN2_less,AIN3_less))
        print("RANGE ==> AIN0 = %f ; AIN1 = %f ; AIN2 = %f ; AIN3 = %f " % (AIN0_range,AIN1_range,AIN2_range,AIN3_range))
        print("=========================================================================================================================");
        
    except Exception as e: 
        print(e)

    time.sleep(1) 