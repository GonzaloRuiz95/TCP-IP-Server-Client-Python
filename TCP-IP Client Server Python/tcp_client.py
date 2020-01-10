#! 
import socket # Para usar sockets TCP
import sys # Para admitir argumentos por línea de comandos
import argparse as ap # Para facilitar el parseo de dichos argumentos. Usamos alias ap
import os
import PySimpleGUI as sg

largest_frame = 100000

if __name__ == '__main__':

    # Defining parser. Por convenio, los argumentos opcionales se encabezan con '--'
    # More info on https://docs.python.org/3/howto/argparse.html
    parser = ap.ArgumentParser(prog=sys.argv[0], description='Un cliente TCP de hola mundo')
    parser.add_argument('--ip', help='IP del servidor', default="127.0.0.1") # Por defecto usamos localhost
    # Los puertos por defecto están en el rango 0-1023. Podemos usar puertos a partir de ahí
    parser.add_argument('--puerto', type=int, help='Puerto TCP de salida [1024-65535]', default=5004, choices=range(1024,65535), metavar='PUERTO (1024-65535)') 
    parser.add_argument('--tam_buf',  type=int, help='Longitud del buffer interno', default=4000)
    parser.add_argument('--mensaje', help='Mensaje a transmitir', default='Hola mundo')
    parser.add_argument('--DOWNLOAD_FILE')
    parser.add_argument('--LIST_FILES', action='store_true')
    parser.add_argument('--DELETE_FILE')
    parser.add_argument('--MOVE_FILE', nargs='+') # nargs accepts 1 or more args

    args = parser.parse_args()
    client_args = sys.argv[1:4]

    # Defining socket and trying to connect to the server
    # First define socket (SOCK_STREAM is TCP) it uses inet directions (AF_INET)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((args.ip, args.puerto)) # Intentamos conectarnos al servidor en el puerto especificado
    # Trying to connect to the server in the specific port

    sg.theme('TealMono')	# Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('Select option')],
            [sg.Combo(['List files', 'Download File', 'Move', 'Delete', 'Upload'], 'Option')],
            [sg.Text('List option does not need a filename')],
            [sg.Text('Enter filename 1 (Download Delete or Move)'), sg.InputText()],
            [sg.Text('Enter filename 2 (Only for move option)'), sg.InputText()],
            [sg.Button('About')],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

    window = sg.Window('TCP/IP Client', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):	# if user closes window or clicks cancel
            break 
        if event == "About":
            sg.Popup("A program by Gonzalo Ruiz and Arturo López:\n ")

        ui_option = values[0]
        # List Option
        if ui_option == "List files":
            print("Listar")
            list_args = "--LIST_FILES"
            s.send(list_args.encode('ascii','ignore'))
            data = s.recv(1024)
            reponse = data.decode('ascii','ignore')
            print(reponse)
            #window = sg.Window('Get filename example', layout2)
            sg.Popup("Files :", reponse)

        # Download Option
        elif ui_option == "Download File":
            filename = 'copy-' + values[1]
            val_list = ["--DOWNLOAD_FILE",values[1]]
            download = '\n'.join(val_list)
            s.send(download.encode('ascii','ignore'))
            data = s.recv(1024)
            reponse = data.decode('ascii','ignore')
            if reponse == "ERROR":
                print("File does not exists")
                sg.Popup("File: " + filename + " does not exists")      
            else:
                size = int(reponse)
                if size < largest_frame:
                    s.send("ACK_DOWNLOAD".encode('ascii','ignore'))
                    f = open(filename,'wb')
                    l = s.recv(1024)
                    while (l):
                        f.write(l)
                        l = s.recv(1024)
                    f.close()
                    sg.Popup("A copy of " + filename + " was created on client side")      

        # Move Option
        elif ui_option == "Move":
            list_args = "--MOVE_FILE"
            val_list = ["--MOVE_FILE",values[1], values[2]]
            move = '\n'.join(val_list)
            s.send(move.encode('ascii','ignore'))
            data = s.recv(1024)
            reponse = data.decode('ascii','ignore')
            print(reponse)
            sg.Popup(reponse + ": " + values[1] + " was renamed to " + values[2])
    
        # Delete Option
        elif ui_option == "Delete":
            val_list = ["--DELETE_FILE",values[1], values[2]]
            delete = '\n'.join(val_list)
            s.send(delete.encode('ascii','ignore'))
            data = s.recv(1024)
            reponse = data.decode('ascii','ignore')
            print(reponse)
            if reponse == "SUCCESS":
                sg.Popup(reponse + ": " + values[1] + " was deleted")
            else:
                sg.Popup(reponse + ": cant delete " + values[1])

        elif ui_option == "Upload":
            # (1) UPLOAD_FILE <nombre_fichero>
            val_list = ["--UPLOAD_FILE", values[1], values[2]]
            filename = values[1]
            upload = '\n'.join(val_list)
            s.send(upload.encode('ascii','ignore'))
            data = s.recv(1024)
            reponse = data.decode('ascii','ignore')
            print(reponse)
            # (3) LONGITUD
            filesize = os.path.getsize(values[1])
            s.send(bytes(str(filesize), 'utf8'))

            data = s.recv(1024)
            reponse = data.decode('ascii','ignore')

            # Upload option
            if reponse == "UPLOAD_ACK":
                print("ACK Recibido. Enviando Contenido Del Fichero")
                f = open(filename,'rb')
                l = f.read(1024)
                while (l):
                    s.send(l)
                    l = f.read(1024)
                f.close()
                sg.Popup("SUCCES: a copy of " + filename + " was created on server side")
            else:
                print("ERROR")
               
    window.close()
    s.close()

        