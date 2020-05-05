import pickle
import jsonlines
import sys
import numpy as np
from sklearn.metrics import pairwise_distances
from dlib import Ranker
from nltk import word_tokenize
from do_driver_calls import get_driver_dict
import pdb

ranker = Ranker('data/best_weights','data')

data_labels_path = sys.argv[1]
article_jsonlines_path = sys.argv[2]
driverpath = sys.argv[3]
outputpath = sys.argv[4]

def get_mediod(data,mapping):
	return mapping[pairwise_distances([data.mean(0)],data).argmax()]

def get_mediod_indices(data,labels):
	mediod_indices = []
	minval = min(labels)
	maxval = max(labels)
	for i in range(minval,maxval+1):
		boolv = labels == i;
		mediod_indices.append(get_mediod(data[boolv],np.where(boolv)[0]))
	return mediod_indices

def tokenize_texts(lines):
	return [word_tokenize(line) for line in lines]

def do_driver_lookups(articles,mediod_indices,drivers,num=5):
	drivertok = tokenize_texts(drivers)
	driver_jsonl = []
	for i,mdi in enumerate(mediod_indices):
		# pdb.set_trace()
		results = ranker.article2queries(word_tokenize(articles[mdi]),drivertok,num)
		results = [res['driver'] for res in results]
		driver_jsonl.append(get_driver_dict(results,i))
	return driver_jsonl

with open(data_labels_path,'rb') as rpkl:
	data,labels = pickle.load(rpkl)

articles = []
with jsonlines.open(article_jsonlines_path,'r') as jr:
	for line in jr:
		articles.append(line)
article_text = [ar['text'] for ar in articles]

with open(driverpath,'r') as dr:
	drivers = [dr.strip().replace('\n','') for dr in dr.readlines()]

mediod_indices = get_mediod_indices(data,labels)
driver_jsonl = do_driver_lookups(article_text,mediod_indices,drivers)

with jsonlines.open(outputpath,'w') as jw:
	jw.write_all(driver_jsonl)