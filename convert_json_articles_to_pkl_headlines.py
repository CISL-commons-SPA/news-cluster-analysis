import jsonlines
import sys
import pickle
import nltk

lines = []
with jsonlines.open(sys.argv[1],'r') as fr, open(sys.argv[2],'wb') as fw:
	for line in fr:
		lines.append(nltk.tokenize.sent_tokenize(line['text'])[0])

	pickle.dump(lines,fw)