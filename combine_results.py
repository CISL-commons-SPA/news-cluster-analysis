import jsonlines
import sys

inpath = sys.argv[1]
outpath = sys.argv[2]

article_list = []

with jsonlines.open(inpath,'r') as filer, jsonlines.open(outpath,'w') as filw:
	for line in filer:
		for key in line.keys():
			for article in line[key]:
				article_list.append(article)

	print(len(article_list))
	filw.write_lines()