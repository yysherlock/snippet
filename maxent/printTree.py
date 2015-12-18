import Tree

filename = 'small_parsed_data.txt'
f = open(filename,'r')

for line in f:
	#print line
	contents = line.strip().split('\t')
	nodes = ['0/null/null/null/0']
	nodes.extend(contents)
	tree = Tree.build_tree(nodes)
	sent = ""
	for i in range(1,len(tree.sentence)):
		sent+=tree.sentence[i].word
		sent+=" "
	
	print sent
	tree.printTree(tree.get_node(0))
	tree.treestr = tree.treestr.replace('null/null/null','Tree: \n')
	print tree.treestr + '\n'

