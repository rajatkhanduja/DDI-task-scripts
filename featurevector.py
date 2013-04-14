import string
import sys
import os

delim = ',;,'
dictwords = dict()

f = open("dictionary")
i = 0
for line in f:
	dictwords[line.strip()] = i
	i += 1
listwords = dictwords.keys()
f.close()

title = ['ID', 'Drug1', 'Drug2', 'Head1', 'Head2', '#words b/w 1 & 2']
title.extend(map(lambda x: str(x) + ' b/w 1 & 2', listwords))
title.extend(map(lambda x: str(x) + ' before 1', listwords))
title.extend(map(lambda x: str(x) + ' after 2', listwords))
title.extend(map(lambda x: str(x) + ' (noun) b/w 1 & 2', listwords))
title.extend(map(lambda x: str(x) + ' (verb) b/w 1 & 2', listwords))
title.append('interaction b/w 1 & 2')

def wordvector(words):
	lwords = words.split('|')
	lwordvector = [0] * len(listwords)
	for word in lwords:
		lwordvector[dictwords[word]] = 1
	return lwordvector

def writerow(g, l, d):
	for i in range(0, len(l) - 1):
		g.write(str(l[i]) + d)
	g.write(str(l[-1]) + '\n')

def makebool(s):
	if s == 'false':
		return 0
	elif s == 'true':
		return 1
	else:
		print "true/false expected."
		exit(3)

f = open("basicFeatures.csv")
g = open("/tmp/featurevector.csv", 'w')
writerow(g, title, delim)
lbf = []
for line in f:
	lresult = []
	lbf = line.strip().split(delim)
	lresult.extend(lbf[0:6])
	lresult.extend(wordvector(lbf[6]))
	lresult.extend(wordvector(lbf[7]))
	lresult.extend(wordvector(lbf[8]))
	lresult.extend(wordvector(lbf[9]))
	lresult.extend(wordvector(lbf[10]))
	lresult.append(makebool(lbf[11]))
	writerow(g, lresult, delim)
	assert(len(lresult) == len(title))
	break
