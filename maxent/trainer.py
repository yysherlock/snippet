import sys
from optparse import OptionParser
import Generator

try:
	from maxent import MaxentModel
except ImportError:
	from pymaxent import MaxentModel

feat_dict={}
m = None

def save_features(filename):
	f = open(filename,'w')
	for feat in feat_dict.keys():
		print >> f, feat_dict[feat],feat


def gather_feature(context,c):
	for pred in context:
		f = pred + '_' + c
        	feat_dict[f] = feat_dict.get(f, 0) + 1

def extract_feature(file,func):
	for line in file: # format: i j k l nodes splitted by '\t'
		# parse line
		contents = line.strip().split('\t')
		i,j,k,l = map(int,contents[0:4])
		if k<=j or i>j or k > l: continue # unvalid sentence
		nodes = ['0/null/null/null/0']
		nodes.extend(contents[4:])
		
		tree = Generator.build_tree(nodes)
		cat = []
		
		for w in range(len(nodes)):
			c = 'N'
			if w>0: 
				if w >= i and w <=j: c = 'C'
				if w >= k and w <= l: c = 'E'
			cat.append(c)

		for w in range(1,len(nodes)):
			
			# for every w (word index), we extract context/features for it
			context = get_context(w,tree,cat) # extract contexts from the dependency subtree where w belongs to
			print 'context of `',str(tree.sentence[w]),'`',context
			# feature incremental for feat_dict 
			func(context,cat[w])

def add_event(context,c):
	context = [pred for pred in context if pred+'_'+c in feat_dict]
	m.add_event(context,c)

def main():
	global feat_dict, m

	# parsing options{{{
	usage = "usage: %prog [options] model"
    	parser = OptionParser(usage)
    	parser.add_option("-f", "--file", type="string", dest="filename",
                    metavar="FILE",
                    help="train a Maxent model with data from FILE")
    	parser.add_option("-g", "--gaussian", type="float", default=0.0, 
            help="apply Gaussian penality when training \
            [default=0.0]")
    	parser.add_option("--iters", type="int", default=15,
                    help="how many iterations are required for training[default=15]")
    	(options, args) = parser.parse_args()
	#}}}

	if options.filename:
		file = open(options.filename)
    	else:
        	print 'training file not given'
        	parser.print_usage()
        	sys.exit(1)

    	if len(args) !=1:
        	print >> sys.stderr, 'model name not given'
        	parser.print_usage()
        	sys.exit(1)

	model_name = args[0]

	global get_context
	get_context = Generator.get_context_wordform # change this to use different features


    	print 'First pass: gather features'
	extract_feature(file,gather_feature)
	feature_file = model_name + '.features'
	print 'save features to file %s' % feature_file
	save_features(feature_file)

	print 'feat_dict: ',feat_dict

	file.seek(0)
	print 'Second pass: training model...'
	m = MaxentModel()
    	m.begin_add_event()
    	extract_feature(file, add_event)
	m.end_add_event()


    	m.train(options.iters, 'lbfgs', options.gaussian)
    	print 'training finished'

   	print 'saving tagger model to %s' % model_name,
    	m.save(model_name)
    	print 'done'

if __name__=="__main__":
	main()
