import jsonlines
import sys
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
import pickle
from fix_punc import fix_punc
import math
from produce_word_cloud import preprocess_tok

def lookup_ngram(gram,w1,w2,typecall='uni'):
	if typecall == 'uni':
		try:
			return gram[(w1,)]
		except:
			return gram[('UNK1',)]
	elif typecall == 'bi':
		try:
			return gram[(w1, w2)]
		except:
			return gram[('UNK1', 'UNK2')]
	else:
		print('INVALID INPUT')
		exit(1)

def pmi(word1,word2,unigram_freq,bigram_freq):
	word1 = word1.lower()
	word2 = word2.lower()
	prob_word1 = lookup_ngram(unigram_freq,word1,'','uni') / float(sum(unigram_freq.values()))
	prob_word2 = lookup_ngram(unigram_freq,word2,'','uni') / float(sum(unigram_freq.values()))
	prob_word1_word2 = lookup_ngram(bigram_freq,word1,word2,'bi') / float(sum(bigram_freq.values()))
	try:
		return math.log(prob_word1_word2/float(prob_word1*prob_word2),2)
	except:
		return 0

def get_ngrams_models(toktext):
	unigrams = ngrams(toktext,1)
	bigrams = ngrams(toktext,2)
	return dict(Counter(unigrams)),dict(Counter(bigrams))

def main():
	inputpath = sys.argv[1]
	outputpath = sys.argv[2]
	corpus = ''
	with jsonlines.open(inputpath,'r') as jr:
		for line in jr:
			corpus += (line['text'] + ' ')

	corpustoken = word_tokenize(corpus.lower().strip() + ' UNK1' + ' UNK2')
	unigram,bigram = get_ngrams_models(corpustoken)

	with open(outputpath,'wb') as pkl:
		pickle.dump((unigram,bigram),pkl)

if __name__ == '__main__':
	main()