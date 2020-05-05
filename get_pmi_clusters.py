import jsonlines
import sys
from create_corpus_file import pmi
from nltk.util import ngrams
from nltk import word_tokenize
import pickle
from collections import Counter
import operator
from itertools import permutations 
import numpy as np
import pdb
from produce_word_cloud import preprocess_tok
from fix_punc import fix_punc
import os

inputpath = sys.argv[1]
ngrampath = sys.argv[2]
outputpath = sys.argv[3]

def pmi_score(top_words,uni,bi):
	pairs = list(permutations(top_words,2))
	# pdb.set_trace()
	scores = np.array([pmi(pair[0][0],pair[1][0],uni,bi) for pair in pairs])
	return np.percentile(scores,50)

def get_mini_corpus(articles):
	line = ''
	for ar in articles:
		line += (ar + ' ')
	return line.strip().lower()

def process_cluster(articles,unimodel,bimodel,topn=15):
	text = get_mini_corpus(articles)
	nclusele = len(articles)
	articles = []

	
	tok = preprocess_tok(word_tokenize(fix_punc(text)))
	freqs = dict(Counter(ngrams(tok,1)))
	
	top_words = sorted(freqs, key=freqs.get, reverse=True)[:topn]
	# pdb.set_trace()
	score = pmi_score(top_words,unimodel,bimodel)

	return float(score),float(nclusele),top_words[:3]

	# sorted_d = dict(sorted(freqs.items(), key=operator.itemgetter(1),reverse=True))


with open(ngrampath,'rb') as ng:
	unigram,bigram = pickle.load(ng)

pmiv = []
nele = []
top_words_list = []

filmode = 'w'
if(os.path.isfile(outputpath)):
	filmode = 'a'

with jsonlines.open(inputpath,'r') as filer, jsonlines.open(outputpath,filmode) as jw:
	for line in filer:
		pmi_val,nc,topw = process_cluster(line['articles'],unigram,bigram)
		pmiv.append(pmi_val)
		nele.append(nc)
		top_words_list.append(topw)

	pmiv = np.array(pmiv)
	nele = np.array(nele) / sum(nele)
	weighted_pmi = sum(pmiv*nele)
	# pdb.set_trace()

	jw.write({'Number of clusters':float(len(nele)),'parameters':inputpath[:inputpath.rfind('.jsonl')],'score':weighted_pmi,'words':top_words_list})