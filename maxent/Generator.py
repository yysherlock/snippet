from nltk.corpus import wordnet as wn

validpos = ("verb","VB","VBN","VBD","VBG","VBP","VBZ","noun","NN", "NNS", "NNP", "NNPS","adjective","JJ", "JJS", "JJR","adverb","RB", "RBS", "RBR")
verbposlst = ["VB","VBN","VBD","VBG","VBP","VBZ"]
nounposlst = ["NN", "NNS", "NNP", "NNPS"]
adjposlst = ["JJ", "JJS", "JJR"]
advposlst = ["RB", "RBS", "RBR"]

tagmap = dict(zip(verbposlst+nounposlst+adjposlst+advposlst,['v']*len(verbposlst)+['n']*len(nounposlst)+['a']*len(adjposlst)+['r']*len(advposlst)))

scfeat = set({})
def load_scfeat(filename):
	f = open(filename)
	for line in f:
		scfeat.add(line.strip().split()[0])
load_scfeat('scfeat_l2.txt') # scfeat_s1.txt - 9 classes
print 'scfeat: ',scfeat
print tagmap

def get_scfeat(word,pos): # pos here is short version e.g. 'n','v','a','r'
	# return least subsumers of each path in scfeat
	features = set({})
	word_synsets = wn.synsets(word,pos)
	for syn in word_synsets:
		paths = syn.hypernym_paths()
		for path in paths:
			for i in range(1,len(path)+1):
				s = str(path[-i])
				if s in scfeat:
					features.add(s)
					break
	return list(features)

def build_tree(nodes):
	tree = Tree(nodes)
	return tree

def valid(treenode):
	#global validpos
	#if treenode.postag in validpos:
	#	return True
	#return False
	return True

def get_context_9wnclasses(w,tree,cat):
	context = []
	curnode = tree.sentence[w]

	if curnode.postag in tagmap:
		for feature in get_scfeat(curnode.word,tagmap[curnode.postag]):
			context.append('curwordsf='+feature)

	head_1 = tree.get_head(w)
	if head_1.postag in tagmap:
		scflst = get_scfeat(head_1.word,tagmap[head_1.postag])
		for feature in scflst:
			context.append('head-1sf='+feature)
	
	if head_1.index > 0:
		head_2 = tree.get_head(head_1.index)
		if head_2.postag in tagmap:
			for feature in get_scfeat(head_2.word,tagmap[head_2.postag]):
				context.append('head-2sf='+feature)
		
	else:
		context.append('head-2sf='+'BOUNDARY')

	if w > 1:
		word_1 = tree.get_node(w-1)
		if word_1.postag in tagmap:
			for feature in get_scfeat(word_1.word,tagmap[word_1.postag]):
				context.append('word-1sf='+feature)
		
		if w > 2:
			word_2 = tree.get_node(w-2)
			if word_2.postag in tagmap:
				for feature in get_scfeat(word_2.word,tagmap[word_2.postag]):
					context.append('word-2sf='+feature)
			context.append('cat-2='+cat[w-2])
		else:
			context.append('word-2sf='+'BOUNDARY')
			context.append('cat-2='+'BOUNDARY')
	else:
		context.append('word-1,2sf='+'BOUNDARY,BOUNDARY')
		context.append('cat-1,2='+'BOUNDARY,BOUNDARY')
	
	n = len(tree.sentence)
	
	if w + 1 < n:
		wordn1 = tree.get_node(w+1)
		if wordn1.postag in tagmap:
			for feature in get_scfeat(wordn1.word,tagmap[wordn1.postag]):
				context.append('word+1sf='+feature)
		
		if w + 2 < n:
			wordn2 = tree.get_node(w+2)
			if wordn2.postag in tagmap:
				for feature in get_scfeat(wordn2.word,tagmap[wordn2.postag]):
					context.append('word+2sf='+feature)
		else:
			context.append('word+2sf=BOUNDARY')
		
	else:
		context.append('word+1,2sf=BOUNDARY,BOUNDARY')
		
	return context

