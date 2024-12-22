#!/bin/bash
# Ce script met à jour toutes les traductions à partir du fichier .pot lui-même mis à jour.
# Ce script se lance depuis un terminal pointant le dossier dans lequel il se trouve (sh ./update.sh)

# Chemin vers le dossier contenant vos fichiers .po et .pot
PO_FILES_PATH="."
# Chemin vers le fichier .pot
POT_FILE="bnote.pot"

# Si appelé avec l'argument "mo", ne faire que la compilation des fichiers .mo
if [ "$1" == "mo" ]; then
    echo "Compilation des fichiers .mo uniquement."
    for po_file in $PO_FILES_PATH/*.po; do
        echo "Compilation de $po_file vers ${po_file%.po}.mo"
        msgfmt "$po_file" -o "${po_file%.po}.mo"
    done
    echo "Compilation terminée."
    exit 0
fi

# Mise à jour du fichier .pot
find .. -name "*.py" | xargs xgettext -o "$POT_FILE" --language=Python --from-code=UTF-8

# Boucle sur chaque fichier .po
for po_file in $PO_FILES_PATH/*.po; do
    echo "Mise à jour du fichier $po_file"
    msgmerge -U "$po_file" "$POT_FILE"
    # Génère le fichier .mo correspondant
    msgfmt "$po_file" -o "${po_file%.po}.mo"
done

echo "Mise à jour terminée."
