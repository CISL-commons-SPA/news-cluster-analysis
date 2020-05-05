
import numpy as np 
# from nltk.cluster import KMeansClusterer
import nltk
import sys
import pickle
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import paired_cosine_distances,paired_euclidean_distances
import time
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from scipy.cluster import  hierarchy
# from scipy.cluster.vq import kmeans,vq
from sklearn.cluster import KMeans
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import silhouette_score

def compute_inertia(a, X):
    W = [np.mean(pairwise_distances(X[a == c, :])) for c in np.unique(a)]
    return np.mean(W)

def compute_gap(clustering, data, k_min=0,k_max=5,step=1, n_references=5):
    totlab = []
    cents = []
    if len(data.shape) == 1:
        data = data.reshape(-1, 1)
    reference = np.random.rand(*data.shape)
    reference_inertia = []
    ondata_inertia = []

    for k in np.arange(k_min, k_max+1,step):
        tn = time.time()
        local_inertia = []
        for _ in range(n_references):
            clustering.n_clusters = k
            assignments = clustering.fit_predict(reference)
            local_inertia.append(compute_inertia(assignments, reference))
        reference_inertia.append(np.mean(local_inertia))
    
        clustering.n_clusters = k
        assignments = clustering.fit_predict(data)
        totlab.append(clustering.labels_)
        cents.append(clustering.cluster_centers_)
        ondata_inertia.append(compute_inertia(assignments, data))
        tn2 = time.time()
        print('cluster ',k,' took ',tn2-tn,' seconds')

    gap = np.log(reference_inertia)-np.log(ondata_inertia)

    return gap, totlab,cents

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
        average_sil_vect = []
        t1 = time.time()
        for i in range(min_clusters,max_clusters+5,5):
            labels,centroids = cluster_data(data,i,option);
            totlab += [labels]
            cents += [centroids]
            average_sil = silhouette_score(data,labels)
            average_sil_vect.append(average_sil)
            print('Done clustering for cluster# ',i)
            t2 = time.time()
            print(t1-t2,' seconds taken')
            t1=t2
        totlab = np.array(totlab)
        centroids = np.array(cents)
        # wss_average = get_wss_cosine_avg(centroids,totlab,data,max_clusters)
        # print(wss_average)
        print(average_sil_vect)
        pickle.dump((totlab,cents,average_sil_vect),filew)


def process_cluster_gap(inpath,outpath,option='maxclust',min_clusters=21,max_clusters=50,step=1):
    with open(inpath,'rb') as filer, open(outpath,'wb') as filew:
        data = pickle.load(filer)
        data = minmax_scale(data, feature_range=(-1, 1))
        t1 = time.time()
        gap,totlab,cents = compute_gap(KMeans(),data, min_clusters,max_clusters,step)
        # wss_average = get_wss_cosine_avg(centroids,totlab,data,max_clusters)
        print(gap)
        # print(average_sil_vect)
        pickle.dump((totlab,cents,gap),filew)

def main():
    inpath = sys.argv[1]
    outpath = sys.argv[2]
    
    print('starting ',inpath)
    process_cluster_gap(inpath,outpath,'maxclust',5,150,5)
    print(inpath,outpath)
            
if __name__ == '__main__':
    main()

