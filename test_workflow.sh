#!/bin/bash

# Script de test pour simuler le workflow GitHub Actions

echo "🧪 Test du workflow GitHub Actions"

# Simuler les variables d'environnement
export GITHUB_REF="refs/tags/v3.1.2005a14"
export GITHUB_REF_NAME="v3.1.2005a14"

echo "📝 Variables d'environnement:"
echo "GITHUB_REF: $GITHUB_REF"
echo "GITHUB_REF_NAME: $GITHUB_REF_NAME"

# Test de l'extraction de version
echo "🔍 Test d'extraction de version:"
ref_name="${GITHUB_REF_NAME#v}"
echo "Version extraite: $ref_name"

# Test de détection de pré-release
echo "🏷️ Test de détection de pré-release:"
if [[ "${GITHUB_REF##*/}" == *"beta"* || "${GITHUB_REF##*/}" == *"alpha"* || "${GITHUB_REF##*/}" == *"rc"* || "${GITHUB_REF##*/}" == *"a"* || "${GITHUB_REF##*/}" == *"b"* || "${GITHUB_REF##*/}" == *"r"* ]]; then
    prerelease="true"
else
    prerelease="false"
fi
echo "Pré-release: $prerelease"

# Test de nom de fichier attendu
expected_file="bnote-${ref_name}-py3-none-any.whl.zip"
echo "📦 Fichier attendu: $expected_file"

# Vérifier si le fichier existe
if [ -f "$expected_file" ]; then
    echo "✅ Fichier trouvé: $expected_file"
else
    echo "❌ Fichier manquant: $expected_file"
    echo "📁 Fichiers présents:"
    ls -la bnote*.whl.zip 2>/dev/null || echo "Aucun fichier .whl.zip trouvé"
fi

echo "🎯 Test terminé"
