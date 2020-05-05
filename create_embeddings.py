import pickle
import sys
from lda_clustering import topic_modeling, get_hdp_labels, clean
import numpy as np 


inputpath = sys.argv[1]
outputpath = sys.argv[2]
topics = int(sys.argv[3])

cetext = []

with open(inputpath,'r') as flr:
	flr = csv.reader(flr)
	for row in flr:
		cause,effect = row
		cetext.append(cause+' '+effect)

lda_model,dictionary,_ = topic_modeling(cetext,'lda',topics)
topic_vect = get_lda_embeddings(lda_model,dictionary,cetext)

with open(outputpath,'w') as filw:
	pickle.dump(topic_vect,filw)