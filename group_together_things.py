import jsonlines
import dlib
from dlib.load_embed import Embedding
import numpy as np
import sklearn
from nltk import word_tokenize as tokenize
from sklearn.cluster import KMeans
import pdb
import pickle
import sys
from lda_clustering import topic_modeling, get_lda_embeddings,clean
# from silence_tensorflow import silence_tensorflow
# silence_tensorflow()
from dlib import Ranker
import json


model_dir = 'data/best_weights'
data_dir = 'data'

rank_one = Ranker(model_dir,data_dir)
# get_embed = Embedding(model_dir,data_dir)

def tokenize_sents(sents):
	# pdb.set_trace()
	return [tokenize(s) for s in sents]

def get_article_embeddings(token_sents):
	return [get_embed.get_article_embed(sent) for sent in token_sents]

def comparison(p,plist):
	# print(p,plist)
	plisttok = tokenize_sents(plist)
	ptok = tokenize(p)
	# print(plisttok)
	data = rank_one.article2queries(plisttok,ptok,1)
	return data[0]['driver']

def assign(clust_list,p,driver):
	flag = 0
	for i,data in enumerate(clust_list):
		pin = p in data
		lin = driver in data
		if(pin or lin):
			clust_list[i].add(p)
			clust_list[i].add(driver)
			flag = 1
			break
	if(flag == 0):
		tem = set()
		tem.add(p)
		tem.add(driver)
		clust_list.append(tem)

def sum_clust_list(clust_list):
	total = []
	for dat in clust_list:
		total += list(dat)
	# print(total)
	return set(total)

def clustering(plist):
	clust_list = []
	i = 0
	while (sum_clust_list(clust_list) != set(plist) or clust_list == []):
		# print(driver)
		driver = comparison(plist[i],plist)
		assign(clust_list,plist[i],driver)
		print(driver)
		i+=1
	return clust_list

def main():
	inpath = sys.argv[1]
	outpath = sys.argv[2]
	outjson = {}

	with open(inpath,'r') as filer:
		drivers = filer.readlines()
		drivers = [d.strip() for d in drivers]

	clist = clustering(drivers)

	for i,c in enumerate(clist):
		outjson[i] = c

	with open(outpath,'w') as jr:
		json.dump(outjson, jr)

if __name__ == '__main__':
	main()