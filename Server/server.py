from socket import *
import os
from Session import Session

serverPort = 8090
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(250)
print('The server is ready to recieve connections in {}:{}'.format(gethostbyname(gethostname()),serverPort))

while True:
	print('waiting for connection...')
	clientsock, addr = serverSocket.accept()
	print('...connected from:',addr)
	t = Session(clientsock, addr)
	t.start()




