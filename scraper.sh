#!/bin/bash

DETTE_PUBLIQUE=$(sed -n 's/.*id="custom-counter-value-dette"[^>]*>\([^<]*\).*/\1/p' source.html | tr -d ' ')
DETTE_HABITANT=$(sed -n 's/.*id="custom-counter-value-habitant"[^>]*>\([^<]*\).*/\1/p' source.html | tr -d ' ')
DEFICIT_SECU=$(sed -n 's/.*id="custom-counter-value-dettesecu"[^>]*>\([^<]*\).*/\1/p' source.html | tr -d ' ')

DETTE_PUBLIQUE=${DETTE_PUBLIQUE:-"Non trouvé"}
DETTE_HABITANT=${DETTE_HABITANT:-"Non trouvé"}
DEFICIT_SECU=${DEFICIT_SECU:-"Non trouvé"}

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "$TIMESTAMP,$DETTE_PUBLIQUE,$DETTE_HABITANT,$DEFICIT_SECU" >> history.csv

echo "Dette publique: $DETTE_PUBLIQUE €" > data.txt
echo "Dette par habitant: $DETTE_HABITANT €" >> data.txt
echo "Déficit Sécurité sociale: $DEFICIT_SECU €" >> data.txt

echo "Données économiques récupérées :"
cat data.txt