
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

def data_process(inpath,tsne):
	cmap = plt.cm.jet
	try:
		with open(inpath,'rb') as filer:
			data,labels = pickle.load(filer)
			data = minmax_scale(data, feature_range=(-1, 1))
	except Exception as E:
		print(E)
		pdb.set_trace()
	# with open('drivers.pkl','rb') as dvr:
	# 	drivdata = pickle.load(dvr)
	# 	drivdata = minmax_scale(drivdata, feature_range=(-1, 1))

	# driv = TSNE(n_components=3).fit_transform(drivdata)
	if(tsne == 'y'):
		dataemb = TSNE(n_components=3).fit_transform(data)
	else:
		dataemb = data
	N = max(labels)+1
	print(N)
	# print()
	cmaplist = [cmap(i) for i in range(cmap.N)]
	cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
	
	bounds = np.linspace(0,N,N+1)
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(dataemb[:,0], dataemb[:,1],dataemb[:,2], c=labels, cmap=cmap)
	# ax.plot(driv[:,0],driv[:,1],driv[:,2],"s")

	# fig = plt.figure(figsize=(8,8))
	# plt.scatter(dataemb[:,0], dataemb[:,1], c=labels, cmap=cmap)
	plt.show()



# colors = [""]

def main():
	inpath = sys.argv[1]
	tsne = sys.argv[2]
	# outpath = sys.argv[2]
	
	data_process(inpath,tsne)

			
if __name__ == '__main__':
	main()

