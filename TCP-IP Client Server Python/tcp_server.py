#!/usr/bin/env python

import socket # Para usar sockets TCP
import sys # Para admitir argumentos 
import argparse as ap # Para facilitar el parseo de dichos argumentos, le damos alias ap
import os

# LFS (Largest frame that can be received)
largest_frame = 100000

def getRequest(data):
    msj = ""
    # Converting Bytes to String
    for x in dat:
        msj += x
    # Split String to Array 
    req = msj.split("\n")
    return req

if __name__ == '__main__':
    
    parser = ap.ArgumentParser(prog=sys.argv[0], description='Un servidor no concurrente TCP de hola mundo') # Definimos el parseador. Por convenio, los argumentos opcionales se encabezan con '--'
    parser.add_argument('--ip', help='IP del servidor', default='0.0.0.0')
    parser.add_argument('--puerto', type=int, help='Puerto TCP de salida', default=5004, choices=range(1024,65535), metavar='1024-65535') 
    parser.add_argument('--tam_buf', type=int, help='Longitud del buffer interno', default=50) # Buffer corto para que responda antes
    
    # Parse arguments
    args = parser.parse_args(sys.argv[1:])

    # Inicialize server: waiting conn. more info: https://wiki.python.org/moin/HowTo/Sockets
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 1. Declaramos el socket
    s.bind((args.ip, args.puerto)) # 2. ip and port associate
    s.listen(1) # 3. Queue till one request
    shutdown = False # Var flag controls server communication. If server receives'shutdown' the execution concludes.
    
    while not shutdown:
        conn, addr = s.accept()   # 4. Aceptamos cliente. Desempaquetamos la tupla de retorno en conexión y dirección del cliente
        print('Aceptado un cliente con (IP, puerto):', addr)
        try:

            data = conn.recv(args.tam_buf)
            
            if not data: # Si no se reciben datos --> se ha desconectado
                break
            
            dat = data.decode('ascii', 'ignore')
            user_request = getRequest(data)

            if user_request[0] == "--LIST_FILES":
                os.system('CLS')
                print("# # # List files # # #")
                files = "\n".join(os.listdir(os.path.expanduser('.')))
                print(files)
                conn.send(files.encode('ascii','ignore'))

            # Download file 
            elif user_request[0] == "--DOWNLOAD_FILE":
                os.system('cls')
                filename = user_request[1]
                if os.path.exists(filename):
                    print("File exists")
                    file_size = os.path.getsize(filename)
                    conn.send(bytes(str(file_size), 'utf8'))
                    data = conn.recv(1024)
                    reponse = data.decode('ascii','ignore')
                    if reponse == "ACK_DOWNLOAD":
                        f = open(filename,'rb')
                        l = f.read(1024)
                        while (l):
                            conn.send(l)
                            l = f.read(1024)
                        f.close()
                else:
                    print("File does not exists")
                    conn.send("ERROR".encode('ascii','ignore'))

            
            # Delete file
            elif user_request[0] == "--DELETE_FILE":
                os.system('CLS')
                print("# # # Delete File # # #")
                filename = user_request[1]
                if os.path.exists(filename) and filename != "tcp_server.py" and filename != "tcp_client.py":
                    print("File " + filename + " was removed")
                    os.remove(filename)
                    reponse = "SUCCESS"
                else:
                    print("No existe")
                    reponse = "ERROR"
            
                conn.send(reponse.encode('ascii','ignore'))

            elif user_request[0] == "--MOVE_FILE":
                os.system('CLS')
                print("# # # Move File # # #")
                filename1 = user_request[1]
                filename2 = user_request[2]

                if os.path.exists(filename1) and not os.path.exists(filename2):
                    os.rename(filename1,filename2)
                    print("File was renamed")
                    reponse = "SUCCES"
                else:
                    print("Error")
                    reponse = "ERROR"

                conn.send(reponse.encode('ascii','ignore'))
            
            elif user_request[0] == "--UPLOAD_FILE":
                os.system('CLS')
                print("# # # UPLOAD FILE # # #")
                # (2) UPLOAD_ACK
                reponse = "UPLOAD_ACK"
                conn.send(reponse.encode('ascii','ignore'))
                reponse = conn.recv(1024)
                size = reponse.decode('ascii','ignore')
                print(size)
                tam = int(size)
                # (4) UPLOAD_ACK
                if tam < largest_frame:
                    reponse = "UPLOAD_ACK"
                    conn.send(reponse.encode('ascii','ignore'))
                    f = open("Descarga.txt",'wb')
                    l = conn.recv(1024)
                    while (l):
                        f.write(l)
                        l = conn.recv(1024)
                    f.close()
                else:
                    conn.send("ERROR".encode('ascii','ignore'))
                
            else:
                print("Error")
                reponse = "INVALID COMMAND"
                conn.send(reponse.encode('ascii','ignore'))

            conn.close() 
            
            if data == b'shutdown':
                shutdown = True
        except ConnectionResetError:
            print('Error: conexión cerrada en el otro extremo')
    print('Cerrando el servidor')

    
