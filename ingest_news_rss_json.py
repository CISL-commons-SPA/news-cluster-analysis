import json
import sys
from dlib import Ranker
from nltk import word_tokenize
import pickle
import pdb
import jsonlines

def unique_articles_in_json(total_articles):
	total_articles = list({dt['text']:dt for dt in total_articles}.values())
	return total_articles

def process_RSS_feed(articles,drivers,topN,ranker,tokthresh=10):
	txttok = []
	newarticles = []
	for article in articles:
		tok_ar = word_tokenize(article['text'])
		if len(tok_ar) > tokthresh:
			txttok.append(tok_ar)
			newarticles.append(article)
	articles = []
	total_articles = []
	# print(articles[9])
	for driver in drivers:
		rankjson = ranker.query2articles(word_tokenize(driver),txttok, topN)
		indices = [rank['index'] for rank in rankjson]
		total_articles += [newarticles[i] for i in indices]
	total_articles = list({dt['text']:dt for dt in total_articles}.values())
	return total_articles

def main():
	inputpath = sys.argv[1]
	outputpath_articles = sys.argv[2]
	outputpath_headlines = sys.argv[3]
	outputpath_articles_unique_jsonl = sys.argv[4]
	driverpath = sys.argv[5]
	topN = int(sys.argv[6])

	lines = []

	ranker = Ranker('data/best_weights','data')

	with open(driverpath,'r') as driv:
		drivers = driv.readlines()
		drivers = [driv.replace('\n','').strip() for driv in drivers]

	with open(inputpath,'r') as jr:
		articles_json = json.load(jr)

	complete_set = []

	for key in articles_json.keys():
		# print(key)
		complete_set += process_RSS_feed(articles_json[key],drivers,topN,ranker)

	complete_set = list({dt['text']:dt for dt in complete_set}.values())

	with jsonlines.open(outputpath_articles_unique_jsonl,'w') as filew:
		filew.write_all(complete_set)

	texts = [ar['text'] for ar in complete_set]
	titles = [ar['title'] for ar in complete_set]

	with open(outputpath_articles,'wb') as arT, open(outputpath_headlines,'wb') as hdT:
		pickle.dump(texts,arT)
		pickle.dump(titles,hdT)
###################################
##                               ##
##                               ##
###################################
if __name__ == '__main__':
	main()