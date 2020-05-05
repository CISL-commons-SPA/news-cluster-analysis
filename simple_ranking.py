import jsonlines
from ingest_news_rss_json import process_RSS_feed # process_RSS_feed(articles,drivers,topN,tokthresh=10)
import sys
from dlib import Ranker

def dictify(article):
	return {'text':article}

def main():
	articles_path = sys.argv[1]
	drivers_path = sys.argv[2]
	output_path = sys.argv[3]
	ranker = Ranker('data/best_weights','data')

	articles = []

	with open(articles_path,'r') as ar:
		articles = ar.readlines()

	with open(drivers_path,'r') as dr:
		drivers = dr.readlines()

	drivers = [driver.replace('\n','').strip() for driver in drivers]
	json_articles = [dictify(article.replace('\n','').strip()) for article in articles]

	new_articles = process_RSS_feed(json_articles,drivers,10,ranker)
	newticles = [ar['text'].replace('\n','').replace('\r','') + '\n' for ar in new_articles]
	# newticles = list(set(newticles))
	with open(output_path,'w') as ow:
		ow.writelines(newticles)

####


if __name__ == '__main__':
	main()