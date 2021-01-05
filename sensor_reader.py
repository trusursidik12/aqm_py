import sys
import time
import mysql.connector
import serial
import subprocess
import glob

AIN0 = 0
AIN1 = 0
AIN2 = 0
AIN3 = 0
AIN4 = 0
AIN5 = 0
AIN6 = 0
AIN7 = 0
HC = "0"
PM10 = ""
PM25 = ""
PM_SDS019 = ""
WS = ""
pump_speed = 0
cur_pump_state = "0"
cur_selenoid_state = "q"
cur_purge_state = "o"
is_COM_GASREADER = False
is_COM_ION_SCIENCE = False
is_COM_PM10 = False
is_COM_PM25 = False
is_COM_SDS019 = False
is_COM_HC = False
is_COM_WS = False
is_COM_AIRMAR = False
is_COM_RHT = False
is_Arduino = False
is_Pump_pwm = False

i_retry_GASREADER = 0
i_retry_ION_SCIENCE = 0
i_retry_PM10 = 0
i_retry_PM25 = 0
i_retry_SDS019 = 0
i_retry_HC = 0
i_retry_WS = 0
i_retry_AIRMAR = 0
i_retry_RHT = 0

retry_GASREADER = []
retry_ION_SCIENCE = []
retry_PM10 = []
retry_PM25 = []
retry_SDS019 = []
retry_HC = []
retry_WS = []
retry_AIRMAR = []
retry_RHT = []


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

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()    
    mycursor.execute("DELETE FROM aqm_sensor_values WHERE id=1")
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
        Pump_pwm.write(str(pump_speed).encode());
        
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

AIN1_less = 99999
AIN0_less = 99999
AIN2_less = 99999
AIN3_less = 99999
AIN4_less = 99999
AIN5_less = 99999
AIN6_less = 99999
AIN7_less = 99999
AIN0_range = 0
AIN1_range = 0
AIN2_range = 0
AIN3_range = 0
AIN4_range = 0
AIN5_range = 0
AIN6_range = 0
AIN7_range = 0


try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_gasreader'")
    rec = mycursor.fetchone()
    if(rec[0] != None and rec[0] != ""):
        is_COM_GASREADER = True
        i_retry_GASREADER = 0
        if sys.platform.startswith('win'):
            command = "gasreader_reader.py"
        else:
            command = "echo admin | sudo -S python3.5 ~/aqm_py/gasreader_reader.py"
        
        subprocess.Popen(command, shell=True)
except Exception as e:
    print(e)
    
try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_ion_science'")
    rec = mycursor.fetchone()
    if(rec[0] != None and rec[0] != ""):
        is_COM_ION_SCIENCE = True
        i_retry_ION_SCIENCE = 0
        
        i = 0
        while(i < len(str(rec[0]).split(";"))):
            if sys.platform.startswith('win'):
                command = "ionscience_reader.py " + str(i)
            else:
                command = "echo admin | sudo -S python3.5 ~/aqm_py/ionscience_reader.py " + str(i)
            
            subprocess.Popen(command, shell=True)
            i += 1
            
except Exception as e:
    print(e)
    
try:
    if(is_COM_GASREADER == False and is_COM_ION_SCIENCE == False):
        if sys.platform.startswith('win'):
            command = "labjack_reader.py"
        else:
            command = "echo admin | sudo -S python3.5 ~/aqm_py/labjack_reader.py"
            
        subprocess.Popen(command, shell=True)
        
    else:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'labjack_force_on'")
        rec = mycursor.fetchone()
        if(str(rec[0]) == "1"):
            if sys.platform.startswith('win'):
                command = "labjack_reader_force.py"
            else:
                command = "echo admin | sudo -S python3.5 ~/aqm_py/labjack_reader_force.py"
                
            subprocess.Popen(command, shell=True)
            
except Exception as e:
    print(e)
    

