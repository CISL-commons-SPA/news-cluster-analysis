
import numpy as np 
# from nltk.cluster import KMeansClusterer
import nltk
import sys
import pickle
from sklearn.metrics.pairwise import paired_cosine_distances,paired_euclidean_distances
import time
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from scipy.cluster import  hierarchy
# from scipy.cluster.vq import kmeans,vq
from sklearn.cluster import KMeans
from sklearn.preprocessing import minmax_scale



def get_centroids(data,labels):
    cents = []
    for i in range(labels.min(), labels.max()+1):
        cents.append(data[labels == i].mean(0))
    return np.vstack(cents)

def get_wss_cosine_avg(centroids,totlab,data,max_clusters):
	wss_cosine_avg = []
	try:
		for curr_clust,labs in enumerate(totlab):
			totdist = [];
			for i in range(0,len(centroids[curr_clust])):			
				clust_data = data[labs == i].tolist()
				if(len(clust_data) == 0):
					continue;
				# print(i,list(range(labs.min(),labs.max()+1)))

				cent = [centroids[curr_clust][i].tolist()]*len(clust_data)
				dists = paired_euclidean_distances(np.array(cent),np.array(clust_data))
				totdist += [dists.mean()]
			wss_cosine_avg +=[np.array(totdist).mean()]
	except:
		import pdb
		pdb.set_trace()

	return np.array(wss_cosine_avg)


def cluster_data(X,metric_value,option='maxclust'):
	kmeans = KMeans(n_clusters=metric_value)
	kmeans.fit(X)
	assigned_clusters = kmeans.labels_;
	centroids = kmeans.cluster_centers_;
	return assigned_clusters,centroids;

def process_cluster(inpath,outpath,option='maxclust',min_clusters=21,max_clusters=50):
	with open(inpath,'rb') as filer, open(outpath,'wb') as filew:
		data = pickle.load(filer)
		data = minmax_scale(data, feature_range=(-1, 1))
		totlab = []
		cents = []
		t1 = time.time()
		for i in range(min_clusters,max_clusters+5,5):
			labels,centroids = cluster_data(data,i,option);
			totlab += [labels]
			cents += [centroids]
			print('Done clustering for cluster# ',i)
			t2 = time.time()
			print(t1-t2,' seconds taken')
			t1=t2
		totlab = np.array(totlab)
		centroids = np.array(cents)
		wss_average = get_wss_cosine_avg(centroids,totlab,data,max_clusters)
		print(wss_average)
		pickle.dump((totlab,cents,wss_average),filew)


def main():
	inpath = sys.argv[1]
	outpath = sys.argv[2]
	
	process_cluster(inpath,outpath,'maxclust',5,230)

			
if __name__ == '__main__':
	main()

