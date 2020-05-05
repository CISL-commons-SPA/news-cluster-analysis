#!/bin/bash

for((i=168;i<=179;i++))

do
	time ./markov.sh unfiltered_english_news_semantic some cosine ${i} news_data/unfiltered_english_news y covid_19_score_0 average 5 unfiltered_english_news
done