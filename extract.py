import sys
from nltk.corpus import wordnet as wn
import matcher
import RoledTree

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
wordset = set({})
# load wordset
wlf = open('wordlist.txt')
for line in wlf:
        wordset.add(line.strip())

def get_form(wordsurface,pos):
        """ pos: wn.NOUN = 'n', wn.VERB = 'v', wn.ADJ='a', wn.ADV='r'
        we use this function to map wordsurface to word form
        """
        wordsurface = wordsurface.lower()
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
        candidate_nodes = [node for node in candidate_nodes if node.postag in validpos]
        thred_level = select([node.level for node in candidate_nodes],2)
        return [node for node in candidate_nodes if node.level <= thred_level]

#parsed_filename = "small_parsed_data.txt" #"parsed_csdata_aa"#"small_parsed_data.txt" #"ss.txt" #"small_parsed_data.txt"
parsed_filename = sys.argv[1]
output_filename = sys.argv[2]
print parsed_filename
print output_filename

parsed_file = open(parsed_filename)
#f2 = open("small_causalpair.txt", "w")
f2 = open(output_filename, 'w')

line_num = 0
for line in parsed_file:
	line_num += 1
        contents = line.strip().split('\t')
        nodes = ['0/null/null/null/0']
        nodes.extend(contents)
        tree = RoledTree.Tree(nodes)
        tree.add_level(tree.sentence[0], 0)

        sent = ['null']
        for i in range(1,len(nodes)):
                sent.append(tree.sentence[i].word)
        for pattern in pattern_lst:
                clst,elst,plst = pattern.match(sent)
                if plst == []: continue
                else:
			if line_num % 10000 == 0 : print line_num
			plst = sorted(plst)
			causalrange = [plst[0]-1-i for i in range(10)] + [plst[-1]+1+i for i in range(10)]
			clst = list(set(clst).intersection(set(causalrange)))
			elst = list(set(elst).intersection(set(causalrange)))
			if len(clst) == 0 or len(elst) == 0:
				continue
                        tree.addlabel(clst,elst,plst)
                        cnodes = extract([tree.sentence[elem] for elem in clst])
                        enodes = extract([tree.sentence[elem] for elem in elst])
			cwords = []
			ewords = []			
			for node in cnodes:
				word = get_form(node.word,tagmap[node.postag])
				if word:
					cwords.append(word)
			for node in enodes:
				word = get_form(node.word,tagmap[node.postag])
				if word:
					ewords.append(word)
			tree.treestr = tree.treestr.replace('null/null/null','Tree: \n')                                 
			for cw in cwords:	
                                for ew in ewords:
                                	causalpair_map.setdefault(cw+'\t'+ew,0)
                                        causalpair_map[cw+'\t'+ew] += 1
#	if line_num > 10:
#		break
	if line_num%10000 == 0:
		print line_num

for k,v in causalpair_map.items():
#	print k+'\t'+str(v)
	f2.write(k+'\t'+str(v)+"\n")

parsed_file.close()
f2.close()						
