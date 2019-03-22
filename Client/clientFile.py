import socket

sock = socket.socket()
sock.connect(('localhost', 12345))

with open('test.mp4', 'rb') as f:
    sock.sendfile(f, 0)
    