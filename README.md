---
title: "Tuto de déploiement"
date: "2024-10-10"
author: "dp""
---

# Configuration pycharm pour auto-formatage des fichiers

## Installer black
$sudo apt install black

## Exécution manuelle
Dans le terminal sur la racine du projet :

user@ubuntu:~/PycharmProjects/bnote2/raspberrypi/bnote$ black .

## Configuration de l'exécution de black avant chaque enregistrement de fichier 
* Installer le plugin "file watcher" s'il n'est pas déjà installé (depuis "File>Settings>Plugins").
* Aller dans "File>Settings>Tools>File watchers" puis cliquer sur '+' et choisir "custom" dans la liste.
* Définir le lancement de black ainsi: 
  Name : Black Auto Format
  File Type : Python  
  Scope : Current File  
  Program : black  
  Arguments : \$FilePathRelativeToProjectRoot\$  
  Working directory : \$ProjectFileDir\$

Ainsi, avant chaque sauvegarde, black sera exécuté sur le fichier. 

# Réalisation d'un fichier d'update
Créée le mardi 08 octobre 2024


## Les docs 
3 documentations par langue :

### Pour le Français
* bnote - Manuel - 3.1.0 - FR  
* bnote - Manuel du développeur - 3.0.0 - FR  
* bnote - Musique - 3.0.0.txt  
* note de version 3.1.0.txt  

### Pour l'Anglais
* bnote - Manual - 3.1.0 - EN
* bnote - Developper manual - 3.0.0 - UK
* bnote - music - 3.0.0.txt
* what's new 3.1.0.txt

(à l'occasion, accorder les noms des manuels, ils doivent se terminer par EN plutôt que par UK)

## Etapes à réaliser sur la doc
### Sur les doc google docs
* Mettre à jour la date et la version de la doc sur la page de garde
* Reconstruire le sommaire
* Télécharger la doc au format: docx, odt, pdf, txt
* Mise à jour de note de version et de what's new

Les copier dans les sources dans le dossier doc à la racine du projet  
Copier aussi les version .txt dans le dossier raspberrypi/bnote/bnote/bnote-documents/documentation/FR et UK, dans ce dossier copier aussi la doc développeur .pdf changer en .pdf.ref

## Les fichiers de traduction
En ligne de commande se placer dans le dossier translation et exécuter le script update.sh

## Le code
* Nettoyer le code de tous les print inutiles dans une version release.
* Mette à jour la version en éditant pyproject.toml
* Placer dans le dossier whl les fichiers .zip dont vous avez besoin pour que l'exécutiuon du fichier libraries.txt se passe bien lors de l'installation de la version.

## Sur la pi
* Se connecter à la Pi et effacer le dossier develop/bnote puis reconstruire un environnement virtuel 3.0  
pi@raspberrypi:~ \$ cd develop  
pi@raspberrypi:~/develop \$ rm -r bnote  
pi@raspberrypi:~/develop \$tar -xvf bnote-3.0.0.tar.gz  
pi@raspberrypi:~/develop \$mv bnote-3.0.0 bnote  
pi@raspberrypi:~/develop \$cd bnote  
pi@raspberrypi:~/develop/bnote \$ sh ./setup.sh  
* Avec filezilla par exemple, ne garder que le venv de ~/home/develop/bnote, supprimer le reste  

* Effacer l'application puis placer l'application issue de pycharm, pour cela faire un git clone des sources, redéfinir un accès ssh sous pycharm puis uploader les sources.

* Se connecter avec un terminal ssh  
pi@raspberrypi:~ \$ cd develop/bnote/  
pi@raspberrypi:~/develop/bnote \$ sh ./generate.sh  
Récupérer le fichier bnote-3.1.0-py3-none-any.whl.zip avec filezilla  

---
# Réalisation d'une image à partir de la précédente :
Créer une sdcard avec pi imager.
## Sous ubuntu, placer la sdcard créer dans le lecteur:
* Modifier sdcard_version situé dans bootfs et dans rootfs/home/pi
* Renommer resize.sh en resize.sav.sh
* Mettre à jour le dossier .bnote/bnote-documents si nécessaire
* Effacer home/pi/bnote/venv et changer le fichier .whl par celui de la nouvelle version à installer.

## Démarrer la sd dans une raspberryPi hors bnote avec écran-clavier
### Connecter la pi à une borne wifi :
\$sudo nmcli dev wifi connect "Livebox-5340" password "KmK92WoVsDyc6ozSPq"

Pour connaitre l'adresse ip:  
\$ip addr  
Mettre la date à jour, pour le 09/10/2024 16:58  
sudo date 100916582024  
Regarder dans libraries.txt les librairies ou les opération à faire  
Dans le cas de la 3.1.0:  
sudo apt-get install poppler-utils -y -q  
sudo cp ar-ar-comp8.utb /usr/share/liblouis/tables/ar-ar-comp8.utb  
sudo cp hr-comp8.utb /usr/share/liblouis/tables/hr-comp8.utb  

Copier le fichier setup.sh à côté du fichier .whl dans ~/home/develop  

### Installation de l'environnement virtuel
pi@raspberrypi:~/bnote \$python -m venv venv  
pi@raspberrypi:~/bnote \$source venv/bin/activate  
Pour une installation via internet :  
pi@raspberrypi:~/bnote \$pip install bnote-3.1.0-py3-none-any.whl  
Pour une installation via le dossier whl :  
sh ./setup.sh  
pi@raspberrypi:~/bnote \$deactivate  

Désintaller le connexion wifi  
pi@raspberrypi:~ \$ nmcli con delete "Livebox-5340"  

### Replacer la carte SD dans le lecteur du PC
* Effacer les fichiers:  
Dans /home/pi : .bash_history  
Dans /home/pi/.bnote : my_agenda.csv, recent_file.trr et settings.txt  
Dans /home/pi/.bnote/bnote-documents : radio_list.xml  
Renommer resize_1.sh en resize.sh  

* Créer une image de la sdcard avec l'utilitaire disque ubuntu (2024-04-30_bnote_3.0.0b10.img)  
* Faire fdisk pour voir la taille de la partition redimensionnée:  
$ fdisk -l 2022-04-20_bnote_2.0.0-rc.1.img  
Disque 2022-04-20_bnote_2.0.0-rc.1.img : 7,44 GiB, 7990149120 octets, 15605760 secteurs  
Unités : secteur de 1 × 512 = 512 octets  
Taille de secteur (logique / physique) : 512 octets / 512 octets  
taille d'E/S (minimale / optimale) : 512 octets / 512 octets  
Type d'étiquette de disque : dos
Identifiant de disque : 0x6449d5aa  
Périphérique                     Amorçage  Début      Fin Secteurs Taille Id Type  
2022-04-20_bnote_2.0.0-rc.1.img1            8192   532479   524288   256M  c W95  
2022-04-20_bnote_2.0.0-rc.1.img2          532480 11018239 10485760     5G 83 Linu  

* Réduite le fichier image  
\$ truncate --size=$[(11018239+1)*512] 2022-04-20_bnote_2.0.0-rc.1.img   

* Pour la compresser et créer un fichier mon_image.img.xz :  
\$xz -z mon_image.img

