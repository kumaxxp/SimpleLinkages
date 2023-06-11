import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.100', 80))  # Replace 'server_ip' with the IP address of the M5Stack Basic
s.sendall(b'Hello, world')
data = s.recv(1024)
s.close()

print('Received', repr(data))
