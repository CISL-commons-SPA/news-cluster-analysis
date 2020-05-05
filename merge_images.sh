#!/bin/bash

for file in cluster_wordcloud/${1}/*.jpeg
do
	convert ${file} -bordercolor black -border 0x2  ${file}
done

convert -append cluster_wordcloud/${1}/*.jpeg cluster_wordcloud/${1}/${1}_stacked.jpeg