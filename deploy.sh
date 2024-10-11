#!/bin/bash

# Vérifier si un argument est passé
if [ -z "$1" ]; then
  echo "Usage: $0 <nom-du-fichier-tar.gz>"
  exit 1
fi

# Extraire le fichier tar
tar -xvf "$1"

# Récupérer le nom du dossier (sans l'extension .tar.gz)
folder_name=$(basename "$1" .tar.gz)

# Renommer le dossier extrait
mv "$folder_name" bnote

# Aller dans le dossier bnote
cd bnote || exit

# Exécuter le script setup.sh
sh ./setup.sh "$folder_name"
