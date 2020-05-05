import sys
import jsonlines
import pickle
import numpy as np
# from sklearn.metrics.pairwise import paired_cosine_distances,paired_euclidean_distances
from sklearn.metrics import pairwise_distances
import os
import pdb
import traceback

def paired_cosine_similarity(dat1,matrix2):
	return 1 - pairwise_distances([dat1],matrix2,metric='cosine')


def metrics_per_cluster(dat,labels_data,opn='cos'):
	if(opn == 'cos'):
		simis = paired_cosine_similarity(dat,labels_data)
	elif(opn == 'euc'):
		simis = pairwise_distances([dat],labels_data,metric='euclidean')
	else:
		print('invalid option')
		exit(1)
	# print(get_field_name('simis',opn),simis)
	return np.mean(simis), np.sum(simis)

def fine_metrics_cluster(labels_data,opn='cos'):
	mean_vect = []
	total_vect = []
	for data in labels_data:

		if(opn == 'cos'):
			simis = paired_cosine_similarity(data,labels_data)
		elif(opn == 'euc'):
			simis = pairwise_distances([data],labels_data,metric='euclidean')
		else:
			print('invalid option')
			exit(1)
		mean_vect.append(np.mean(simis))
		total_vect.append(np.sum(simis))
	return np.mean(mean_vect),np.mean(total_vect),np.sum(mean_vect),np.sum(total_vect)

def obtain_semantic_measures(data,labels,opn='cos'):
	maxlabels = max(labels)
	minlabels = min(labels)
	mean_simv = []
	total_simv = []
	per_cluster_fine_mean = []
	per_cluster_total_mean = []
	per_cluster_fine_total = []
	per_cluster_total_total = []
	for i in range(minlabels,maxlabels+1):
		labels_data = []
		labels_data = data[labels == i]
		try:	
			mean_sim,total_sim = metrics_per_cluster(np.mean(labels_data,0),labels_data,opn)
		except Exception as E:
			print(E)
			print(traceback.format_exc())
			
		fmm,ftm,fmt,ftt = fine_metrics_cluster(labels_data,opn)

		mean_simv.append(mean_sim)
		total_simv.append(total_sim)
		per_cluster_fine_mean.append(fmm)
		per_cluster_total_mean.append(ftm)
		per_cluster_fine_total.append(fmt)
		per_cluster_total_total.append(ftt)
	# print(get_field_name('mean_simv ',opn),mean_simv)
	# print(get_field_name('total_simv ',opn),total_simv)
	return np.mean(mean_simv),np.mean(total_simv),np.sum(mean_simv),np.sum(total_simv),np.mean(per_cluster_fine_mean),np.mean(per_cluster_total_mean),np.sum(per_cluster_fine_total),np.sum(per_cluster_total_total)

def get_field_name(strung,option):
	return strung + ' (' + option + ')'

def get_json(data,name,option):
	data = [str(d) for d in data]
	return {'Parameter_settings':name,
	get_field_name('mean cross cluster similarity score',option):data[0],
	get_field_name('mean cross cluster total similarity score',option):data[1],
	get_field_name('total cross cluster average similarity score',option):data[2],
	get_field_name('total cross cluster total similarity score',option):data[3],
	get_field_name('per cluster pairwise only average',option):data[4],
	get_field_name('per cluster pairwise total average',option):data[5],
	get_field_name('per cluster pairwise only average total',option):data[6],
	get_field_name('per cluster pairwise complete total',option):data[7]}

def main():

	inpath = sys.argv[1]
	outpath = sys.argv[2]

	with open(inpath,'rb') as filer:
		(data,labels) = pickle.load(filer)

	maxlabels = max(labels) + 1
	name_for_data = inpath[inpath.find('/')+1:inpath.rfind('.pkl')]
	metricsC = obtain_semantic_measures(data,labels,'cos')
	metricsE = obtain_semantic_measures(data,labels,'euc')
	json_datC = get_json(metricsC,name_for_data,'Cosine')
	json_datE = get_json(metricsE,name_for_data,'Euclidean')

	if(maxlabels):
		quant = data.shape[0] / maxlabels
	else:
		quant = 'zero clusters'

	result_dict = {**json_datC,**json_datE,'no_clusters':str(maxlabels),'average_elements_per_cluster':str(quant)}
	# print(json_dat)
	jsonwritemode = 'w'
	if(os.path.isfile(outpath)):
		jsonwritemode = 'a'

	with jsonlines.open(outpath,jsonwritemode) as jw:
		jw.write(result_dict)

if __name__ == '__main__':
	main()