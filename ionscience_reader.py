from __future__ import print_function
from pymodbus.client.sync import ModbusSerialClient
import sys
import minimalmodbus
import serial
from mysql.connector.constants import ClientFlag
import mysql.connector
import time
import serial.rs485

serial_port='COM5'
serial_rate=19200

ion=minimalmodbus.Instrument(serial_port,1)
ion.serial.baudrate=serial_rate
ion.serial.parity=serial.PARITY_NONE
ion.serial.bytesize=8
ion.serial.stopbits=1
ion.mode=minimalmodbus.MODE_RTU
ion.serial.timeout=0.05
modbus=ion.write_register(0x1248,1)


#ser = serial.rs485.RS485(port=serial_port, baudrate=serial_rate)
#ser.rs485_mode = serial.rs485.RS485Settings(rts_level_for_tx=False, rts_level_for_rx=True, delay_before_tx=0.0, delay_before_rx=0.0)
#client = ModbusSerialClient(method='rtu')
#client.socket = ser
#client.connect()
#client.write_register(0x1248,0x01);
# time.sleep(3)
#result = client.read_holding_registers(0x1202, count=2, unit=1)
#print(result.registers)
#client.close()