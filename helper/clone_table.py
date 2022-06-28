from datetime import datetime
import mysql.connector
import sys
# Pastikan sudah membuat database data_logger sebelum menjalankan

# Cronjob cloning table aqm_data every month
# 5 1 1 * * /usr/bin/python3 /home/admin/aqm_py/helper/clone_table.py aqm_data >/dev/null 2>&1

# Cronjob cloning table aqm_data_log per 2 jam
# 5 */2 * * * /usr/bin/python3 /home/admin/aqm_py/helper/clone_table.py aqm_data_log >/dev/null 2>&1

args = sys.argv
try:
    table = str(args[1]) # table name from argument
except IndexError:
    table = None
if table : # If has arg table
    hour = str(datetime.now().hour)
    minute = str(datetime.now().minute)
    day = str(datetime.now().day)
    month = str(datetime.now().month)
    year = str(datetime.now().year)

    activeTable = table
    if(activeTable == "aqm_data_log"):
        newTable = activeTable+"_"+hour+"_"+minute+"_"+day+"_"+month+"_"+year
    else:
        newTable = activeTable+"_"+day+"_"+month+"_"+year
    connection = mysql.connector.connect(user="root",password="root")
    db = connection.cursor()

    try:
        query = "CREATE TABLE data_logger."+newTable+" SELECT * FROM trusur_aqm."+activeTable
        db.execute(query) # Clone Table
        db.execute("TRUNCATE trusur_aqm."+activeTable) # Truncate Table
        print("[Success] - Cloning table "+activeTable+" was successfully!")
    except mysql.connector.Error as e:
        print(str(e))