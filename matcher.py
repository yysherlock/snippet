#clst,elst,plst = matcher.pattern_match(sent)
# write code for the above line
import re

outf1 = open('pp.txt','w')
p1 = r'(\bis\b|\bwas\b|\bare\b|\bwere\b) (\ba\b|\bthe\b|\bone\b) (\breason\b|\breasons\b) (\bof\b|\bfor\b)'
p2 = [r'(\ba\b|\bthe\b|\bone\b) effect of\b',r'\bis\b|\bare\b|\bwas\b|\bwere\b']
p3 = [r'\bthe reasons? (\bfor\b|\bof\b)',r'\bis\b|\bare\b|\bwas\b|\bwere\b']

def load_pattern(pattern_file):
	pattern_map = []
	for line in pattern_file:
		aidx,bidx = 0,0
		patpairs = [] # list of tuples [[sidx1,eidx1],[sidx2,eidx2]]
		elems = line.strip().split()
		#print elems
		outf1.write(str(elems)+'\n')
		for i in range(len(elems)):
			if elems[i] == 'A': aidx = i
			elif elems[i] == 'B': bidx = i
			elif elems[i] == '#PS': patpairs.append([i])
			elif elems[i] == '#PE': patpairs[-1].append(i)
			else:
				pass
		pattern_map.append(Pattern(aidx,bidx,patpairs,elems))
	outf1.close()
	return pattern_map

def get_matchremain(s, patstr):
	newstart = s.find(patstr)+len(patstr)+1
	return (newstart==0,s[newstart:])

def match1(s,pattern): # match pattern: A/B p1 B/A
	old = pattern
	if '/' in pattern:
		x = re.search(p1, s)
		if x: 
			pattern = x.group()
			#print pattern
		else: return (-1,-1,-1,-1,[])
	if pattern[0]>='a' and pattern[0]<='z': 
		pattern = ' '+pattern+' '
	
	if s.find(pattern) == -1: return (-1,-1,-1,-1,[])
	pattern = old

	beforeboundary = s.find(pattern)
	afterboundary = s.find(pattern)+len(pattern)-1
	end1 = len(s[0:beforeboundary].strip().split())-1
	start1 = 1
	n = len(s.strip().split())
	start2 = n - len(s[afterboundary+1:].strip().split())
	end2 = n - 1
	plst = range(end1+1,start2)
	#print 'plst: ',plst,pattern
	return (start1,end1,start2,end2,plst)

def match2(s,p1str,p2str): # match pattern: p1 A p2 B
	old1,old2 = p1str,p2str
	if '/' in p1str and '/' in p2str:
		if p1str == 'a/the/one effect of': p = p2
		if p1str == 'the reason/reasons for/of': p = p3
		x = []
		#print s
		x.append(re.search(p[0], s))
		if x[0]:
			rs = get_matchremain(s, x[0].group())[1]
			x.append(re.search(p[1], rs))
			if x[1]: 
				p1str = x[0].group()
				p2str = x[1].group()
		if len(x)<2 or not x[1]:
			return (-1,-1,-1,-1,[])
		else:
			old1,old2 = p1str,p2str

	if p1str[0]>='a' and p1str[0]<='z': 
		p1str = ' '+p1str+' '
	if p2str[0]>='a' and p2str[0]<='z': 
		p2str = ' '+p2str+' '

	if s.find(p1str)==-1 or get_matchremain(s, p1str)[1].find(p2str)==-1:
		return (-1,-1,-1,-1,[])
	p1str,p2str = old1,old2

	before1 = s.find(p1str)
	after1 = s.find(p1str)+len(p1str)-1
	before2 = s.find(p2str) 
	after2 = s.find(p2str) + len(p2str) - 1
	n = len(s.strip().split())
	start1 = n - len(s[after1+1:].strip().split())
	end1 = len(s[0:before2].strip().split()) - 1
	start2 = n - len(s[after2+1:].strip().split())
	end2 = n - 1
	plst = range(1,start1)
	plst.extend(range(end1+1,start2))
	#print "match2: ",plst
	#print p1str,p2str
	return (start1,end1,start2,end2,plst)

class Pattern:

	def __init__(self, aidx, bidx, patpairs, elems):
		if aidx > bidx: self.order = 1
		else: self.order = 0
		
		self.patternparts = []
		for pair in patpairs:
			self.patternpart = ' '.join([elems[i] for i in range(pair[0]+1,pair[1])])
			self.patternparts.append(self.patternpart)
		
		#print self.patternparts

	def match(self, sent):
		
		sentformatch = ' '.join(sent).strip()
		plst = []
		i,j,k,l= -1,-1,-1,-1

		if len(self.patternparts)==1:
			patstr = self.patternparts[0]
			
			if self.order == 0: 
				i,j,k,l,plst = match1(sentformatch,patstr)
				#print 'i,j,k,l: ',i,j,k,l,plst
			else: 
				k,l,i,j,plst = match1(sentformatch,patstr)
				#print 'i,j,k,l: ',i,j,k,l,plst
		
		if len(self.patternparts)==2:
			p1str = self.patternparts[0].strip()
			p2str = self.patternparts[1].strip()
			if self.order == 0: 
				i,j,k,l,plst = match2(sentformatch,p1str,p2str)
			else: 
				k,l,i,j,plst = match2(sentformatch,p1str,p2str)

		clst = range(i,j+1)
		elst = range(k,l+1)
		#print 'cep: ',clst,elst,plst				
		return clst,elst,plst
		#ceindiceslst # [[causestartidx,causeendidx,effectstartidx,effectendidx],[],..]
		


