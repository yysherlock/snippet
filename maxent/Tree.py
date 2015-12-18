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

def build_tree(nodes):
        tree = Tree(nodes)
        return tree
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
                #       print "children:", node.children

        def get_node(self,i):
                return self.sentence[i] # return the node of index i

        def get_head(self,i): # return node (the head of node i)
                return self.sentence[self.get_node(i).headidx]


        def printSpace(self,level):
                self.treestr += "\n"
                for i in range(level):
                        self.treestr += "    "

        def printTree(self,root,level =0):

                self.treestr += str(root)
                for i in range(1,len(self.sentence)):
                        if self.sentence[i].headidx == root.index:
                                self.printSpace(level+1)
                                #print "["
                                self.treestr+="["
                                self.printTree(self.sentence[i],level + 1)
                                #print "]"
                                self.treestr+="]"

                

def printSpace(level):
                for i in range(level):
                        print "    "


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

