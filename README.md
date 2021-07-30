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

## Fonctionnalité

Serveur peut gérer plusieur clients en même temps.

Fonction Reverse Shell.

Fonction Keylogger.

Fonction Persistance.

Stocke les informations recupérer des fichiers .json

## Utilisation
Lancer d'abort le serveur :
```cmd
python server.py
```
Génerer un payload : (pas encore fait)

Lancer le client :
```cmd
python client.py
```

__Disclaimer__: Le payload est au format.py, utiliser un outils comme cx_freeze pour le transformer en .exe.

### Commande du server

help --- Afficher le menu d'aide.

shell <"id du client"> --- Ouvre un Reverse Shell sur la machine.

clients --- Afficher les information des machines clients.

Dans le Shell :

keylogger <"run/status/stop"> --- Run lance un keylogger sur la machine, status renvoi les données enregistrer, stop arete le keylogger.

persistance <"startup/reg/powershell"> --- Startup active la persistance sur la machine via le dossier startup de windows, reg active la persistance via clé de registre windows(pas encore fait), powwershell active la persistance via powershell(pas encore fait).