def get_context_wordform(w,tree,cat):
	context = []
	curnode = tree.sentence[w]
	context.append('curword='+curnode.word)

	head_1 = tree.get_head(w)
	context.append('head-1='+head_1.word)

	if head_1.index > 0:
		head_2 = tree.get_head(head_1.index)
		context.append('head-2='+head_2.word)
		
	else:
		context.append('head-2='+'BOUNDARY')

	if w > 1:
		word_1 = tree.get_node(w-1)
		context.append('word-1='+word_1.word)

		if w > 2:
			word_2 = tree.get_node(w-2)
			context.append('word-2='+word_2.word)
		#	context.append('cat-2='+cat[w-2])
		else:
			context.append('word-2='+'BOUNDARY')
		#	context.append('cat-2='+'BOUNDARY')
	else:
		context.append('word-1,2='+'BOUNDARY,BOUNDARY')
		#context.append('cat-1,2='+'BOUNDARY,BOUNDARY')

	n = len(tree.sentence)
	
	if w + 1 < n:
		wordn1 = tree.get_node(w+1)
		context.append('word+1=' + wordn1.word)
		
		if w + 2 < n:
			wordn2 = tree.get_node(w+2)
			context.append('word+2=' + wordn2.word)
		else:
			context.append('word+2=BOUNDARY')
		
	else:
		context.append('word+1,2=BOUNDARY,BOUNDARY')
	
	return context

def get_context_syntactic(w,tree,cat):
	context = []
	curnode = tree.sentence[w]
	context.append('curpostag='+curnode.postag)
	context.append('curdeprel='+curnode.deprel)
	
	head_1 = tree.get_head(w)
	
	context.append('head-1postag='+head_1.postag)
	context.append('head-1deprel='+head_1.deprel)

	if head_1.index > 0:
		head_2 = tree.get_head(head_1.index)
		context.append('head-2postag='+head_2.postag)
		context.append('head-2deprel='+head_2.deprel)
	else:
		context.append('head-2='+'BOUNDARY')
		
	if w > 1:
		word_1 = tree.get_node(w-1)
		context.append('word-1postag='+word_1.postag)
		context.append('word-1deprel='+word_1.deprel)
		
		if w > 2:
			word_2 = tree.get_node(w-2)
			context.append('word-2postag='+word_2.postag)
			context.append('word-2deprel='+word_2.deprel)
		#	context.append('cat-2='+cat[w-2])
		else:
			context.append('word-2postag='+'BOUNDARY')
			context.append('word-2deprel='+'BOUNDARY')
		#	context.append('cat-2='+'BOUNDARY')
	else:
		context.append('word-1,2postag='+'BOUNDARY,BOUNDARY')
		context.append('word-1,2deprel='+'BOUNDARY,BOUNDARY')
	#	context.append('cat-1,2='+'BOUNDARY,BOUNDARY')
	
	n = len(tree.sentence)
	
	if w + 1 < n:
		wordn1 = tree.get_node(w+1)
		context.append('word+1postag='+wordn1.postag)
		context.append('word+1deprel='+wordn1.deprel)
		
		if w + 2 < n:
			wordn2 = tree.get_node(w+2)
			context.append('word+2postag='+wordn2.postag)
			context.append('word+2deprel='+wordn2.deprel)
		else:
			context.append('word+2postag='+'BOUNDARY')
			context.append('word+2deprel='+'BOUNDARY')
	else:
		context.append('word+1,2postag='+'BOUNDARY,BOUNDARY')
		context.append('word+1,2deprel='+'BOUNDARY,BOUNDARY')
	
	return context

