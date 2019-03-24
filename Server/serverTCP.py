from socket import *
import os
from Session import Session

serverPort = 8070
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('0.0.0.0',serverPort))
serverSocket.listen(250)
print('The server is ready to recieve connections')

while True:
	print('waiting for connection...')
	clientsock, addr = serverSocket.accept()
	print('...connected from:',addr)
	t = Session(clientsock, addr)
	t.start()





