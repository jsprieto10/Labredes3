from threading import Thread
from pymongo import MongoClient
import os
from helper import find_free_port
import serverVideo

class Session(Thread):

	def __init__(self, sock, addr):
		Thread.__init__(self)
		self.sock = sock
		self.addr = addr
		self.is_logged = False
		self.username = None

	def run(self):

		while True:
			order = self.sock.recv(1024).decode().upper()

			if order == 'QUIT':
				print('client: {} is requesting to close connection')
				self.sock.close()
				print('connection close')
				break

			elif order == 'REGISTRO':
			 	self.create_user()

			elif order == 'LOGIN':
			 	self.search_login()

			elif order == 'SUBIR':
				self.upload_video()

			elif order == 'VER':
				self.send_video()

			else:
			 	self.sock.send('Repetir opcion por favor'.encode())


	def create_user(self):

		self.sock.send('ingrese su usuario'.encode())
		user = self.sock.recv(1024).decode()

		print(user, 'usuario')
		self.sock.send('ingrese su clave'.encode())
		password = self.sock.recv(1024).decode()

		db = MongoClient().redes
		try:
			db.usuarios.insert_one({'user': user, 'password': password})
			os.mkdir(user)
			self.sock.send('creado correctamente¬'.encode())
		except:
			self.sock.send('error al crear el usuario¬'.encode())


	def search_login(self):

		self.sock.send('ingrese su usuario'.encode())
		user = self.sock.recv(1024).decode()

		self.sock.send('ingrese su clave'.encode())
		password = self.sock.recv(1024).decode()

		db = MongoClient().redes
		usr = db.usuarios.find_one({'user': user, 'password': password})

		msj = 'No se ha podido encontrar el usuario con nombre {} y clave {}¬'.format(user, password)

		if usr:
			self.is_logged = True
			self.username = user
			msj = 'Loggeado correctamente¬'
		
		self.sock.send(msj.encode())


	def upload_video(self):

		self.sock.send('Escoja la ruta del video'.encode())

		CHUNK_SIZE = 1024*8
		file_name = self.sock.recv(1024).decode().split('/')[-1]
		self.sock.send('Esta listo para recibir'.encode())

		size = int(self.sock.recv(1024).decode())//CHUNK_SIZE

		with open(os.path.join(self.username, file_name), 'wb') as f:
			i=0
			while i <= size:
				chunk = self.sock.recv(CHUNK_SIZE)
				f.write(chunk)
				i+=1
			f.close()


		print('termino')
		self.sock.send('Video subido correctamente¬'.encode())


	def send_video(self):


		self.sock.send("ruta del video".encode())

		p = find_free_port()


		self.sock.send(str(p).encode())
		serverVideo.main(p)
		
		print(self.sock.recv(1024).decode())

		self.sock.send("Eeyy termine¬".encode())


