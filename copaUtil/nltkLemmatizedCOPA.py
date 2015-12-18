from xml.dom.minidom import parse
import xml.dom.minidom
from copaPyling import *

def declare_xml():
	return '<?xml version="1.0" encoding="UTF-8"?>'+separator()

def declare_dtd():
	return '<!DOCTYPE copa-corpus SYSTEM "copa.dtd">'+separator()

def start_corpus(corpus_name="copa-corpus", version="1.0"):
	return '<' + corpus_name + ' ' + 'version=' + '"' + version + '"' + '>' + separator()

def end_corpus(corpus_name="copa-corpus"):
	return '</' + corpus_name + '>' + separator()

def start_item(ID, direction, ans):
	return separator()+'  <item id=' + '"'+ ID +'" asks-for="'+direction+'"' + ' most-plausible-alternative='+'"'+ans+'">'+separator()

def end_item():
	return '  </item>'+separator()

def start_tag(tagname):
	return '    <' + tagname + '>'
	
def end_tag(tagname):
	return '</'+tagname+'>'+separator()

def separator():
	return '\n'

def process(document,outfile):
	DOMTree = xml.dom.minidom.parse(document)
        copaCorpus = DOMTree.documentElement
        items = copaCorpus.getElementsByTagName("item")
	
	outf = open(outfile,'w')
	outf.write(declare_xml())
	outf.write(declare_dtd())
	outf.write(start_corpus())
	
	for item in items:
		ID = item.getAttribute("id")
                direction = item.getAttribute("asks-for")
		ans = item.getAttribute("most-plausible-alternative")
                q = item.getElementsByTagName('p')[0].childNodes[0].data
                a1 = item.getElementsByTagName('a1')[0].childNodes[0].data
                a2 = item.getElementsByTagName('a2')[0].childNodes[0].data
		lemq = lemmatizer(q)
	#	print lemq
		lema1 = lemmatizer(a1)
		#print lema1
		lema2 = lemmatizer(a2)
		#print lema2
		outf.write(start_item(ID,direction,ans))
		outf.write(start_tag("p"))
		outf.write(lemq)
		outf.write(end_tag("p"))
		outf.write(start_tag("a1"))
		outf.write(lema1)
		outf.write(end_tag("a1"))
		outf.write(start_tag("a2"))
		outf.write(lema2)
		outf.write(end_tag("a2"))
		outf.write(end_item())
		
	outf.write(end_corpus())
	outf.close()

if __name__=="__main__":
#	process("/home/jessie/public_html/docs/copa-all.xml","/home/jessie/code/copa/nltk-copa-all.xml")
	process("/home/jessie/code/copa/res/data/copaReplace6.xml","/home/jessie/code/copa/res/data/yuchen-nltk-copa-all.xml")
