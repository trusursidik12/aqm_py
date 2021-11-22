from __future__ import print_function
from pyvantagepro import VantagePro2
from mysql.connector.constants import ClientFlag
import mysql.connector
import sys
import serial
import time
import subprocess
import glob

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
except Exception as e: 
    print("[X] " + e)

mycursor.execute("UPDATE aqm_configuration SET content='' WHERE data LIKE 'com_pm10'")
mydb.commit()
mycursor.execute("UPDATE aqm_configuration SET content='' WHERE data LIKE 'com_pm25'")
mydb.commit()
mycursor.execute("UPDATE aqm_configuration SET content='' WHERE data LIKE 'com_hc'")
mydb.commit()
mycursor.execute("UPDATE aqm_configuration SET content='' WHERE data LIKE 'com_ws'")
mydb.commit()

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
    
def check_as_arduino(port):
    try:
        COM = serial.Serial()
        COM.port = port
        COM.baudrate = 9600
        COM.timeout = 3
        COM.open()
        retval = str(COM.readline())

        if(retval.count("000.") > 0 and retval.count(",+") > 0 and retval.count(",*") > 0):
            mycursor.execute("UPDATE aqm_configuration SET content='" + port + "' WHERE (data LIKE 'com_pm10' OR data LIKE 'com_pm25') AND content='' LIMIT 1")
            mydb.commit()
            print(" ==> PM")
            
        if(int(retval.replace("b'","").replace("\\r\\n'","")) >= 0 and int(retval.replace("b'","").replace("\\r\\n'","")) <= 60000):
            mycursor.execute("UPDATE aqm_configuration SET content='" + port + "' WHERE data LIKE 'com_hc' AND content='' LIMIT 1")
            mydb.commit()
            print(" ==> HC")
    except Exception as e: 
        None
        
def check_as_ventagepro2(port):
    try:
        COM_WS = VantagePro2.from_url("serial:%s:19200:8N1" % (port))
        ws_data = COM_WS.get_current_data()
        WS = ws_data.to_csv(';',False)
        mycursor.execute("UPDATE aqm_configuration SET content='" + port + "' WHERE data LIKE 'com_ws' AND content='' LIMIT 1")
        mydb.commit() 
        print(" ==> VANTAGEPRO2")
    except Exception as e:
        None
        
mycursor.execute("TRUNCATE TABLE serial_ports")
mydb.commit()
for port in serial_ports():
    print("Adding port " + port)
    port_desc = ""

    if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
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
    try:
        mycursor.execute("INSERT INTO serial_ports (port,description) VALUES ('" + port +"','" + port_desc +"')")
        mydb.commit()
    except Exception as e: 
        None
    
mycursor.execute("SELECT port,description FROM serial_ports ORDER BY port")
serial_ports = mycursor.fetchall()
for serial_port in serial_ports:
    print(serial_port[0])
    if(str(serial_port[0]).count("ttyS") > 0 or str(serial_port[0]).count("ttyUSB") > 0 or str(serial_port[0]).count("ttyPM") > 0 or str(serial_port[0]).count("ttyWS") > 0 or str(serial_port[0]).count("COM") > 0):
        check_as_ventagepro2(serial_port[0])
        
        mycursor.execute("SELECT id FROM aqm_configuration WHERE content LIKE '"+ serial_port[0] +"'")
        try:
            sensor_reader_id = mycursor.fetchone()[0]
        except Exception as e:
            sensor_reader_id = ""
        if(str(sensor_reader_id) == ""):
            check_as_arduino(serial_port[0])