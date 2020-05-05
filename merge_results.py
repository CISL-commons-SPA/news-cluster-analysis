import json
import sys
import jsonlines
import csv

def process_path(lines,inpath):
	ldict = {}
	newlines = []
	with open(inpath,'r') as jr:
		ldict = json.load(jr)
	for line in lines:
		line.append(ldict[line[0]])
		newlines.append(line)
	return newlines


drivertxtfile = sys.argv[1]
outpath = sys.argv[2]

with open(drivertxtfile,'r') as filer:
	lines = filer.readlines()
	lines = [[line.strip()] for line in lines]

cols = []
cnt = 1
for i,path in enumerate(sys.argv):
	if (i == 0 or i == 1 or i == 2):
		continue;
	lines = process_path(lines,path)
	cols.append(cnt)
	cnt+=1

column_values = ['Original Value'] + ['Level' + str(k) for k in cols]
lines = [column_values] + lines 

with open(outpath,'w') as filew:
	csw = csv.writer(filew)
	for line in lines:
		csw.writerow(line)