from socket import *
from tkinter import filedialog
from tkinter import *
import os

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

esta_loggeado = False
ejecutando = False
def dar_opciones():
	global ejecutando
	ejecutando = True
	if esta_loggeado:
		return input("""Subir video: Subir\nVer video: Ver usuario/nombre.mp4\nquit to exit: quit\nCliente: """)

	else:
		return input("""Loggearse: Login\nRegistrarse: Registro\nquit to exit: quit\nCliente: """)

opcion = ''
while True:
	if not ejecutando:
		opcion = dar_opciones()


	clientSocket.send(opcion.encode())
	if opcion.lower() == 'quit': 
		print('quitting...')
		clientSocket.close()
		break

	res = clientSocket.recv(1024).decode()
	if res[-1] == '¬':
		print('Servidor:',res[:-1])
		print('=========================', flush=True)
		ejecutando = False
		if 'Loggeado' in res:
			esta_loggeado = True

	elif opcion.lower() == 'subir':

		print('Servidor: {} (Seleccione)'.format(res))
		root = Tk()
		file_to_send = filedialog.askopenfilename()
		root.destroy()

		clientSocket.send(file_to_send.encode())
		
		print('Servidor:', clientSocket.recv(1024).decode())


		clientSocket.send(str(os.path.getsize(file_to_send)).encode())

		with open(file_to_send, 'rb') as f:
			clientSocket.sendfile(f, 0)


	else:
		opcion = input('Servidor: {} (Escriba): '.format(res))


