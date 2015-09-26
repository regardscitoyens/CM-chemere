#!/bin/bash

ls source-doc | while read file; do
  soffice --headless  --convert-to html "source-doc/$file"
  html=$(echo "$file" | sed 's/.doc/.html/')
  echo $file $html
  mv "$html" "html/$html"
done
