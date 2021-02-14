from __future__ import print_function
import sys
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

is_Digital_Sensor_connect = False

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] Digital Sensor Database CONNECTED")
except Exception as e: 
    print("[X]  [V] Digital Sensor " + e)
    
def connect_digital_sensor(i_com):
    global is_Digital_Sensor_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_digital_sensors'")
        rec = mycursor.fetchone()
        for row in rec:
            serial_port = str(rec[0]).split(";")[i_com]
        
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_digital_sensors'")
        rec = mycursor.fetchone()
        for row in rec: 
            try:
                serial_rate = str(rec[0]).split(";")[i_com]
            except Exception as e2:
                serial_rate = str(rec[0]).split(";")[0]
                
        if(serial_rate == ""):
            serial_rate = str(rec[0]).split(";")[0]
        
        COM_Digital_Sensor = serial.Serial(serial_port, serial_rate)
        DIGITAL_SENSOR = str(COM_Digital_Sensor.readline())
        if(DIGITAL_SENSOR.count(",") == 0 and DIGITAL_SENSOR.count("\\r\\n") == 1 and DIGITAL_SENSOR.count("b'") == 1):
            is_Digital_Sensor_connect = True
            return COM_Digital_Sensor 
        else:
            is_Digital_Sensor_connect = False
            return None
            
    except Exception as e: 
        return None
    
try:
    while True :
        try:
            mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'ain_digital_sensors'")
            rec = mycursor.fetchone()
            for row in rec:
                i_ain = str(rec[0]).split(";")[int(sys.argv[1])]
        
            if(not is_Digital_Sensor_connect):
                COM_Digital_Sensor = connect_digital_sensor(int(sys.argv[1]))
        
            DIGITAL_SENSOR = str(COM_Digital_Sensor.readline())
            if(DIGITAL_SENSOR.count(",") == 0 and DIGITAL_SENSOR.count("\\r\\n") == 1 and DIGITAL_SENSOR.count("b'") == 1):
                DIGITAL_SENSOR = DIGITAL_SENSOR.split("\\r\\n")[0];
                DIGITAL_SENSOR = DIGITAL_SENSOR.split("b'")[1];
            else:
                DIGITAL_SENSOR = "0"
                
            sql = "UPDATE aqm_sensor_values SET AIN"+ i_ain +" = '" + DIGITAL_SENSOR + "' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
            
            #print(DIGITAL_SENSOR)
        except Exception as e2: 
            is_Digital_Sensor_connect = False
            print("Reconnect Digital_Sensor");
            sql = "UPDATE aqm_sensor_values SET AIN"+ i_ain +" = '-1' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)