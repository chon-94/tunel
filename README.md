# Bufferes

puedo mostar 1k o 1mb  todo esta en colocar 1024 o 1024000, al parecer 1mb es mejor, mas funcional, menos viajes menos rastros, mas informacion de una


# el beacon
 no me refiero a esos embutidos me refiro a que  los resultado ultimos se mesclan con el output proximo una locura, para ello se debe de hacer esta cosita
 sustituir el codigo
 diciendo primero recimo la conoexion 1k  luego la muestro ... asi la ordecna dice
         # ← ✅ AGREGAR ESTO: Recibir el conexion ANTES del loop
         
        conexion = self.connection.recv(1024)
        print(conexion.decode('utf-8', errors='ignore'))
        #self.connection, address = listener.accept()
        #print("[+] Tenemos una conexion de " + str(address))

no recuerdo que estab haciendo allaa arriba 

## Librerias

hay muchas librerias, una de las ultimas que acabo de conocer es la ssl
esta al parece hace que mi codigo sea mas dificil de detectar, es como
añadirle una capa extra de seguridad es cosa de probar

🔧 PASO 1: GENERAR CERTIFICADOS (5 MINUTOS):

# En Manjaro, en la carpeta del proyecto:
$ cd ~/Documentos/GitHub/tunel/tunelTCP/

# Generar certificados:
$ openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=192.168.1.33"

# Verificar:
$ ls -lh *.pem
# cert.pem  key.pem

# Permisos seguros:
$ chmod 600 key.pem
$ chmod 644 cert.pem

# Agregar a .gitignore (IMPORTANTE):
$ echo "*.pem" >> .gitignore