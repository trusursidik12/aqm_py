from __future__ import print_function
import sys
from mysql.connector.constants import ClientFlag
import mysql.connector
import time
import serial

is_GPS_connect = False

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] GSTAR IV Database CONNECTED")
except Exception as e: 
    print("[X]  GSTAR IV " + e)
    
def connect_gps():
    global is_GPS_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_gstar_iv'")
        rec = mycursor.fetchone()
        for row in rec: serial_port = rec[0]
        
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_gstar_iv'")
        rec = mycursor.fetchone()
        for row in rec: baudrate = rec[0]
        
        try:
            COM_GPS = serial.Serial(serial_port, baudrate)
            i = 0
            gps_data = ""
            while i <= 12:
                gps_data = gps_data + str(COM_GPS.readline());
                i += 1
                
            GPGGA = gps_data.split("$GPGGA,")[1];
            GPGGA = GPGGA.split("\\r\\n")[0];
            
            if(GPGGA != ""):
                is_GPS_connect = True
                return COM_GPS
            else:
                is_GPS_connect = False
                return None
                
                
        except:
            is_GPS_connect = False
            return None
            
    except Exception as e: 
        return None
    
try:
    while True :
        try:
            if(not is_GPS_connect):
                COM_GPS = connect_gps()
                time.sleep(3)
        
            i = 0
            gps_data = ""
            while i <= 12:
                gps_data = gps_data + str(COM_GPS.readline());
                i += 1

            try:
                GPGGA = gps_data.split("$GPGGA,")[1];
                GPGGA = GPGGA.split("\\r\\n")[0];
            except Exception as x:
                GPGGA = ""

            lat = GPGGA.split(",")[1];
            ns = GPGGA.split(",")[2];
            lon = GPGGA.split(",")[3];
            ew = GPGGA.split(",")[4];
            altitude = GPGGA.split(",")[8];
            
            if(altitude == ""):
                altitude = "0"
                
            if(GPGGA.split(",")[9] != "M"):
                altitude = str(float(altitude) * 0,3048)
                
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
                
            sql = "UPDATE aqm_configuration SET content='" + lat + "' WHERE data = 'sta_lat'";
            mycursor.execute(sql)
            mydb.commit()
            sql = "UPDATE aqm_configuration SET content='" + lon + "' WHERE data = 'sta_lon'";
            mycursor.execute(sql)
            mydb.commit()    
            sql = "UPDATE aqm_configuration SET content='" + altitude + "' WHERE data = 'altitude'";
            mycursor.execute(sql)
            mydb.commit()
            sql = "UPDATE aqm_sensor_values SET GPS = '" + lat + ";" + lon + ";" + altitude + "' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit() 
            #print(lat + ";" + lon + ";" + altitude)
        except Exception as e2: 
            is_GPS_connect = False
            print("Reconnect GPS GSTAR IV");
            sql = "UPDATE aqm_configuration SET content='' WHERE data = 'sta_lat'";
            mycursor.execute(sql)
            mydb.commit()
            sql = "UPDATE aqm_configuration SET content='' WHERE data = 'sta_lon'";
            mycursor.execute(sql)
            mydb.commit() 
            sql = "UPDATE aqm_configuration SET content='0' WHERE data = 'altitude'";
            mycursor.execute(sql)
            mydb.commit()
            sql = "UPDATE aqm_sensor_values SET GPS = ';;0' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)