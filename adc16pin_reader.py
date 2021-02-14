import sys
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

is_adc16pin_connect = False

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] Gas ADC 16 Pin Database CONNECTED")
except Exception as e: 
    print("[X]  [V] Gas ADC 16 Pin " + e)
    
    
def connect_adc16pin():
    global is_adc16pin_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_adc16pin'")
        rec = mycursor.fetchone()
        for row in rec: serial_port = rec[0]
        
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_adc16pin'")
        rec = mycursor.fetchone()
        for row in rec: serial_rate = rec[0]
        
        COM_ADC16PIN = serial.Serial(serial_port, serial_rate)
        time.sleep(3)
        ADC16PIN = str(COM_ADC16PIN.readline())
        if(ADC16PIN.count(";") == 16):
            is_adc16pin_connect = True
            return COM_ADC16PIN 
        else:
            is_adc16pin_connect = False
            return None
            
    except Exception as e: 
        return None


try:
    while True :
        try:
            mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'param_adc16pin'")
            rec = mycursor.fetchone()
            for row in rec: params = rec[0]
            if(params.count(";") > 0):
                params = params.split(";")
        
            if(not is_adc16pin_connect):
                COM_ADC16PIN = connect_adc16pin()
            
            ADC16PIN = str(COM_ADC16PIN.readline().decode("utf-8"))
            if(ADC16PIN.count(";") != 16):
                ADC16PIN = "0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;\\r\\n'"
            
            AIN = ADC16PIN.split(";")
            
            VALUES = ""
            for x in range(len(params)):
                VALUES = VALUES + " AIN" + str(params[x]) + " = " + AIN[int(params[x])]
                if(x < len(params) - 1):
                    VALUES = VALUES + ","
                
            sql = "UPDATE aqm_sensor_values SET " + VALUES + " WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
            
            # print(ADC16PIN)
        except Exception as e2:
            print(e2)
            is_adc16pin_connect = False
            print("Reconnect ADC16PIN : " + str(e2));
            
            VALUES = ""
            for x in range(len(params)):
                VALUES = VALUES + " AIN" + str(x) + " = 0"
                if(x < len(params) - 1):
                    VALUES = VALUES + ","
                
            sql = "UPDATE aqm_sensor_values SET " + VALUES + " WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)