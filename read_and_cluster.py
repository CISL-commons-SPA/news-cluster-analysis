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
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')

# from silence_tensorflow import silence_tensorflow
# silence_tensorflow()

def get_embeddings(article_bodies,option):
	if option == 'semantic':
		tokenized_sentences = tokenize_sents(article_bodies)
		article_embed = np.array(get_article_embeddings(tokenized_sentences))
	elif option == 'lda':
		# numfeatures = int(sys.argv[4])
		lda_model,dictionary,_ = topic_modeling(article_bodies,'lda')
		print(lda_model.get_topics().shape)
		for i,body in enumerate(article_bodies):
				temvect = get_lda_embeddings(lda_model,dictionary,body)
				if(i == 0):
					article_embed = temvect
				else:
					article_embed = np.vstack((article_embed,temvect))
	elif option == 'bert':
		article_embed = np.array(model.encode(article_bodies))
	return article_embed


def get_keyword_embeddings(keywordslist,option):
	keyword_embed = []
	for keywords in keywordslist:
		if(keywords == []):
			keyword_embed.append(np.zeros(keyword_embed[0].shape[1]))
		else:
			keyword_embed.append(np.array([get_embeddings([keyword],option) for keyword in keywords]).mean(axis=0)[0])
	return np.array(keyword_embed)


model_dir = 'data/best_weights'
data_dir = 'data'

get_embed = Embedding(model_dir,data_dir)

def tokenize_sents(sents):
	# pdb.set_trace()
	return [tokenize(s) for s in sents]

def get_article_embeddings(token_sents):
	return [get_embed.get_article_embed(sent) for sent in token_sents]

def dims_check(embed,data):
	if(len(embed.shape) != 2):
		dims = embed[0].shape[0]
		embed = np.array([emb if(data[i]!='') else np.zeros(dims) for i,emb in enumerate(embed)])
	return embed
	

article_lines_path = sys.argv[1]
output_path = sys.argv[2]
option = sys.argv[3]
featp = sys.argv[4]

article_bodies = []
article_embed = []

if(featp != 'article-and-headline'):

	with open(article_lines_path,'rb') as pr:
		article_bodies = pickle.load(pr)

	article_embed = get_embeddings(article_bodies,option)

else:
	article_bodies = []
	headlines = []
	keywords = []
	with jsonlines.open(article_lines_path,'r') as pr:
		for line in pr:
			article_bodies.append(line['text'])
			headlines.append(line['title'])
			keywords.append(line['keywords'])

	article_embed = get_embeddings(article_bodies,option)
	# pdb.set_trace()
	headline_embed = get_embeddings(headlines,option)
	keyword_embed = get_keyword_embeddings(keywords,option)
	# pdb.set_trace()
	headline_embed = dims_check(headline_embed,headlines)
	
	article_embed = np.hstack((article_embed,headline_embed))
	article_embed = np.hstack((article_embed,keyword_embed))

print(article_embed.shape)
with open(output_path,'wb') as pkl:
	pickle.dump(article_embed,pkl)
