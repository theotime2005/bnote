#!/bin/bash

# Function to display a formatted log message
log() {
  echo -e "\e[1;34m#####################################################"
  echo -e "# $1"
  echo -e "######################################################\e[0m"
}

# Function to display a success message
success() {
  echo -e "\e[1;32m✔️  $1\e[0m"
}

# Function to display an error message and exit
error() {
  echo -e "\e[1;31m❌  $1\e[0m"
  exit 1
}

# Function to display an informational message
info() {
  echo -e "\e[1;33m🔹 $1\e[0m"
}

log "STEP 1: Cleaning up previous build artifacts"

# Remove old build artifacts
if [ -d "dist" ]; then
  rm -r dist/*
  success "Removed old 'dist' files."
fi

if [ -d "build" ]; then
  rm -r build/*
  success "Removed old 'build' files."
fi

log "STEP 2: Generating build artifacts"

# Create a new wheel and source distribution
if venv/bin/python3 -m build --wheel --sdist; then
  success "Build artifacts created successfully."
else
  error "Failed to generate build artifacts."
fi

# Retrieve file paths
WHL_FILE_PATH=$(ls dist/*.whl)
TAR_GZ_FILE_PATH=$(ls dist/*.tar.gz)
TAR_FILE_PATH=$(echo "$TAR_GZ_FILE_PATH" | sed 's/\.gz$//')
BNOTE_FOLDER_NAME=$(basename "$TAR_GZ_FILE_PATH" .tar.gz)
WHL_FILE=$(basename "$WHL_FILE_PATH")

# Display found paths
log "STEP 3: Verifying build files"
info "Found .whl path: $WHL_FILE_PATH"
info "Found .tar.gz path: $TAR_GZ_FILE_PATH"
info "Found .tar path: $TAR_FILE_PATH"
info "Found bnote name: $BNOTE_FOLDER_NAME"
info "Found .whl file: $WHL_FILE"

# Copy wheel file
log "STEP 4: Copying .whl file"
if cp "$WHL_FILE_PATH" ./"$WHL_FILE"; then
  success "Copied $WHL_FILE successfully."
else
  error "Failed to copy $WHL_FILE."
fi

# Create ZIP file
log "STEP 5: Creating ZIP package"
WHL_ZIP_PATH="$WHL_FILE.zip"
if zip -r "$WHL_ZIP_PATH" "$WHL_FILE" libraries.txt __main__.py whl; then
  success "ZIP package created successfully: $WHL_ZIP_PATH"
else
  error "Failed to create ZIP package."
fi

# Decompress the tar.gz file
log "STEP 6: Decompressing TAR.GZ file"
if gunzip "$TAR_GZ_FILE_PATH"; then
  success "Decompressed TAR.GZ successfully."
else
  error "Failed to decompress TAR.GZ file."
fi

# Append files to the tar archive
log "STEP 7: Appending files to the TAR archive"
tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," generate.sh
tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," setup.sh
tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," libraries.txt
tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," __main__.py
tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," __main_debug__.py
tar --append --file="$TAR_FILE_PATH" --transform "s,^,$BNOTE_FOLDER_NAME/," whl/*

success "Files successfully added to the TAR archive."

# Compress back to tar.gz
log "STEP 8: Recompressing the TAR file"
FINAL_TAR_GZ_PATH="$TAR_FILE_PATH.gz"
if gzip "$TAR_FILE_PATH"; then
  success "Recompressed TAR.GZ successfully: $FINAL_TAR_GZ_PATH"
else
  error "Failed to recompress TAR.GZ file."
fi

# Final log output with generated file paths
log "🎉 BUILD PROCESS COMPLETED SUCCESSFULLY!"
echo -e "\e[1;36m#####################################################"
echo -e "# Build artifacts generated successfully!"
echo -e "# - TAR.GZ file path: $FINAL_TAR_GZ_PATH"
echo -e "# - WHL ZIP file path: $WHL_ZIP_PATH"
echo -e "#####################################################\e[0m"
