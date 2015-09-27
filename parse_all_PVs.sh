#!/bin/bash

echo > /tmp/presences1
ls html/CM* | while read f; do
  if ! python parse_PV.py "$f" >> /tmp/presences1; then echo "ERROR on $f"; fi
done

echo > /tmp/presences2
ls source-doc/CM* source-pdf/CM* | sed 's/^.*\/CM //' | sed 's/\..*$//' | sort -u > /tmp/allPVs
ls html/CM* | sed 's/^.*\/CM //' | sed 's/\..*$//' | sort -u > /tmp/allHtmls
diff /tmp/allPVs /tmp/allHtmls | grep '>' | sed 's/> /xml\/CM /' | sed 's/$/.xml/' | while read f; do
  if ! python parse_PV.py "$f" >> /tmp/presences2; then echo "ERROR on $f"; fi
done

