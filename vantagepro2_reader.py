from __future__ import print_function
from pyvantagepro import VantagePro2
import sys
import time
    
try:
    COM_WS = VantagePro2.from_url("serial:%s:19200:8N1" % (sys.argv[1]))
    ws_data = COM_WS.get_current_data()
    print(ws_data.to_csv(';',False))
except:
    print("Error: not connected")