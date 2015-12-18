import sys
from nltk.corpus import wordnet as wn
import matcher
import Tree

invalidrel=("aux","cop")
validpos = ("verb","VB","VBN","VBD","VBG","VBP","VBZ","noun","NN", "NNS", "NNP", "NNPS","adjective","JJ", "JJS", "JJR","adverb","RB", "RBS", "RBR")
verbposlst = ["VB","VBN","VBD","VBG","VBP","VBZ"]
nounposlst = ["NN", "NNS", "NNP", "NNPS"]
adjposlst = ["JJ", "JJS", "JJR"]
advposlst = ["RB", "RBS", "RBR"]

tagmap = dict(zip(verbposlst+nounposlst+adjposlst+advposlst,['v']*len(verbposlst)+['n']*len(nounposlst)+['a']*len(adjposlst)+['r']*len(advposlst)))
causalpair_map = {} # cause\teffect:freq
pattern_file = open('pattern_formalized.txt')
pattern_lst = matcher.load_pattern(pattern_file)

def get_form(wordsurface,pos):
	""" pos: wn.NOUN = 'n', wn.VERB = 'v', wn.ADJ='a', wn.ADV='r'
	we use this function to map wordsurface to word form
	"""
	wordsurface = wordsurface.lower()
	#print wordsurface
	wform = ""
	try:
		wform = wn.morphy(wordsurface,pos)
	except:
		return ""
	return wform

def select(lst,k): # select #k min element
	lst = sorted(lst)
	#print k,lst
	if len(lst)==0: return -1
	return lst[min(k-1,len(lst)-1)]

def extract(candidate_nodes):
	# filter, reserve n,v,a,r
	candidate_nodes = [node for node in candidate_nodes if node.postag in validpos and node.deprel not in invalidrel]
	thred_level = select([node.level for node in candidate_nodes],2)
	return [node for node in candidate_nodes if node.level <= thred_level]

#parsed_filename = "1.txt"
filedir = "./"
parsed_filename = "small_parsed_data.txt"
parsed_file = open(filedir+parsed_filename)

notmatchf = open(parsed_filename+'_notmatch_psentences.txt','w')

for line in parsed_file:
	contents = line.strip().split('\t')
	nodes = ['0/null/null/null/0']
	nodes.extend(contents)

	# construct sentence `sent` list of word
	tree = Tree.Tree(nodes)
	tree.add_level(tree.sentence[0], 0)

	sent = ['null']
	for i in range(1,len(nodes)):
		sent.append(tree.sentence[i].word)
		#print sent[i],tree.sentence[i].level # check add_level
	# sys.exit(0)

	matched = False

	for pattern in pattern_lst:
		# match pattern, identify 'C' 'E' 'P','N' nodes, return three lists of indices
		# e.g. clst = [1,2,3,..] elst, plst, index start from 1 since sent[0]='null'
		clst,elst,plst = pattern.match(sent)

		if plst == []: continue
		else:
			matched = True
		#	print nodes
		#	print 'clst: ',clst
		#	print [sent[i] for i in clst]
		#	print 'elst: ',elst
		#	print [sent[i] for i in elst]
		#	print 'plst: ',plst
		#	print [sent[i] for i in plst]

			tree.addlabel(clst,elst,plst)

			cnodes = extract([tree.sentence[elem] for elem in clst])
			enodes = extract([tree.sentence[elem] for elem in elst])
			cwords = [get_form(node.word,tagmap[node.postag]) for node in cnodes]
			ewords = [get_form(node.word,tagmap[node.postag]) for node in enodes]
			#print 'cwords: ',cwords
			#print 'ewords: ', ewords
			for cw in cwords:
				if cw:
					for ew in ewords:
						if ew:
							causalpair_map.setdefault(cw+'\t'+ew,0)
							causalpair_map[cw+'\t'+ew] += 1

			#sys.exit(0)
			break
			sys.exit(0)

	if not matched:
		notmatchf.write(' '.join(sent)+'\n')

notmatchf.close()

outf = open(parsed_filename+'_causal_pairs.txt','w')

for k,v in causalpair_map.items():
	outf.write(k+'\t'+str(v)+'\n')


outf.close()



