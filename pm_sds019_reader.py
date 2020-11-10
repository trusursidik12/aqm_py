from pymodbus.client.sync import ModbusSerialClient
import serial.rs485

ser=serial.rs485.RS485(port='/dev/ttyUSB0',baudrate=9600)
ser.rs485_mode = serial.rs485.RS485Settings(rts_level_for_tx=False,rts_level_for_rx=True, delay_before_tx=0.0, delay_before_rx=-0.0)

client = ModbusSerialClient(method='rtu')
client.socket = ser
client.connect()
result = client.read_holding_registers(address=0x00B4, count=3, unit=1)
print(result)
print(result.registers)
client.close()
