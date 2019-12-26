#!/usr/bin/env python

import socket # Para usar sockets TCP
import sys # Para admitir argumentos 
import argparse as ap # Para facilitar el parseo de dichos argumentos, le damos alias ap
import os

def getRequest(data):
    msj = ""
    # Converting Bytes to String
    for x in dat:
        msj += x
    # Split String to Array 
    words = msj.split("\n")
    return words

if __name__ == '__main__':
    
    parser = ap.ArgumentParser(prog=sys.argv[0], description='Un servidor no concurrente TCP de hola mundo') # Definimos el parseador. Por convenio, los argumentos opcionales se encabezan con '--'
    parser.add_argument('--ip', help='IP del servidor', default='0.0.0.0')
    parser.add_argument('--puerto', type=int, help='Puerto TCP de salida', default=5005, choices=range(1024,65535), metavar='1024-65535') 
    parser.add_argument('--tam_buf', type=int, help='Longitud del buffer interno', default=50) # Buffer corto para que responda antes
    
    # Parseamos los argumentos de acuerdo al parser
    args = parser.parse_args(sys.argv[1:])

    # Inicializacmos el servidor: empezamos a esperar conexiones. Para más información consulte: https://wiki.python.org/moin/HowTo/Sockets
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 1. Declaramos el socket
    s.bind((args.ip, args.puerto)) # 2. Lo ligamos a una IP y puerto
    s.listen(1) # 3. Podemos encolar hasta una solicitud
    shutdown = False # Variable flag que controla si queremos finalizar el servidor. En el caso de que reciba 'shutdown' terminará su ejecución.
    
    while not shutdown:
        conn, addr = s.accept()   # 4. Aceptamos cliente. Desempaquetamos la tupla de retorno en conexión y dirección del cliente
        print('Aceptado un cliente con (IP, puerto):', addr)
        
        try:
            data = conn.recv(args.tam_buf)
            
            if not data: # Si no se reciben datos --> se ha desconectado
                break
            
            dat = data.decode('ascii', 'ignore')
            user_request = getRequest(data)

            # DOWNLOAD FILE 
            if user_request[0] == "--DOWNLOAD_FILE":
                os.system('cls')
                print("# # # Download File # # #")
                filename = user_request[1]
                print(filename)
                if os.path.exists(filename):
                    print("File exists")
                    file_size = os.path.getsize(filename)
                    print(file_size)
                    f = open(filename,'rb')
                    l = f.read(1024)
                    while(l):
                        #conn.send(l)
                        print('Sent')
                        l = f.read(1024)
                    f.close

                    #with open(filename,'wb') as f: ESTO VA EN EL CLIENTE
                        #print('file opened')


                else:
                    print("Error")

            conn.send(data)
            conn.close() 
            
            if data == b'shutdown':
                shutdown = True
        except ConnectionResetError:
            print('Error: conexión cerrada en el otro extremo')
    print('Cerrando el servidor')

    
