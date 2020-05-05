#!/bin/bash

for ((i=1;i<=8;i++))
do
	python3.7 grab_news.py rss_parts/${i}.txt news_collector/${i}.jsonl &
done
