#!/usr/bin/env sh
# Add current folder to PYTHONPATH
CURRENT_FOLDER=$(pwd)
SITE_PACKAGES_FOLDER="$(ls -d $(poetry env info -p)/lib/python*/site-packages/)project_dir.pth"
echo "$CURRENT_FOLDER" > "$SITE_PACKAGES_FOLDER"