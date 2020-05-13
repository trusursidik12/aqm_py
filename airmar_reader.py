from __future__ import print_function
import sys
import time
import serial

try:    
    if len(sys.argv) > 2:
        baudrate = sys.argv[2];
    else :
        baudrate = 4800;
        
    COM_WS = serial.Serial(sys.argv[1], baudrate)
    i = 0
    WS = ""
    while i <= 12:
        WS = WS + str(COM_WS.readline());
        i += 1
        
    WIMDA = WS.split("$WIMDA,")[1];
    WIMDA = WIMDA.split("\\r\\n")[0];
    
    barometer = WIMDA.split(",")[0];
    if barometer == "": barometer = "0.0";
    barometer = str(33.8639 * float(barometer));
    
    temp = WIMDA.split(",")[4];
    if temp == "": temp = "0.0";
    
    humidity = WIMDA.split(",")[8];
    if humidity == "": humidity = "0.0";
    
    windspeed = WIMDA.split(",")[18];
    if windspeed == "": windspeed = "0.0";
    
    winddir = WIMDA.split(",")[12];
    if winddir == "": winddir = "0.0";
    
    rainrate = "0.0";
    solarrad = "0.0";
    print(barometer + ";" + temp + ";" + humidity + ";" + windspeed + ";" + winddir + ";" + rainrate + ";" + solarrad + ";");
except:
    print("Error: not connected")
    print("barometer;temp;humidity;windspeed;winddir;rainrate;solarrad;");