try:
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm10'")
    rec = mycursor.fetchone()
    if(rec[0] != None and rec[0] != ""):
        is_COM_PM10 = True
        i_retry_PM10 = 0
        if sys.platform.startswith('win'):
            command = "pm_reader.py 10"
        else:
            command = "echo admin | sudo -S python3.5 ~/aqm_py/pm_reader.py 10"

        subprocess.Popen(command, shell=True)
except Exception as e:
    print(e)

try:    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm25'")
    rec = mycursor.fetchone()
    if(rec[0] != None and rec[0] != ""):
        is_COM_PM25 = True
        i_retry_PM25 = 0
        if sys.platform.startswith('win'):
            command = "pm_reader.py 25"
        else:
            command = "echo admin | sudo -S python3.5 ~/aqm_py/pm_reader.py 25"

        subprocess.Popen(command, shell=True)
except Exception as e:
    print(e)
    
try:    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm_sds019'")
    rec = mycursor.fetchone()
    if(rec[0] != None and rec[0] != ""):
        is_COM_SDS019 = True
        i_retry_SDS019 = 0
        if sys.platform.startswith('win'):
            command = "pm_sds019_reader.py"
        else:
            command = "echo admin | sudo -S python3.5 ~/aqm_py/pm_sds019_reader.py"

        subprocess.Popen(command, shell=True)
except Exception as e:
    print(e)

try:    
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_hc'")
    rec = mycursor.fetchone()
    if(rec[0] != None and rec[0] != ""):
        is_COM_HC = True
        i_retry_HC = 0
        if sys.platform.startswith('win'):
            command = "hc_reader.py"
        else:
            command = "echo admin | sudo -S python3.5 ~/aqm_py/hc_reader.py"

        subprocess.Popen(command, shell=True)
except Exception as e:
    print(e)

try:        
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_ws'")
    rec = mycursor.fetchone()
    if(rec[0] != None and rec[0] != ""):
        is_COM_WS = True
        i_retry_WS = 0
        if(rec[0] == "pce_fws20n"):
            if sys.platform.startswith('win'):
                command = "ws_fws20n_reader.py"
            else:
                command = "echo admin | sudo -S python3.5 ~/aqm_py/ws_fws20n_reader.py"

        else:
            if sys.platform.startswith('win'):
                command = "ws_davis_reader.py"
            else:
                command = "echo admin | sudo -S python3.5 ~/aqm_py/ws_davis_reader.py"

        subprocess.Popen(command, shell=True)
except Exception as e:
    print(e)

try:        
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_airmar'")
    rec = mycursor.fetchone()
    if(rec[0] != None and rec[0] != ""):
        is_COM_AIRMAR = True
        i_retry_AIRMAR = 0
        if sys.platform.startswith('win'):
            command = "ws_airmar_reader.py"
        else:
            command = "echo admin | sudo -S python3.5 ~/aqm_py/ws_airmar_reader.py"

        subprocess.Popen(command, shell=True)
except Exception as e:
    print(e)
    
try:        
    mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_rht'")
    rec = mycursor.fetchone()
    if(rec[0] != None and rec[0] != ""):
        is_COM_RHT = True
        i_retry_RHT = 0
        if sys.platform.startswith('win'):
            command = "rht_reader.py.py"
        else:
            command = "echo admin | sudo -S python3.5 ~/aqm_py/rht_reader.py.py"

        subprocess.Popen(command, shell=True)
except Exception as e:
    print(e)


time.sleep(5)
    
