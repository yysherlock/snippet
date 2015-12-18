from nltkLemmatizedCOPA import *

def convertDcoref2CopaDoc(CopaDoc,dcorefCopaDoc,outfile):
	tag = ['p','a1','a2']

	outf = open(outfile,'w')
	outf.write(declare_xml())
        outf.write(declare_dtd())
        outf.write(start_corpus())
	outf.write('  <item id="1" asks-for="cause" most-plausible-alternative="1">\n')
	
	DOMTree = xml.dom.minidom.parse(CopaDoc)
        copaCorpus = DOMTree.documentElement
        items = copaCorpus.getElementsByTagName("item")
	startItem = items[0]
	startID = startItem.getAttribute("id")
        startdirection = startItem.getAttribute("asks-for")
        startans = startItem.getAttribute("most-plausible-alternative")
	
	inf = open(dcorefCopaDoc,'r')
	senindx = -1
	itemindx = 0
	
	for line in inf:
		senindx += 1
		
		if senindx % 4 == 3:
			if senindx > 0:
				outf.write(end_item())
			if senindx == 0:
				outf.write(start_item(startID, startdirection, startans))

			itemindx += 1
			
			if itemindx >= items.length:
				break
			item = items[itemindx]
			
			ID = item.getAttribute("id")
                	direction = item.getAttribute("asks-for")
                	ans = item.getAttribute("most-plausible-alternative")
			
			outf.write(start_item(ID,direction,ans))
		else:
			#sentences[senindx % 3] = line.trim()
			lemSen = lemmatizer(line.strip())
			outf.write(start_tag(tag[senindx % 4]))
               		outf.write(lemSen)
                	outf.write(end_tag(tag[senindx % 4]))
	
	outf.write(end_corpus())
        outf.close()					

if __name__ == "__main__":
 	#convertDcoref2CopaDoc('../copa-all.xml','/home/jessie/public_html/docs/dcoref-all-v2.txt','nltk-copa-all.xml')
	#convertDcoref2CopaDoc('../copa-all.xml','yuchen-dcoref-all.txt','../res/data/yuchen-nltk-copa-all.xml')
	convertDcoref2CopaDoc('../correct-copa-all.xml','correct-dcoref-all.txt','../res/data/correct-nltk-copa-all.xml')
