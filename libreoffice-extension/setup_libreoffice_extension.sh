#!/usr/bin/env bash
DIR="$(find / -name 'gsoc2019-anonymization' -printf '%h\n' -quit)/gsoc2019-anonymization/libreoffice-extension/";
cp $DIR/anonymizer_extension.py /usr/lib/libreoffice/share/Scripts/python/;
echo 'Anonymizer extension was installed successfully ..'
