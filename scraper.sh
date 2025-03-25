#!/bin/bash

clean_value() {
    echo "$1" | tr -d '\r\n €' | tr ',' '.' | xargs
}

DETTE_PUBLIQUE=$(clean_value "$(sed -n 's/.*id="custom-counter-value-dette"[^>]*>\([^<]*\).*/\1/p' source.html)")
DETTE_HABITANT=$(clean_value "$(sed -n 's/.*id="custom-counter-value-habitant"[^>]*>\([^<]*\).*/\1/p' source.html)")
DEFICIT_SECU=$(clean_value "$(sed -n 's/.*id="custom-counter-value-dettesecu"[^>]*>\([^<]*\).*/\1/p' source.html)")

DETTE_PIB_INT=$(grep -A1 'data-to-value="115"' source.html | sed -n 's/.*data-to-value="\([^"]*\)".*/\1/p')
DETTE_PIB_SUFFIX=$(grep -A1 'data-to-value="115"' source.html | grep 'suffix' | sed -n 's/.*>\([^<]*\).*/\1/p')
DETTE_PIB=$(clean_value "$DETTE_PIB_INT$DETTE_PIB_SUFFIX")

DEFICIT_BUDGET=$(clean_value "$(sed -n 's/.*id="custom-counter-value-deficitmobile"[^>]*>\([^<]*\).*/\1/p' source.html)")

DEFICIT_2024_INT=$(grep -A1 'data-to-value="156"' source.html | sed -n 's/.*data-to-value="\([^"]*\)".*/\1/p')
DEFICIT_2024_SUFFIX=$(grep -A1 'data-to-value="156"' source.html | grep 'suffix' | sed -n 's/.*>\([^<]*\).*/\1/p')
DEFICIT_2024=$(clean_value "$DEFICIT_2024_INT$DEFICIT_2024_SUFFIX")

DETTE_PUBLIQUE=${DETTE_PUBLIQUE:-"NA"}
DETTE_HABITANT=${DETTE_HABITANT:-"NA"}
DEFICIT_SECU=${DEFICIT_SECU:-"NA"}
DETTE_PIB=${DETTE_PIB:-"NA"}
DEFICIT_BUDGET=${DEFICIT_BUDGET:-"NA"}
DEFICIT_2024=${DEFICIT_2024:-"NA"}

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "$TIMESTAMP,$DETTE_PUBLIQUE,$DETTE_HABITANT,$DEFICIT_SECU,$DETTE_PIB,$DEFICIT_BUDGET,$DEFICIT_2024" >> history.csv

{
  echo "Dette publique : $DETTE_PUBLIQUE €"
  echo "Dette par habitant : $DETTE_HABITANT €"
  echo "Déficit sécurité sociale : $DEFICIT_SECU €"
  echo "Dette publique / PIB : $DETTE_PIB %"
  echo "Déficit du budget de l'État : $DEFICIT_BUDGET €"
  echo "Déficit budgétaire prévu en 2024 : $DEFICIT_2024"
} > data.txt

echo "Données mises à jour avec succès"