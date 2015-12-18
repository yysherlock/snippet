import collections

wdic={}
orgmap = {}

Org = collections.namedtuple("Org","id orgword")

with open("e_lemma_file.txt","r") as f:
	
	cnt = 0
	for line in f:
		index = -1

		if line.startswith(';'):
			continue
		line = line.strip().lower()
		if line.find(" -> ") == -1:
			word = line
			forms = []
		else:
			word,forms = line.split(" -> ")
			forms = forms.split(",")

		group = []
		group.append(word)
		group.extend(forms)
		flag = False

		for w in group:
			if w in wdic.keys():
				index = wdic[w]
				flag = True
				break
		if flag:
			for w in group:
				wdic[w] = index	
		else :
			for w in group:
				wdic[w] = cnt

			orgmap[cnt] = group[0]
			cnt += 1


#with open("table.txt","w") as outf:
#	for w in wdic.keys():
#		outf.write(w+"\t"+str(wdic[w])+"\n")

with open("map.txt","w") as outf:
	for w in wdic.keys():
		outf.write(w+"\t"+orgmap[wdic[w]]+"\n")
		
