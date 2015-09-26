#!/bin/bash

ls source-pdf | while read file; do
  pdftohtml -xml "source-pdf/$file"
  xml=$(echo "$file" | sed 's/.pdf/.xml/')
  echo $file $xml
  mv "source-pdf/$xml" "xml/$xml"
done
