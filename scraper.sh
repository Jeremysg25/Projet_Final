#!/bin/bash

clean_value() {
    echo "$1" | tr -d '\r\n €' | tr ',' '.' | xargs
}

DETTE_PUBLIQUE=$(clean_value "$(sed -n 's/.*id="custom-counter-value-dette"[^>]*>\([^<]*\).*/\1/p' source.html)")
DETTE_HABITANT=$(clean_value "$(sed -n 's/.*id="custom-counter-value-habitant"[^>]*>\([^<]*\).*/\1/p' source.html)")
DEFICIT_BUDGET=$(clean_value "$(sed -n 's/.*id="custom-counter-value-deficitmobile"[^>]*>\([^<]*\).*/\1/p' source.html)")

DETTE_PUBLIQUE=${DETTE_PUBLIQUE:-"NA"}
DETTE_HABITANT=${DETTE_HABITANT:-"NA"}
DEFICIT_BUDGET=${DEFICIT_BUDGET:-"NA"}

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "$TIMESTAMP,$DETTE_PUBLIQUE,$DETTE_HABITANT,$DEFICIT_BUDGET" >> history.csv

MAX_LINES=5
line_count=$(wc -l < history.csv)

if [ "$line_count" -gt "$MAX_LINES" ]; then
    head -n 1 history.csv > temp.csv
    tail -n +3 history.csv >> temp.csv
    mv temp.csv history.csv
fi

{
  echo "Dette publique : $DETTE_PUBLIQUE €"
  echo "Dette par habitant : $DETTE_HABITANT €"
  echo "Déficit du budget de l'État : $DEFICIT_BUDGET €"
} > data.txt
