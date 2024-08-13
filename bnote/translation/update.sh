#!/bin/bash
# Ce script met à jour toutes les traduction à partir du fichier .pot lui-même mis à jour.
# Ce script se lance depuis un terminal pointant le dossier dans lequel il se trouve (sh ./update.sh)

# Chemin vers le dossier contenant vos fichiers .po et .pot
PO_FILES_PATH="."
# Chemin vers le fichier .pot
POT_FILE="bnote.pot"

# Mise à jour du fichier .pot
find .. -name *.py | xargs xgettext -o "$POT_FILE" --language=Python --from-code=UTF-8
#xgettext -o "$POT_FILE" fichier1.c fichier2.c
# Boucle sur chaque fichier .po
for po_file in $PO_FILES_PATH/*.po; do
echo "Mise à jour du fichier $po_file"
msgmerge -U "$po_file" "$POT_FILE"
# Génère le fichier .mo correspondant
msgfmt "$po_file" -o "${po_file%.po}.mo"
done

echo "Mise à jour terminée."
