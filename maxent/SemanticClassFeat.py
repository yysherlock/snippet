# generate all top semantic classes (synsets)
# express these synsets as its string format: for example, Synset('ring.v.01'),
# since it is easy for reading by program
# output these top semantic classes into file

# Other program should read this file to construct semantic features' list.

import sys
from nltk.corpus import wordnet as wn

if len(sys.argv) < 1:
	print 'please pass me the top levels you want to have'
	sys.exit(1)

top = int(sys.argv[1])
tagset = ['n','v','a','r']
semantic_classes = {} # synset_str:idx
for tag in tagset:
	word_synsets = list(wn.all_synsets(tag))
	for syn in word_synsets:
		paths = syn.hypernym_paths()
		for path in paths:
			k = min(top,len(path))
			for sc in path[0:k]:
				if str(sc) not in semantic_classes:
					semantic_classes[str(sc)] = len(semantic_classes)
		
outf = open('scfeat_l'+str(top)+'.txt','w')
for k,v in semantic_classes.items():
	outf.write(k+" "+str(v)+"\n")
outf.close()




