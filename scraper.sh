#!/bin/bash

HTML=$(cat source.html)

DETTE_PUBLIQUE=$(echo "$HTML" | grep -oP '(?<=id="custom-counter-value-dette">)[^<]+' | head -1)
DETTE_HABITANT=$(echo "$HTML" | grep -oP '(?<=id="custom-counter-value-habitant">)[^<]+')
DEFICIT_SECU=$(echo "$HTML" | grep -oP '(?<=id="custom-counter-value-dettesecu">)[^<]+')

echo "Données économiques récupérées :"
echo "➜ Dette publique : ${DETTE_PUBLIQUE:-Non trouvé} €"
echo "➜ Dette par habitant : ${DETTE_HABITANT:-Non trouvé} €"
echo "➜ Déficit Sécurité sociale : ${DEFICIT_SECU:-Non trouvé} €"