while True:
    try:
        try:
            mycursor.execute("SELECT AIN0,AIN1,AIN2,AIN3,AIN4,AIN5,AIN6,AIN7 FROM aqm_sensor_values WHERE id = '1'")
            rec = mycursor.fetchone()
            AIN0 = float(rec[0])
            AIN1 = float(rec[1])
            AIN2 = float(rec[2])
            AIN3 = float(rec[3])
            AIN4 = float(rec[4])
            AIN5 = float(rec[5])
            AIN6 = float(rec[6])
            AIN7 = float(rec[7])
            if AIN0 < 0: 
                AIN0 = 0
                AIN0_less = 0
            if AIN1 < 0: 
                AIN1 = 0
                AIN1_less = 0
            if AIN2 < 0: 
                AIN2 = 0
                AIN2_less = 0
            if AIN3 < 0: 
                AIN3 = 0
                AIN3_less = 0
            if AIN4 < 0: 
                AIN4 = 0
                AIN4_less = 0
            if AIN5 < 0: 
                AIN5 = 0
                AIN5_less = 0
            if AIN6 < 0: 
                AIN6 = 0
                AIN6_less = 0
            if AIN7 < 0: 
                AIN7 = 0
                AIN7_less = 0
            if AIN0_less > AIN0 and AIN0 > 0: AIN0_less = AIN0
            if AIN1_less > AIN1 and AIN1 > 0: AIN1_less = AIN1
            if AIN2_less > AIN2 and AIN2 > 0: AIN2_less = AIN2
            if AIN3_less > AIN3 and AIN3 > 0: AIN3_less = AIN3
            if AIN4_less > AIN4 and AIN4 > 0: AIN4_less = AIN4
            if AIN5_less > AIN5 and AIN5 > 0: AIN5_less = AIN4
            if AIN6_less > AIN6 and AIN6 > 0: AIN6_less = AIN6
            if AIN7_less > AIN7 and AIN7 > 0: AIN7_less = AIN7
            AIN0_range = 0.04 - AIN0_less
            AIN1_range = 0.04 - AIN1_less
            AIN2_range = 0.04 - AIN2_less
            AIN3_range = 0.04 - AIN3_less
            AIN4_range = 0.04 - AIN4_less
            AIN5_range = 0.04 - AIN5_less
            AIN6_range = 0.04 - AIN6_less
            AIN7_range = 0.04 - AIN7_less
            
        except Exception as e: 
            print(e)
            AIN0 = 0
            AIN1 = 0
            AIN2 = 0
            AIN3 = 0
            AIN4 = 0
            AIN5 = 0
            AIN6 = 0
            AIN7 = 0
            AIN0_less = 0
            AIN1_less = 0
            AIN2_less = 0
            AIN3_less = 0
            AIN4_less = 0
            AIN5_less = 0
            AIN6_less = 0
            AIN7_less = 0
            AIN0_range = 0
            AIN1_range = 0
            AIN2_range = 0
            AIN3_range = 0
            AIN4_range = 0
            AIN5_range = 0
            AIN6_range = 0
            AIN7_range = 0
            
        try :
            mycursor.execute("SELECT PM10 FROM aqm_sensor_values WHERE id = '1'")
            rec = mycursor.fetchone()
            PM10 = rec[0]
        except Exception as e:
            PM10 = "b'000.000,0.0,+0.0,0,0,00,*0\\r\\n'"
            
        try :
            mycursor.execute("SELECT PM25 FROM aqm_sensor_values WHERE id = '1'")
            rec = mycursor.fetchone()
            PM25 = rec[0]
        except Exception as e:
            PM25 = "b'000.000,0.0,+0.0,0,0,00,*0\\r\\n'"
            
        try :
            mycursor.execute("SELECT HC FROM aqm_sensor_values WHERE id = '1'")
            rec = mycursor.fetchone()
            HC = rec[0]
        except Exception as e:
            HC = "0"
            
        try :
            mycursor.execute("SELECT WS FROM aqm_sensor_values WHERE id = '1'")
            rec = mycursor.fetchone()
            WS = rec[0]
        except Exception as e:
            WS = ";0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0";
                
        if is_Pump_pwm:
            try:
                mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'pump_state'")
                rec = mycursor.fetchone()
                for row in rec: pump_state = int(rec[0])
                speed = (pump_state * 100) + pump_speed;
                print("speed : " + str(speed))
                if pump_state != cur_pump_state:
                    cur_pump_state = pump_state
                    Pump_pwm.write(str(speed).encode());
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
                
            try:
                mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'selenoid_state'")
                rec = mycursor.fetchone()
                for row in rec: selenoid_state = rec[0]
                if selenoid_state != cur_selenoid_state:
                    cur_selenoid_state = selenoid_state
                    if cur_selenoid_state == "q":
                        Arduino.write(b'q');
                    elif cur_selenoid_state == "w":
                        Arduino.write(b'w');
                    elif cur_selenoid_state == "e":
                        Arduino.write(b'e');
                    elif cur_selenoid_state == "r":
                        Arduino.write(b'r');
                    elif cur_selenoid_state == "t":
                        Arduino.write(b't');
                    elif cur_selenoid_state == "y":
                        Arduino.write(b'y');
            except Exception as e: 
                print(e)
                
            try:
                mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'purge_state'")
                rec = mycursor.fetchone()
                for row in rec: purge_state = rec[0]
                if purge_state != cur_purge_state:
                    cur_purge_state = purge_state
                    if cur_purge_state == "o":
                        Arduino.write(b'o');
                    elif cur_purge_state == "p":
                        Arduino.write(b'p');
            except Exception as e: 
                print(e)


        mydb.commit()
        
        ##======START RETRY ========================================================================================================
        if(is_COM_PM10 and PM10[0:13] != "b'000.000,0.0"):
            i_retry_PM10 = 0
            retry_PM10.clear()
            
        if(is_COM_PM10 and PM10[0:13] == "b'000.000,0.0" and i_retry_PM10 <= 5 ):
            i_retry_PM10 = i_retry_PM10 + 1
            
        if(i_retry_PM10 > 5):
            i_retry_PM10 = 0
            print("Try Connecting PM10");
            for port in serial_ports():
                print("Try PORT PM10: " + port)
                if port not in retry_PM10:
                    retry_PM10.append(port)
                    sql = "UPDATE aqm_configuration SET content = '" + port + "' WHERE data = 'com_pm10'"
                    mycursor.execute(sql)
                    mydb.commit()
                    time.sleep(10)
                    break
                
                try :
                    mycursor.execute("SELECT PM10 FROM aqm_sensor_values WHERE id = '1'")
                    rec = mycursor.fetchone()
                    PM10 = rec[0]
                except Exception as e:
                    PM10 = "b'000.000,0.0,+0.0,0,0,00,*0\\r\\n'"
                    
                if(PM10[0:13] != "b'000.000,0.0"):
                    i_retry_PM10 = 0
                    retry_PM10.clear()
                    break
                
                
        if(is_COM_PM25 and PM25[0:13] != "b'000.000,0.0"):
            i_retry_PM25 = 0
            retry_PM25.clear()
            
        if(is_COM_PM25 and PM25[0:13] == "b'000.000,0.0" and i_retry_PM25 <= 5 ):
            i_retry_PM25 = i_retry_PM25 + 1
            
        if(i_retry_PM25 > 5):
            i_retry_PM25 = 0
            print("Try Connecting PM25");
            for port in serial_ports():
                print("Try PORT PM25: " + port)
                if port not in retry_PM25:
                    retry_PM25.append(port)
                    sql = "UPDATE aqm_configuration SET content = '" + port + "' WHERE data = 'com_PM25'"
                    mycursor.execute(sql)
                    mydb.commit()
                    time.sleep(10)
                    break
                
                try :
                    mycursor.execute("SELECT PM25 FROM aqm_sensor_values WHERE id = '1'")
                    rec = mycursor.fetchone()
                    PM25 = rec[0]
                except Exception as e:
                    PM25 = "b'000.000,0.0,+0.0,0,0,00,*0\\r\\n'"
                    
                if(PM25[0:13] != "b'000.000,0.0"):
                    i_retry_PM25 = 0
                    retry_PM25.clear()
                    break
                
                
        if(is_COM_HC and HC > -1):
            i_retry_HC = 0
            retry_HC.clear()
            
        if(is_COM_HC and HC == -1 and i_retry_HC <= 5 ):
            i_retry_HC = i_retry_HC + 1
            
        if(i_retry_HC > 5):
            i_retry_HC = 0
            print("Try Connecting HC");
            for port in serial_ports():
                print("Try PORT HC: " + port)
                if port not in retry_HC:
                    retry_HC.append(port)
                    sql = "UPDATE aqm_configuration SET content = '" + port + "' WHERE data = 'com_HC'"
                    mycursor.execute(sql)
                    mydb.commit()
                    time.sleep(10)
                    break
                
                try :
                    mycursor.execute("SELECT HC FROM aqm_sensor_values WHERE id = '1'")
                    rec = mycursor.fetchone()
                    HC = rec[0]
                except Exception as e:
                    HC = "-1"
                    
                if(HC > -1):
                    i_retry_HC = 0
                    retry_HC.clear()
                    break
                
        if(is_COM_WS and WS != ";0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0"):
            i_retry_WS = 0
            retry_WS.clear()
            
        if(is_COM_WS and WS == ";0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0" and i_retry_WS <= 5 ):
            i_retry_WS = i_retry_WS + 1
            
        if(i_retry_WS > 5):
            mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_ws'")
            rec = mycursor.fetchone()
            if(rec[0] != "pce_fws20n"):
                i_retry_WS = 0
                print("Try Connecting WS");
                for port in serial_ports():
                    print("Try PORT WS: " + port)
                    if port not in retry_WS:
                        retry_WS.append(port)
                        sql = "UPDATE aqm_configuration SET content = '" + port + "' WHERE data = 'com_WS'"
                        mycursor.execute(sql)
                        mydb.commit()
                        time.sleep(10)
                        break
                    
                    try :
                        mycursor.execute("SELECT WS FROM aqm_sensor_values WHERE id = '1'")
                        rec = mycursor.fetchone()
                        WS = rec[0]
                    except Exception as e:
                        WS = ";0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0"
                        
                    if(WS != ";0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0"):
                        i_retry_WS = 0
                        retry_WS.clear()
                        break
        ##======END RETRY ========================================================================================================
        
        print("PM10 = %s" % (PM10.replace("\r\n","")))
        print("PM25 = %s" % (PM25.replace("\r\n","")))
        try:
            print("WS = %s" % (WS[0:75]))
        except Exception as e:
            print("WS = 0")

        print("HC = %s" % (HC))
        print("cur_pump_state = %s" % (cur_pump_state))
        print("cur_selenoid_state = %s" % (cur_selenoid_state))
        print("cur_purge_state = %s" % (cur_purge_state))
        print("--------------------------------------------------------------------------------");
        print("AIN \t|\t VOLTAGE \t|\t MIN \t\t|\t RANGE \t\t|")
        print("--------------------------------------------------------------------------------");
        print("AIN0 \t|\t %f \t|\t %f \t|\t %f \t|" % (AIN0,AIN0_less,AIN0_range))
        print("AIN1 \t|\t %f \t|\t %f \t|\t %f \t|" % (AIN1,AIN1_less,AIN1_range))
        print("AIN2 \t|\t %f \t|\t %f \t|\t %f \t|" % (AIN2,AIN2_less,AIN2_range))
        print("AIN3 \t|\t %f \t|\t %f \t|\t %f \t|" % (AIN3,AIN3_less,AIN3_range))
        print("AIN4 \t|\t %f \t|\t %f \t|\t %f \t|" % (AIN4,AIN4_less,AIN4_range))
        print("AIN5 \t|\t %f \t|\t %f \t|\t %f \t|" % (AIN5,AIN5_less,AIN5_range))
        print("AIN6 \t|\t %f \t|\t %f \t|\t %f \t|" % (AIN6,AIN6_less,AIN6_range))
        print("AIN7 \t|\t %f \t|\t %f \t|\t %f \t|" % (AIN7,AIN7_less,AIN7_range))
        print("================================================================================");
        
    except Exception as e2: 
        print(e2)
        
    time.sleep(1)