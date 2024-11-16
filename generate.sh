#!/bin/bash

# Check if 'archive' argument is passed
ARCHIVE=false
for arg in "$@"
do
  if [ "$arg" == "archive" ]; then
    ARCHIVE=true
    break
  fi
done

if [ -d "dist" ]; then
  rm -r dist/*
fi
if [ -d "build" ]; then
  rm -r build/*
fi
venv/bin/python3 -m build --wheel --sdist
WHL_FILE_PATH=$(ls dist/*.whl)
TAR_GZ_FILE_PATH=$(ls dist/*.tar.gz)
TAR_FILE_PATH=$(echo "$TAR_GZ_FILE_PATH" | sed 's/\.gz$//')
BNOTE_FOLDER_NAME=$(basename "$TAR_GZ_FILE_PATH" .tar.gz)
echo "Found .whl path: $WHL_FILE_PATH"
echo "Found .tar.gz path: $TAR_GZ_FILE_PATH"
echo "Found .tar path: $TAR_FILE_PATH"
echo "Found bnote name: $BNOTE_FOLDER_NAME"
WHL_FILE=$(basename "$WHL_FILE_PATH")
echo "Found .whl file: $WHL_FILE"
cp "$WHL_FILE_PATH" ./"$WHL_FILE"
zip -r "$WHL_FILE".zip "$WHL_FILE" libraries.txt __main__.py whl

if [ "$ARCHIVE" = true ]; then
  gunzip "$TAR_GZ_FILE_PATH"
  echo "tar --append --file=$TAR_FILE_PATH -C generate.sh $BNOTE_FOLDER_NAME/generate.sh"
  tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," generate.sh
  tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," setup.sh
  tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," libraries.txt
  tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," __main__.py
  tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," __main_debug__.py
  tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," whl/*
  gzip "$TAR_FILE_PATH"
fi