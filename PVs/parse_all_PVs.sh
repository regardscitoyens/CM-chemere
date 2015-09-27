#!/bin/bash

mkdir -p data

function parsePV {
  f=$1
  csv=$2
  if ! python parse_PV.py "$f" >> $csv; then
    echo "ERROR on $f"
  else
    python parse_PV.py "$f" 1 > /tmp/parsedPV.json
    outfile=$(grep '"date":' /tmp/parsedPV.json | sed 's/^.*: "//' | sed 's/",/.json/')
    mv -f /tmp/parsedPV.json "data/$outfile"
  fi
}

rm -f data/presences.tmp

ls ../html/CM* | while read f; do
  parsePV "$f" data/presences.tmp
done

ls ../source-doc/CM* ../source-pdf/CM* | sed 's/^.*\/CM //' | sed 's/\..*$//' | sort -u > /tmp/allPVs
ls ../html/CM* | sed 's/^.*\/CM //' | sed 's/\..*$//' | sort -u > /tmp/allHtmls
diff /tmp/allPVs /tmp/allHtmls | grep '<' | sed 's|< |../xml/CM |' | sed 's/$/.xml/' | while read f; do
  parsePV "$f" data/presences.tmp
done

echo "date,heure,élu" > data/presences.csv
sort data/presences.tmp >> data/presences.csv
rm -f data/presences.tmp
