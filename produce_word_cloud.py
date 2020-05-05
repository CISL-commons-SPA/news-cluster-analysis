import jsonlines
# from nltk.corpus import stopwords
from wordcloud import WordCloud 
import matplotlib.pyplot as plt 
import pandas as pd 
from nltk import word_tokenize
import sys
import os
from nltk.stem import WordNetLemmatizer
import imageio
import nltk

wordnet_lemmatizer = WordNetLemmatizer()
stop_words = set([
    'all', 'six', 'just', 'less', 'being', 'indeed', 'over', 'move', 'anyway', 'four', 'not', 'own', 'through',
    'using', 'fifty', 'where', 'mill', 'only', 'find', 'before', 'one', 'whose', 'system', 'how', 'somewhere',
    'much', 'thick', 'show', 'had', 'enough', 'should', 'to', 'must', 'whom', 'seeming', 'yourselves', 'under',
    'ours', 'two', 'has', 'might', 'thereafter', 'latterly', 'do', 'them', 'his', 'around', 'than', 'get', 'very',
    'de', 'none', 'cannot', 'every', 'un', 'they', 'front', 'during', 'thus', 'now', 'him', 'nor', 'name', 'regarding',
    'several', 'hereafter', 'did', 'always', 'who', 'didn', 'whither', 'this', 'someone', 'either', 'each', 'become',
    'thereupon', 'sometime', 'side', 'towards', 'therein', 'twelve', 'because', 'often', 'ten', 'our', 'doing', 'km',
    'eg', 'some', 'back', 'used', 'up', 'go', 'namely', 'computer', 'are', 'further', 'beyond', 'ourselves', 'yet',
    'out', 'even', 'will', 'what', 'still', 'for', 'bottom', 'mine', 'since', 'please', 'forty', 'per', 'its',
    'everything', 'behind', 'does', 'various', 'above', 'between', 'it', 'neither', 'seemed', 'ever', 'across', 'she',
    'somehow', 'be', 'we', 'full', 'never', 'sixty', 'however', 'here', 'otherwise', 'were', 'whereupon', 'nowhere',
    'although', 'found', 'alone', 're', 'along', 'quite', 'fifteen', 'by', 'both', 'about', 'last', 'would',
    'anything', 'via', 'many', 'could', 'thence', 'put', 'against', 'keep', 'etc', 'amount', 'became', 'ltd', 'hence',
    'onto', 'or', 'con', 'among', 'already', 'co', 'afterwards', 'formerly', 'within', 'seems', 'into', 'others',
    'while', 'whatever', 'except', 'down', 'hers', 'everyone', 'done', 'least', 'another', 'whoever', 'moreover',
    'couldnt', 'throughout', 'anyhow', 'yourself', 'three', 'from', 'her', 'few', 'together', 'top', 'there', 'due',
    'been', 'next', 'anyone', 'eleven', 'cry', 'call', 'therefore', 'interest', 'then', 'thru', 'themselves',
    'hundred', 'really', 'sincere', 'empty', 'more', 'himself', 'elsewhere', 'mostly', 'on', 'fire', 'am', 'becoming',
    'hereby', 'amongst', 'else', 'part', 'everywhere', 'too', 'kg', 'herself', 'former', 'those', 'he', 'me', 'myself',
    'made', 'twenty', 'these', 'was', 'bill', 'cant', 'us', 'until', 'besides', 'nevertheless', 'below', 'anywhere',
    'nine', 'can', 'whether', 'of', 'your', 'toward', 'my', 'say', 'something', 'and', 'whereafter', 'whenever',
    'give', 'almost', 'wherever', 'is', 'describe', 'beforehand', 'herein', 'doesn', 'an', 'as', 'itself', 'at',
    'have', 'in', 'seem', 'whence', 'ie', 'any', 'fill', 'again', 'hasnt', 'inc', 'thereby', 'thin', 'no', 'perhaps',
    'latter', 'meanwhile', 'when', 'detail', 'same', 'wherein', 'beside', 'also', 'that', 'other', 'take', 'which',
    'becomes', 'you', 'if', 'nobody', 'unless', 'whereas', 'see', 'though', 'may', 'after', 'upon', 'most', 'hereupon',
    'eight', 'but', 'serious', 'nothing', 'such', 'why', 'off', 'a', 'don', 'whereby', 'third', 'i', 'whole', 'noone',
    'sometimes', 'well', 'amoungst', 'yours', 'their', 'rather', 'without', 'so', 'five', 'the', 'first', 'with',
    'make', 'once'
])

def lemmatize_max(token):
    retval = wordnet_lemmatizer.lemmatize(wordnet_lemmatizer.lemmatize(wordnet_lemmatizer.lemmatize(token, pos = "n"), pos = "v"), pos = ("a"))
    return retval

def lemmatize_min(token,postg='n'):
	return wordnet_lemmatizer.lemmatize(token, pos = postg)

def preprocess_tok(tok):
	tok = nltk.pos_tag(tok)
	# tok = [t for t in tok if lemmatize_max(t[0]) not in stop_words and t[0] not in stop_words and len(t[0]) > 2]
	tok = [lemmatize_min(t[0],'n') for t in tok if 'NN' in t[1] and lemmatize_min(t[0],'n') not in stop_words and t[0] not in stop_words] + [lemmatize_min(t[0],'a') for t in tok if 'JJ' in t[1] and lemmatize_min(t[0],'a') not in stop_words and t[0] not in stop_words] + [lemmatize_min(t[0],'v') for t in tok if 'VB' in t[1] and lemmatize_min(t[0],'v') not in stop_words and t[0] not in stop_words] + [t[0] for t in tok if 'NN' not in t[1] and 'JJ' not in t[1] and 'VB' not in t[1] and lemmatize_max(t[0]) not in stop_words and t[0] not in stop_words]
	return tok

def get_wordcloud_cluster(articles,outfolderpath):
	wc_words = ''

	for article in articles:
		tok = word_tokenize(article.lower())
		tok = preprocess_tok(tok)
		wc_words += (' '.join(tok) + ' ')	  

	wordcloud = WordCloud(width = 800, height = 800, 
	                background_color ='white', 
	                stopwords = stop_words, 
	                min_font_size = 10).generate(wc_words)

	# plot the WordCloud image           
	imageio.imwrite(outfolderpath, wordcloud)             

def main():
	inpath = sys.argv[1]
	outfolder = sys.argv[2]

	if(not(os.path.isdir(outfolder))):
		os.mkdir(outfolder)

	with jsonlines.open(inpath,'r') as lines:
		for i,line in enumerate(lines):
			get_wordcloud_cluster(line['articles'],outfolder + '/' + str(i) + '.jpeg')

if __name__ == '__main__':
	main()