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

#def build_tree1(nodes):
#        tree = Tree(nodes)
#        return tree


class Tree:

        def __init__(self, nodes, clst=[], elst=[], plst=[]):
                
                self.treestr = ""
                self.sentence = []

                for node in nodes:
                        index,word,postag,deprel,headidx = parse_node(node)
                        treenode = TreeNode(index,word,postag,deprel,headidx)
                        self.sentence.append(treenode)

                # second pass, build children list for each node
                for node in nodes:
                        index,word,postag,deprel,headidx = parse_node(node)
                        self.sentence[int(headidx)].children.append(int(index))
                
                if clst==[] and elst==[] and plst==[]:
                        pass
                else:
                        # label for each treenode
                        for elem in clst: self.sentence[elem].label = 'C'
                        for elem in elst: self.sentence[elem].label = 'E'

        def addlabel(self,clst,elst,plst):
                # label for each treenode
                for elem in clst: self.sentence[elem].label = 'C'
                for elem in elst: self.sentence[elem].label = 'E'

        def get_node(self,i):
                return self.sentence[i] # return the node of index i

        def get_head(self,i): # return node (the head of node i)
                return self.sentence[self.get_node(i).headidx]
        
        def add_level(self,root, level):
                root.level = level
                for i in range(1,len(self.sentence)):
                        if self.sentence[i].headidx == root.index:
                                self.add_level(self.sentence[i], level + 1)
        

        def printSpace(self,level):
                self.treestr += "\n"
                for i in range(level):
                        self.treestr += "    "

        def printTree(self,root,level = 0):
                self.treestr += str(root)
                for i in range(1,len(self.sentence)):
                        if self.sentence[i].headidx == root.index:
                                self.printSpace(level+1)
                                #print "["
                                self.treestr+="["
                                self.printTree(self.sentence[i],level + 1)
                                #print "]"
                                self.treestr+="]"


class TreeNode:

        def __init__(self, index, word, postag, deprel, headidx, children=[],label='N', level = 0):
                self.index = int(index)
                self.word = word
                self.postag = postag
                self.deprel = deprel
                self.headidx = int(headidx)
                self.children = []
                self.label = label
                self.level = level

        def __str__(self):
                return self.word+'/'+self.postag+'/'+self.deprel

