from __future__ import print_function
import sys
from mysql.connector.constants import ClientFlag
import mysql.connector
import time
import serial

is_WS_connect = False

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] AIRMAR Database CONNECTED")
except Exception as e: 
    print("[X]  AIRMAR " + e)
    
def connect_ws():
    global is_WS_connect
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'com_airmar'")
        rec = mycursor.fetchone()
        for row in rec: serial_port = rec[0]
        
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'baud_airmar'")
        rec = mycursor.fetchone()
        for row in rec: baudrate = rec[0]
        
        try:
            COM_WS = serial.Serial(serial_port, baudrate)
            i = 0
            ws_data = ""
            while i <= 12:
                ws_data = ws_data + str(COM_WS.readline());
                i += 1
            
            WIMDA = ws_data.split("$WIMDA,")[1];
            WIMDA = WIMDA.split("\\r\\n")[0];
            
            if(WIMDA != ""):
                is_WS_connect = True
                return COM_WS
            else:
                is_WS_connect = False
                return None
                
        except:
            is_WS_connect = False
            return None
            
    except Exception as e: 
        return None
    
try:
    while True :
        try:
            if(not is_WS_connect):
                COM_WS = connect_ws()
        
            i = 0
            ws_data = ""
            while i <= 12:
                ws_data = ws_data + str(COM_WS.readline());
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
                
            sql = "UPDATE aqm_sensor_values SET WS = '" + WS + "' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit() 
            
            sql = "UPDATE aqm_configuration SET content='" + lat + "' WHERE data = 'sta_lat'";
            mycursor.execute(sql)
            mydb.commit()
            sql = "UPDATE aqm_configuration SET content='" + lon + "' WHERE data = 'sta_lon'";
            mycursor.execute(sql)
            mydb.commit()           
            #print(WS)
        except Exception as e2: 
            is_WS_connect = False
            print("Reconnect WS AIRMAR");
            sql = "UPDATE aqm_sensor_values SET WS = ';0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()
        
        time.sleep(1)
        
except Exception as e: 
    print(e)