def get_context1(w,tree,cat):
	"""get context for w
	features: semantic features added.
	"""
	context = []
	curnode = tree.sentence[w]
	context.append('curword='+curnode.word)
	context.append('curpostag='+curnode.postag)
	context.append('curdeprel='+curnode.deprel)

	if curnode.postag in tagmap:
		for feature in get_scfeat(curnode.word,tagmap[curnode.postag]):
			context.append('curwordsf='+feature)

	head_1 = tree.get_head(w)
	context.append('head-1='+head_1.word)
	##print 'head_1 pos:',head_1.postag, tagmap.get(head_1.postag,"NOT in tagmap")
	if head_1.postag in tagmap:
		scflst = get_scfeat(head_1.word,tagmap[head_1.postag])
		for feature in scflst:
			context.append('head-1sf='+feature)
	
	context.append('head-1postag='+head_1.postag)
	context.append('head-1deprel='+head_1.deprel)

	if head_1.index > 0:
		head_2 = tree.get_head(head_1.index)
		context.append('head-2='+head_2.word)
		if head_2.postag in tagmap:
			for feature in get_scfeat(head_2.word,tagmap[head_2.postag]):
				context.append('head-2sf='+feature)
		context.append('head-2postag='+head_2.postag)
		context.append('head-2deprel='+head_2.deprel)
	else:
		context.append('head-2='+'BOUNDARY')
		context.append('head-2sf='+'BOUNDARY')

	if w > 1:
		word_1 = tree.get_node(w-1)
		context.append('word-1='+word_1.word)
		if word_1.postag in tagmap:
			for feature in get_scfeat(word_1.word,tagmap[word_1.postag]):
				context.append('word-1sf='+feature)
		context.append('word-1postag='+word_1.postag)
		context.append('word-1deprel='+word_1.deprel)
		
		if w > 2:
			word_2 = tree.get_node(w-2)
			context.append('word-2='+word_2.word)
			if word_2.postag in tagmap:
				for feature in get_scfeat(word_2.word,tagmap[word_2.postag]):
					context.append('word-2sf='+feature)
			context.append('word-2postag='+word_2.postag)
			context.append('word-2deprel='+word_2.deprel)
			context.append('cat-2='+cat[w-2])
		else:
			context.append('word-2='+'BOUNDARY')
			context.append('word-2sf='+'BOUNDARY')
			context.append('word-2postag='+'BOUNDARY')
			context.append('word-2deprel='+'BOUNDARY')
			context.append('cat-2='+'BOUNDARY')
	else:
		context.append('word-1,2='+'BOUNDARY,BOUNDARY')
		context.append('word-1,2sf='+'BOUNDARY,BOUNDARY')
		context.append('word-1,2postag='+'BOUNDARY,BOUNDARY')
		context.append('word-1,2deprel='+'BOUNDARY,BOUNDARY')
		context.append('cat-1,2='+'BOUNDARY,BOUNDARY')
	
	n = len(tree.sentence)
	
	if w + 1 < n:
		wordn1 = tree.get_node(w+1)
		context.append('word+1=' + wordn1.word)
		if wordn1.postag in tagmap:
			for feature in get_scfeat(wordn1.word,tagmap[wordn1.postag]):
				context.append('word+1sf='+feature)
		context.append('word+1postag='+wordn1.postag)
		context.append('word+1deprel='+wordn1.deprel)
		
		if w + 2 < n:
			wordn2 = tree.get_node(w+2)
			context.append('word+2=' + wordn2.word)
			#print 'postag: ',wordn2.word,wordn2.postag,wordn2.deprel
			if wordn2.postag in tagmap:
				for feature in get_scfeat(wordn2.word,tagmap[wordn2.postag]):
					context.append('word+2sf='+feature)
			context.append('word+2postag='+wordn2.postag)
			context.append('word+2deprel='+wordn2.deprel)
		else:
			context.append('word+2=BOUNDARY')
			context.append('word+2sf=BOUNDARY')
			context.append('word+2postag='+'BOUNDARY')
			context.append('word+2deprel='+'BOUNDARY')
	else:
		context.append('word+1,2=BOUNDARY,BOUNDARY')
		context.append('word+1,2sf=BOUNDARY,BOUNDARY')
		context.append('word+1,2postag='+'BOUNDARY,BOUNDARY')
		context.append('word+1,2deprel='+'BOUNDARY,BOUNDARY')
	
	return context

