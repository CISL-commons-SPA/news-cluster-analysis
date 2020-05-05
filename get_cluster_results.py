
import numpy as np 
import pdb
import nltk
import sys
import pickle
from sklearn.metrics.pairwise import paired_cosine_distances,paired_euclidean_distances
import time
from sklearn.cluster import KMeans
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import jsonlines

def get_centroids(data,labels):
    cents = []
    for i in range(labels.min(), labels.max()+1):
        cents.append(data[labels == i].mean(0))
    return np.vstack(cents)

def cluster_data(X,metric_value,option='maxclust'):
	kmeans = KMeans(n_clusters=metric_value)
	kmeans.fit(X)
	assigned_clusters = kmeans.labels_;
	centroids = kmeans.cluster_centers_;
	return assigned_clusters,centroids;

def data_process(inpath,article_lines,outpath):

	try:
		with open(inpath,'rb') as filer, open(article_lines,'rb') as ar:
			_,labels = pickle.load(filer)
			datalines = np.array(pickle.load(ar))
			# pdb.set_trace()
			# data = minmax_scale(data, feature_range=(-1, 1))
	except Exception as E:
		print(E)
		pdb.set_trace()
	with jsonlines.open(outpath,'w') as jr:
		maxlabel = max(labels)
		minlabel = min(labels)
		for i in range(minlabel,maxlabel+1):
			jr.write({'label':i,'articles':datalines[labels == i].tolist()})

# colors = [""]

def main():
	inpath = sys.argv[1]
	article_lines = sys.argv[2]
	outpath = sys.argv[3]
	
	data_process(inpath,article_lines,outpath)

			
if __name__ == '__main__':
	main()

