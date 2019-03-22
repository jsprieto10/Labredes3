import socket

CHUNK_SIZE = 8 * 1024


server_socket = socket.socket()
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
client_socket, addr = server_socket.accept()

with open('test.mp4', 'wb') as f:
    while True:
        chunk = client_socket.recv(CHUNK_SIZE)
        if not chunk: break
        f.write(chunk)
client_socket.close()