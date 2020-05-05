#!/bin/bash

for filename in 'clustering_data_labels/'${1}
do
	if [[ "$filename" == *"driver"* ]]; then
  		continue
	fi
	python3 semantic_scoring.py $filename cluster_semantic_scores/${2}
done
