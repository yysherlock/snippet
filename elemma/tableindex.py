
outf = open("table1.txt","w")
index = 0
with open('copawordlist.txt','r') as f:
	for line in f:
		outf.write(line.strip()+"\t"+str(index)+"\n")
		index += 1
outf.close()
