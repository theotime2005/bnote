#!/bin/bash

# Vérifier si un argument est passé
if [ -z "$1" ]; then
  echo "Usage: $0 <nom-du-fichier>"
  exit 1
fi

python3 -m venv venv
venv/bin/pip install  --no-index --find-links ~/whl ~/bnote/"$1"-py3-none-any.whl
