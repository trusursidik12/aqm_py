from __future__ import print_function
from pymodbus.client.sync import ModbusSerialClient
import sys
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time
import serial.rs485

is_PM_connect = False

try:
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="trusur_aqm")
    mycursor = mydb.cursor()

    print("[V] PM Database CONNECTED")
except Exception as e:
    print("  [X] PM " + e)


def connect_pm():
    global is_PM_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_pm_sds019'")
        rec = mycursor.fetchone()
        for row in rec:
            serial_port = rec[0]

        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_pm_sds019'")
        rec = mycursor.fetchone()
        for row in rec:
            serial_rate = rec[0]

        ser = serial.rs485.RS485(port=serial_port, baudrate=serial_rate)
        ser.rs485_mode = serial.rs485.RS485Settings(rts_level_for_tx=False, rts_level_for_rx=True, delay_before_tx=0.0, delay_before_rx=-0.0)
        client = ModbusSerialClient(method='rtu')
        client.socket = ser
        client.connect()
        result = client.read_holding_registers(address=0x00B4, count=3, unit=1)
        client.close()
        return result
        
    except Exception as e:
        return None


try:
    while True:
        try:
            PM = connect_pm()
            if(str(PM).count("None") == 1):            
                sql = "UPDATE aqm_sensor_values SET PM25 = '0,0,0' WHERE id = 1"
                mycursor.execute(sql)
                mydb.commit()
                
            if(str(PM).count("ReadRegisterResponse") == 1):
                sql = "UPDATE aqm_sensor_values SET PM25 = '" + str(PM.registers).replace(" ","").replace("[","").replace("]","") + "' WHERE id = 1"
                mycursor.execute(sql)
                mydb.commit()
        except Exception as e2:
            print(e2)
            print("Reconnect PM");
            sql = "UPDATE aqm_sensor_values SET PM25 = '0,0,0' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()

        time.sleep(1)

except Exception as e:
    print(e)