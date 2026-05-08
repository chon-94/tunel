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