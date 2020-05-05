import jsonlines
import sys
from ingest_news_rss_json import unique_articles_in_json
import pickle

def remove_articles(arlines):
	return [ar for ar in arlines if ar['text'] != '']

inputjson = sys.argv[1]
outputjsonlines = sys.argv[2]
outputarticle = sys.argv[3] 

total_articles_jsonl = []

with jsonlines.open(inputjson) as jr:
	for line in jr:
		total_articles_jsonl.append(line)

total_articles_jsonl = remove_articles(unique_articles_in_json(total_articles_jsonl))
 
with jsonlines.open(outputjsonlines,'w') as jw:
	jw.write_all(total_articles_jsonl)

articles = [ar['text'] for ar in total_articles_jsonl]

with open(outputarticle,'wb') as jb:
	pickle.dump(articles,jb)