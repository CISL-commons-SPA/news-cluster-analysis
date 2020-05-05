import json
import sys
import jsonlines

inpath = sys.argv[1]
outpath = sys.argv[2]

lines = {}

def line_pross(drivers,num=0):
	tup = {}
	for d in drivers:
		tup[d] = drivers[num]
	return tup

with jsonlines.open(inpath,'r') as filer:
	for line in filer:
		drivers = line['drivers']
		lines = {**lines,**line_pross(drivers)}

with open(outpath,'w') as jr:
	json.dump(lines,jr)