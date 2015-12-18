copawordlist = []
wordlist = []
formlist = []
dic = {}

with open('copawordlist.txt','r') as f:
	for line in f:
		copawordlist.append(line.strip().lower())

with open('e_lemma_file.txt','r') as f:
        for line in f:
		line = line.lower()
                if line.startswith(';'):
                        continue
		if line.find(" -> ") == -1:
			a = []
			a.append(line.strip())

			if line.strip() not in dic.keys():
                        	dic[line.strip()] = a
			continue
                word,forms = line.strip().split(' -> ')
		
                forms = forms.strip().split(',')
		l = []
		l.append(word)
		l.extend(forms)

		if word.strip() not in dic.keys():
			dic[word.strip()] = l
			for form in forms:
				if form not in dic.keys():
					dic[form] = l


with open('copadict.txt','w') as outf:
	
	for word in copawordlist:
		if word not in dic.keys():
			print word
		else :
			for w in dic[word]:
				outf.write(w+'\n')
		
