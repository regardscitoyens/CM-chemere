#!/bin/sh

for json in json/*; do
	python find_streets.py "$json";
done
