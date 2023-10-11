import socket

from config import server_address

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((server_address, 3772))
    s.sendall(bytes([0x00]))
    data = s.recv(1)
    print(data)
