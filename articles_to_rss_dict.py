import jsonlines
import sys
from collections import defaultdict

inputpath = sys.argv[1]
outputpath = sys.argv[2]

compleat_dictionary = defaultdict(list)

with jsonlines.open(inputpath) as filer, jsonlines.open(outputpath,'w') as filew:
	for line in filer:
		compleat_dictionary[line['rss_link']].append(line)
	filew.write(compleat_dictionary)