def get_context(w,tree,cat):
    """get context for w"""
    context = []
    curnode = tree.sentence[w]

    if valid(curnode):
    	context.append('curword='+curnode.word)
    	#context.append('childrennum='+str(len(curnode.children)))
    	context.append('curpostag='+curnode.postag)
	context.append('curdeprel='+curnode.deprel)
	
    	head_1 = tree.get_head(w)

    	context.append('head-1='+head_1.word)
    	context.append('head-1postag='+head_1.postag)
    	context.append('head-1deprel='+head_1.deprel)
	#print cat,"  ",head_1.index, "  ",[ x.word for x in tree.sentence[1:len(cat)+1]]
    	#context.append('head-1cat='+cat[head_1.index])
    	
    	if head_1.index > 0:
    		head_2 = tree.get_head(head_1.index)
    		context.append('head-2='+head_2.word)
    		context.append('head-2postag='+head_2.postag)
    		context.append('head-2deprel='+head_2.deprel)
    	#	context.append('head-2cat='+cat[head_2.index])
    	else:
    		context.append('head-2='+'BOUNDARY')
    	#	context.append('head-2cat='+'BOUNDARY')

    	if w > 1:
    		word_1 = tree.get_node(w-1)
    		context.append('word-1='+word_1.word)
    		context.append('word-1postag='+word_1.postag)
    		context.append('word-1deprel='+word_1.deprel)
    		context.append('cat-1='+cat[w-1])

    		if w > 2:
    			word_2 = tree.get_node(w-2)
    			context.append('word-2='+word_2.word)
    			context.append('word-2postag='+word_2.postag)
    			context.append('word-2deprel='+word_2.deprel)
    			context.append('cat-2='+cat[w-2])
    		else:
    			context.append('word-2='+'BOUNDARY')
    			context.append('word-2postag='+'BOUNDARY')
    			context.append('word-2deprel='+'BOUNDARY')
    			context.append('cat-2='+'BOUNDARY')
    	else:
    		context.append('word-1,2='+'BOUNDARY,BOUNDARY')
    		context.append('word-1,2postag='+'BOUNDARY,BOUNDARY')
    		context.append('word-1,2deprel='+'BOUNDARY,BOUNDARY')
    		context.append('cat-1,2='+'BOUNDARY,BOUNDARY')
    	
    	n = len(tree.sentence)

    	if w + 1 < n:
    		wordn1 = tree.get_node(w+1)
    		context.append('word+1=' + wordn1.word)
    		context.append('word+1postag='+wordn1.postag)
    		context.append('word+1deprel='+wordn1.deprel)
    	#	context.append('cat+1='+cat[w+1])

	        if w + 2 < n:
	       		wordn2 = tree.get_node(w+2)
	        	context.append('word+2=' + wordn2.word)
	            	context.append('word+2postag='+wordn2.postag)
    			context.append('word+2deprel='+wordn2.deprel)
    	#		context.append('cat+2='+cat[w+2])
	        else:
	            	context.append('word+2=BOUNDARY')
	            	context.append('word+2postag='+'BOUNDARY')
	            	context.append('word+2deprel='+'BOUNDARY')
	 #           	context.append('cat+2='+'BOUNDARY')
	else:
		
	        context.append('word+1,2=BOUNDARY,BOUNDARY')
	        context.append('word+1,2postag='+'BOUNDARY,BOUNDARY')
	        context.append('word+1,2deprel='+'BOUNDARY,BOUNDARY')
#	        context.append('cat+1,2='+'BOUNDARY,BOUNDARY')

    return context

def parse_node(node):
	r1 = node.rfind('/')
	headidx = node[r1+1:]
        node = node[:r1]
        r2 = node.rfind('/')
        deprel = node[r2+1:]
        node = node[:r2]
        r3 = node.rfind('/')
        postag = node[r3+1:]
        node = node[:r3]
        r4 = node.find('/')
        index = node[:r4]
        word = node[r4+1:]
	return (index,word,postag,deprel,headidx)

class Tree:

	def __init__(self, nodes):
		self.treestr = ""
		self.sentence = []
		for node in nodes:
			#print node
			index,word,postag,deprel,headidx = parse_node(node)
			treenode = TreeNode(index,word,postag,deprel,headidx)
			self.sentence.append(treenode)

		# second pass, build children list for each node
		for node in nodes:
			index,word,postag,deprel,headidx = parse_node(node)
			self.sentence[int(headidx)].children.append(int(index))
		#for node in self.sentence:
		#	print "children:", node.children

	def get_node(self,i):
		return self.sentence[i] # return the node of index i

	def get_head(self,i): # return node (the head of node i)
		return self.sentence[self.get_node(i).headidx]


	def printSpace(self,level):
		print '\n'
		self.treestr += '\n'

		for i in range(level):
			print "    "
			self.treestr += "  "

	def printTree(self,root):
		print str(root)
		treestr += str(root)
		for i in range(1,len(self.sentence)):
			if self.sentence[i].headidx == root.index:
				printSpace(level+1)
				print "["
				treestr+="["
				printTree(self.sentence[i],level+1)
				print "]"
				treestr+="]"
		
	
class TreeNode:

	def __init__(self, index, word, postag, deprel, headidx, children=[]):
		self.index = int(index)
		self.word = word
		self.postag = postag
		self.deprel = deprel
		self.headidx = int(headidx)
		self.children = []
	
	def __str__(self):
		return self.word+'/'+self.postag+'/'+self.deprel
