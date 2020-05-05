import jsonlines
import sys
from dlib import Ranker
from nltk import word_tokenize
import collections, itertools

def process_drivers(driverlist,option,num=5):
	drivers_score = collections.defaultdict(int)
	drs = set()
	if(option == 'intersect'):
		for drivers in driverlist:
			drs = drs.intersection(set(drivers))
	elif(option == 'union'):
		for drivers in driverlist:
			drs = drs.union(set(drivers))
	elif(option == 'frequency'):
		for driver in itertools.chain.from_iterable(driverlist):
			drivers_score[driver] += 1
		drs = list({k for k, v in sorted(drivers_score.items(), key=lambda item: item[1])})[-num:]
	else:
		print('invalid option!')
		return []
	return list(drs)

def get_driver_dict(drivers,label):
	return {'label':label,'drivers':drivers}

def do_lookups_and_collect_drivers(tokar,drivertok,ranker,num):
	collec_drivers = []
	for tok in tokar:
		results = ranker.article2queries(tok,drivertok,num)
		temdrivers = [res['driver'] for res in results]
		collec_drivers.append(temdrivers)	
	return collec_drivers

def process_cluster(article_cluster,drivers,ranker,option='average',num=5):

	if(option!='average' and option!='intersect' and option != 'union' and option != 'frequency'):
		print('invalid option entered!')
		return []

	articles = article_cluster['articles']
	tokar = []
	collec_drivers = []
	drivertok = [word_tokenize(driver) for driver in drivers]
	if(option == 'average'):
		for article in articles:
			tokar += word_tokenize(article)

		results = ranker.article2queries(tokar,drivertok,num)
		ret_drivers = [res['driver'] for res in results]
		return get_driver_dict(ret_drivers,article_cluster['label'])
	
	for article in articles:
		tokar.append(word_tokenize(article))
	
	collec_drivers = do_lookups_and_collect_drivers(tokar,drivertok,ranker,num)
	
	ret_drivers = process_drivers(collec_drivers,option,num)
	return get_driver_dict(ret_drivers,article_cluster['label'])

def main():
	inputpath = sys.argv[1]
	driverpath = sys.argv[2]
	outputpath = sys.argv[3]
	option = sys.argv[4]
	num = int(sys.argv[5])

	ranker = Ranker('data/best_weights','data')

	article_clusters = []

	with open(driverpath,'r') as drv:
		drivers = drv.readlines()
		drivers = [driver.strip() for driver in drivers]

	with jsonlines.open(inputpath,'r') as jr:
		for line in jr:
			article_clusters.append(line)

	with jsonlines.open(outputpath,'w') as jw:
		for article_cluster in article_clusters:
			cluster_result = process_cluster(article_cluster,drivers,ranker,option,num)
			jw.write(cluster_result)

if __name__ == '__main__':
	main()