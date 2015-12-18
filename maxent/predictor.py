import sys
import cPickle
from optparse import OptionParser

try:
    from maxent import MaxentModel
except ImportError:
    from pymaxent import MaxentModel
import Generator

m = None

def predict_file(filein, fileout):

	for line in filein:
        	contents = line.strip().split('\t')
		nodes = ['0/null/null/null/0']
		nodes.extend(contents[4:])
		tree = Generator.build_tree(nodes)

		if len(tree.sentence) == 0: continue
        	results = predict_sentence(tree, 3)

        	assert (len(tree.sentence) == len(results))
        
        	for i in range(1,len(tree.sentence)):
            		w = tree.sentence[i].word
            		fileout.write('%s/%s ' % (w, results[i]))
        	print >> fileout

def predict_sentence(tree,N):

    	def insert(h,s): h.append(s)
    	def extract(h): return h.pop()
    	def advance(curcs, tree, i):
		#print curcs[0]," ",curcs[1]," ",i
		cs = predictword(tree,i,curcs[0]) # cs: category with score
        	r=[]
        	for t,score in cs :
			r.append([curcs[0]+[t], score*curcs[1]])
		return r
	n = len(tree.sentence)
	assert N > 0

	s = [[],1.0]
	h0 = []
	insert(h0,s)

	for i in range(n):
		sz = min(N, len(h0))
		#print "sz",sz
		h1 = []
		for j in range(sz):
			r = advance(extract(h0),tree,i)
			for x in r :
				insert(h1,x)
		h0 =h1
		h0.sort(lambda x,y:cmp(x[1],y[1]))

	return h0[-1][0]


def predictword(tree,i,hist):
    	assert tree
    	assert len(hist) == i

    	context = Generator.get_context(i,tree,hist)
    	result = m.eval_all(context)
    	return result

def main():

	usage = "usage: %prog [options] -m model file"
    	parser = OptionParser(usage)
	parser.add_option("-i","--input",type="string",
			help="test data as input")
    	parser.add_option("-o", "--output", type="string",
            help="write detector result to OUTPUT")
    	parser.add_option("-m", "--model", type="string", 
            help="load trained model from MODEL")
    	(options, args) = parser.parse_args()

	global m
	model = options.model
	m = MaxentModel()
	m.load(model)

	#in_file = sys.stdin
	if options.input:
    		in_file = open(options.input)
	else: 
		print >> sys.stderr,'not given input test data'
		sys.exit(1)
	
	if len(args) >=1:
        	tag_in_file = open(args[0])

    	out_file = sys.stdout
    
    	if options.output:
        	out_file = open(options.output, 'w')

    	predict_file(in_file,out_file)


if __name__=="__main__":
    	main()


