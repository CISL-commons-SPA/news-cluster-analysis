
import faulthandler; faulthandler.enable()
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
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
from lda_clustering import topic_modeling, get_hdp_labels, clean
import pdb
from itertools import chain
from sklearn.metrics import pairwise_distances
import markov_clustering as mc
import networkx as nx
import random
from scipy.sparse import csc_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from spectral_cluster import generate_knn_mst_graph
import scipy.io as sio
import subprocess
# from markov_stability.stability import calculate_full_stability

def get_distance_matrix(features,dist='cosine'):
	distance_matrix = []
	for i,data in enumerate(features):
		vect = pairwise_distances([data],features,dist).ravel()
		try:
			vect[i] = 0
		except:
			pdb.set_trace()
		distance_matrix.append(vect)
	return np.array(distance_matrix)

	#notes: For 250 optimizations => index = 159 has 308 clusters and the local min of variation of Information
	#notes: For 250 optimizations =>index = 168 has 105 clusters
	#notes: For 250 optimizations => index = 175 has 25 clusters
	#notes: or 500 optimizations => index 235	
def load_and_get_clusters_markov(path_to_clusters,path_to_variation,path_to_commodities,index=235):
	cluster_labels = []
	mat_contents = sio.loadmat(path_to_variation)
	VI = mat_contents['VI']
	VI = VI[0]
	mat_contents = sio.loadmat(path_to_commodities)
	N = mat_contents['N']
	print(N)
	N = N[0]
	mat_contents = sio.loadmat(path_to_clusters)
	C = mat_contents['C']
	numClusters = N[index]
	print(numClusters)
	# print(N)
	numarticles = C.shape[0]
	for a_id in range(numarticles):
		cluster_labels.append(C[a_id][index])
	return np.array(cluster_labels).astype(int)




def perform_clustering(inpath,outpath,option='hierarchy',article_path = '',params = {}):
	with open(inpath,'rb') as filer, open(outpath,'wb') as filew:
		data = pickle.load(filer)
		data = minmax_scale(data, feature_range=(-1, 1))
		labels = []
		if(option == 'heirarchy'):
			clustering = AgglomerativeClustering(n_clusters=params['n_clusters'],affinity=params['affinity'],linkage=params['linkage'],distance_threshold=params['distance_threshold']).fit(data)
			labels = clustering.labels_
			# print(labels)
		elif (option == 'kmeans'):
			k_val = params['k']
			kmeans = KMeans(n_clusters=k_val).fit(data)
			labels = kmeans.labels_
		elif(option == 'dbscan'):
			db = DBSCAN(eps=params['eps'], min_samples=params['min_samples']).fit(data)
			labels = db.labels_
		elif(option == 'tsne'):
			dataemb = TSNE(n_components=params['dimensions']).fit_transform(data)
			pickle.dump(dataemb,filew)
			return
		elif(option == 'hdp-lda'):
			with open(article_path,'rb') as pr:
				article_bodies = pickle.load(pr)
			lda_model,dictionary,_ = topic_modeling(article_bodies,'hdp')
			numtopics = lda_model.get_topics().shape[0]
			for i,body in enumerate(article_bodies):
				label = get_hdp_labels(lda_model,dictionary,body)
				labels.append(label)
			labels = np.array(labels)

		elif(option == 'lda'):
			with open(article_path,'rb') as pr:
				article_bodies = pickle.load(pr)
			lda_model,dictionary,_ = topic_modeling(article_bodies,'lda',params['numtopics'])
			# pdb.set_trace()
			bow_bodies = [dictionary.doc2bow(clean(body).split()) for body in article_bodies]
			lda_corpus = lda_model[bow_bodies]
			scores = list(chain(*[[score for topic_id,score in topic] for topic in [doc for doc in lda_corpus]]))
			threshold = sum(scores)/len(scores)
			labels = []
			print(threshold)
			for bow in lda_corpus:
				for i in range(params['numtopics']):
					if bow[i][1] > threshold:
						labels.append(i)
						break;
			labels = np.array(labels)
		elif(option == 'markov'):
			# mat = abs(1 - get_distance_matrix(data,dist=params['dist']))
			# # data_mat = csr_matrix(mat)
			# # mst_dat = minimum_spanning_tree(data_mat)
			# # mst_dat = mst_dat.toarray().astype(float)
			# knn_mst = generate_knn_mst_graph(mat)
			# # g = nx.from_numpy_matrix(knn_mst)
			# # g.to_undirected()
			# # knn_mst = nx.to_numpy_matrix(g)
			# np.savetxt('matlab/sparse_graph.txt', knn_mst, delimiter=",", fmt="%-0.5f")
			# subprocess.call(["./matlab/embedded"])

			labels = load_and_get_clusters_markov('matlab/Cluster Labels.mat','matlab/Variation.mat','matlab/Number of Communities.mat',params['markov_iterations'])
			# if('markov_time' in params.keys()):
			# 	result = mc.run_mcl(knn_mst,inflation=params['markov_time'])
			# else:
			# 	result = mc.run_mcl(knn_mst)

			# for inflation in [i / 10 for i in range(15, 100)]:
			# 	result = mc.run_mcl(nx.to_scipy_sparse_matrix(nx.from_numpy_matrix(knn_mst)), inflation=inflation)
			# 	clusters = mc.get_clusters(result)
			# 	Q = mc.modularity(matrix=result, clusters=clusters)
			# 	print("inflation:", inflation, "modularity:", Q)
			# result = calculate_full_stability(knn_mst,[params['markov_time']])
			# pdb.set_trace()
			# clusters = mc.get_clusters(result)
			# print(len(clusters))
			# labels = np.zeros(data.shape[0])
			# for ic,clist in enumerate(clusters):
			# 	labels[[c for c in clist]] = ic
			# labels = labels.astype(int)
			# mc.draw_graph(mat, clusters, pos=positions, node_size=50, with_labels=False, edge_color="silver")
			# pdb.set_trace()
			# Q = mc.modularity(matrix=csc_matrix(result), clusters=clusters)
		else:
			print('invalid option')
			print(option)

		pickle.dump((data,labels),filew)


def main():
	inpath = sys.argv[1]
	outpath = sys.argv[2]
	param = sys.argv[3]
	typep = sys.argv[4].strip()

	params = {}
	if(typep == 'kmeans'):
		params['k'] = int(param)
	elif(typep == 'heirarchy'):
		param2 = sys.argv[5]
		params['n_clusters'] = None
		params['affinity'] = 'cosine'
		params['linkage'] = param2
		params['distance_threshold'] = float(param) 
	elif(typep == 'dbscan'):
		param2 = sys.argv[5]
		params['eps'] = float(param)
		params['min_samples'] = float(param2)
	elif(typep == 'tsne'):
		params['dimensions'] = int(param)
	elif(typep == 'hdp-lda'):
		params = {}
		perform_clustering(inpath,outpath,typep,param,params)
		return 1;
	elif(typep == 'lda'):
		numtopics = sys.argv[5]
		params['numtopics'] = int(numtopics)
		perform_clustering(inpath,outpath,typep,param,params)
		return 1;
	elif(typep == 'markov'):
		params['dist'] = param
		try:
			params['markov_iterations'] = int(sys.argv[5])
		except:
			pass
		# perform_clustering(inpath,outpath,typep,'',params)
	else:
		print('wrong choice')
		print(typep,params)
		exit(1)
	
	perform_clustering(inpath,outpath,typep,'',params)

if __name__ == '__main__':
	main()