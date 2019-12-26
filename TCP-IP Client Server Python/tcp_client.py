#! 
import socket # Para usar sockets TCP
import sys # Para admitir argumentos por línea de comandos
import argparse as ap # Para facilitar el parseo de dichos argumentos. Usamos alias ap

if __name__ == '__main__':
    # Definimos el parseador. Por convenio, los argumentos opcionales se encabezan con '--'
    # Para más información, consulte https://docs.python.org/3/howto/argparse.html
    parser = ap.ArgumentParser(prog=sys.argv[0], description='Un cliente TCP de hola mundo')
    parser.add_argument('--ip', help='IP del servidor', default="127.0.0.1") # Por defecto usamos localhost
    # Los puertos por defecto están en el rango 0-1023. Podemos usar puertos a partir de ahí
    parser.add_argument('--puerto', type=int, help='Puerto TCP de salida [1024-65535]', default=5005, choices=range(1024,65535), metavar='PUERTO (1024-65535)') 
    parser.add_argument('--tam_buf',  type=int, help='Longitud del buffer interno', default=4000)
    parser.add_argument('--mensaje', help='Mensaje a transmitir', default='Hola mundo')
    parser.add_argument('--DOWNLOAD_FILE')
    
    # Parseamos los argumentos de acuerdo al parser
    args = parser.parse_args()
    
    download_args = sys.argv[1:3]
    print(sys.argv[1:3])
    
    # Definimos socket e intentamos conectarnos al servidor.
    # Primero definimos el socket (SOCK_STREAM es TCP) usa direcciones de internet (AF_INET)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((args.ip, args.puerto)) # Intentamos conectarnos al servidor en el puerto especificado
    
    # Una vez conectados, debemos definir el protocolo del programa. 
    # En este caso simple, el cliente manda un mensaje al que el servidor hace ECHO.

    # Download File Option
    download = '\n'.join(download_args)
    print(download)
    s.send(download.encode('ascii','ignore'))

    mensaje = ''.join(args.mensaje) # Concatenamos el mensaje
    
    print ("Mandando el mensaje:", mensaje, 'a la IP:', args.ip)
    
    # Mandamos el dato en codificación ASCII (por defecto en Python3 las cadenas se codifican en UTF-8)
    s.send(mensaje.encode("ascii", "ignore")) 
        
    #data = s.recv(args.tam_buf) # Esperamos el eco
    
    # Una vez acabado el intercambio de datos, debemos cerrar el socket
    
    



    s.close() # Cerramos el socket

    #print ("Datos recibidos:", data.decode("ascii"))
