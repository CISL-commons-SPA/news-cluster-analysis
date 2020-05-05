import json
import sys
import jsonlines
import csv

inpath= sys.argv[1]
outpath = sys.argv[2]

def pross_dict(pdict,line,ret):
	pdict[line] = ret.replace(',','')
	return 1

def pross_line(line):
	if(line[0] == ''):
		return line[5]
	elif(line[0] == 'k'):
		return line[1]
	else:
		return line[0]

pdict = {}

with open(inpath,'r') as filer:
	csr = csv.reader(filer)
	for i,line in enumerate(csr):
		if (i == 0):
			continue
		#print(line)
		#print(i)
		pross_dict(pdict,line[1],pross_line(line))

with open(outpath,'w') as jw:
	json.dump(pdict,jw)
