import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

UDP_IP = "192.168.1.252"
UDP_PORT = 5959
byte_message = bytes("4a100e007e149b166c2ce91b", "utf-8")

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", byte_message)

sock.sendto(byte_message, (UDP_IP, UDP_PORT))