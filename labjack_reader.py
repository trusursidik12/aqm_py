from __future__ import print_function
from labjack import ljm
from mysql.connector.constants import ClientFlag
import mysql.connector
import time

AIN0 = 0
AIN1 = 0
AIN2 = 0
AIN3 = 0
AIN4 = 0
AIN5 = 0
AIN6 = 0
AIN7 = 0
AIN8 = 0
AIN9 = 0
AIN10 = 0
AIN11 = 0
AIN12 = 0
AIN13 = 0
AIN14 = 0
AIN15 = 0
A_AIN = [0] * 16

try:
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd="root", database="trusur_aqm")
    mycursor = mydb.cursor()

    print("[V] Labjack Database CONNECTED")
except Exception as e:
    print("[X]  Labjack " + str(e))

params = ""
while True:
    try:
        mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'labjack_force_on'")
        rec = mycursor.fetchone()
        if(str(rec[0]) == "1"):
            mycursor.execute("SELECT content FROM aqm_configuration WHERE data = 'param_labjack'")
            rec = mycursor.fetchone()
            for row in rec: params = rec[0]
            if(params.count(";") > 0):
                params = params.split(";")
    
        labjack = ljm.openS("ANY", "ANY", "ANY")
        AIN0 = ljm.eReadName(labjack, "AIN0")
        AIN1 = ljm.eReadName(labjack, "AIN1")
        AIN2 = ljm.eReadName(labjack, "AIN2")
        AIN3 = ljm.eReadName(labjack, "AIN3")
        AIN4 = ljm.eReadName(labjack, "AIN4")
        AIN5 = ljm.eReadName(labjack, "AIN5")
        AIN6 = ljm.eReadName(labjack, "AIN6")
        AIN7 = ljm.eReadName(labjack, "AIN7")

        try:
            AIN8 = ljm.eReadName(labjack, "AIN8")
            AIN9 = ljm.eReadName(labjack, "AIN9")
            AIN10 = ljm.eReadName(labjack, "AIN10")
            AIN11 = ljm.eReadName(labjack, "AIN11")
            AIN12 = ljm.eReadName(labjack, "AIN12")
            AIN13 = ljm.eReadName(labjack, "AIN13")
            AIN14 = ljm.eReadName(labjack, "AIN14")
            AIN15 = ljm.eReadName(labjack, "AIN15")

        except Exception as e2:
            AIN8 = 0
            AIN9 = 0
            AIN10 = 0
            AIN11 = 0
            AIN12 = 0
            AIN13 = 0
            AIN14 = 0
            AIN15 = 0

    except Exception as e:
        AIN0 = 0
        AIN1 = 0
        AIN2 = 0
        AIN3 = 0
        AIN4 = 0
        AIN5 = 0
        AIN6 = 0
        AIN7 = 0
        AIN8 = 0
        AIN9 = 0
        AIN10 = 0
        AIN11 = 0
        AIN12 = 0
        AIN13 = 0
        AIN14 = 0
        AIN15 = 0
    
    
        
    if(params != ""):
        A_AIN[0] = AIN0;
        A_AIN[1] = AIN1;
        A_AIN[2] = AIN2;
        A_AIN[3] = AIN3;
        A_AIN[4] = AIN4;
        A_AIN[5] = AIN5;
        A_AIN[6] = AIN6;
        A_AIN[7] = AIN7;
        A_AIN[8] = AIN8;
        A_AIN[9] = AIN9;
        A_AIN[10] = AIN10;
        A_AIN[11] = AIN11;
        A_AIN[12] = AIN12;
        A_AIN[13] = AIN13;
        A_AIN[14] = AIN14;
        A_AIN[15] = AIN15;
        VALUES = ""
        for x in range(len(params)):
            VALUES = VALUES + " AIN" + str(params[x]) + " = " + str(A_AIN[int(params[x])])
            if(x < len(params) - 1):
                VALUES = VALUES + ","
            
        sql = "UPDATE aqm_sensor_values SET " + VALUES + " WHERE id = 1"
        mycursor.execute(sql)
        mydb.commit()
    else:
        sql = "UPDATE aqm_sensor_values SET AIN0 = %s, AIN1 = %s, AIN2 = %s, AIN3 = %s, AIN4 = %s, AIN5 = %s, AIN6 = %s, AIN7 = %s, AIN8 = %s, AIN9 = %s, AIN10 = %s, AIN11 = %s, AIN12 = %s, AIN13 = %s, AIN14 = %s, AIN15 = %s WHERE id = 1"
        val = (AIN0, AIN1, AIN2, AIN3, AIN4, AIN5, AIN6, AIN7, AIN8, AIN9, AIN10, AIN11, AIN12, AIN13, AIN14, AIN15)
        mycursor.execute(sql, val)
        mydb.commit()
        
    #print("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (AIN0,AIN1,AIN2,AIN3,AIN4,AIN5,AIN6,AIN7,AIN8,AIN9,AIN10,AIN11,AIN12,AIN13,AIN14,AIN15));

    time.sleep(1)
