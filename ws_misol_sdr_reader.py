import time
import datetime
from mysql.connector.constants import ClientFlag
import mysql.connector

try:
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="trusur_aqm")
    mycursor = mydb.cursor()
    
    print("[V] WS MISOL SDR Database CONNECTED")
except Exception as e: 
    print("[X]  WS MISOL SDR " + e)

is_WS_connect = False

sql = "UPDATE aqm_sensor_values SET WS = ';0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0' WHERE id = 1"
mycursor.execute(sql)
mydb.commit()

def read_ws():
    global is_WS_connect
    is_WS_connect = True
    try:
        f = open("../misol_sdr.txt", "r")
        content = str(f.read()).split("Fineoffset-WHx080")
        content = content[len(content)-1]
        return content
    except Exception as e:
        is_WS_connect = False
        return ""
        
try:
    while True:
        try:
            ws_content = read_ws()
            if(ws_content != ""):
                outdoor_temperature = float(ws_content.split("Temperature: ")[1].split(" C")[0])
                wind_speed = float(ws_content.split("Wind avg speed: ")[1].split(" ")[0])
                wind_dirs = ws_content.split("Wind Direction: ")[1].split(" ")[0]
                outdoor_humidity = ws_content.split("Humidity  : ")[1].split(" %")[0]
                rain = float(ws_content.split("Total rainfall: ")[1].split(" ")[0])
                
                WS = str(datetime.datetime.now()) + ";0;0;0;0;" + str((outdoor_temperature*9/5)+32) + ";" + str(round(wind_speed,2)) + ";" + str(round(wind_speed,2)) + ";" + wind_dirs + ";" + outdoor_humidity + ";" + str(round(rain,2)) + ";0;0;0.0;0;" + str(round(rain,2)) + ";0;0"
                sql = "UPDATE aqm_sensor_values SET WS = '" + WS + "' WHERE id = 1"
                mycursor.execute(sql)
                mydb.commit()
                f = open("../misol_sdr.txt", "w")
                f.write("")
                f.close()
                
            # print(WS)
                
        except Exception as e2:
            is_WS_connect = False
            print("Reconnect WS MISOL SDR : " + str(e2));
            sql = "UPDATE aqm_sensor_values SET WS = ';0;0;0;0;0;0;0;0;0;0;0;0;0.0;0;0;0;0' WHERE id = 1"
            mycursor.execute(sql)
            mydb.commit()

        time.sleep(10)
	

except Exception as e:
    print(e)
