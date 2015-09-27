#!/bin/sh
for html in html/Arrete*; do
	JSON=$(echo "$html" | sed 's/ /_/g' | sed 's/html/json/g' | sed 's/\.\..//')
	echo $JSON
	python arrete_parser.py "$html" > "$JSON" || exit 1;
done
