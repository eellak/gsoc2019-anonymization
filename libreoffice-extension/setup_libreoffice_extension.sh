#!/usr/bin/env bash
DIR="$(find / -name 'gsoc2019-anonymization' -printf '%h\n' -quit)/gsoc2019-anonymization/libreoffice-extension/";
SEARCH="$HOME/snap/libreoffice/144/.config/libreoffice/4/user"
DEST="$SEARCH/Scripts/python"
mkdir -p $DEST
cp $DIR/anonymizer_extension.py $DEST/ 
cp $DIR/anonymizer_extension.py /usr/lib/libreoffice/share/Scripts/python/;
echo 'Anonymizer extension was installed successfully ..'
