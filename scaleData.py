import random

selectlist = []
dic = {}
f = open('/home/zhiyi/data/compact8g.txt')
pairnum = 0
for line in f:
	cause,effect,freq = line.strip().split('\t')
	#dic[int(freq)] = cause+'\t'+effect 
	for i in range(int(freq)): selectlist.append(pairnum)
	pairnum+=1

# scale
length = len(selectlist)
def scaleData(scale,outfilename):
	with open(outfilename,'w') as outf:
		for i in range(int(scale*length)):
			idx = random.randrange(length)
			outf.write(str(selectlist[idx]))
			outf.write('\n')
				
scaleData(0.2, '0.2scaledidx.txt')
scaleData(0.4, '0.4scaledidx.txt')
scaleData(0.6, '0.6scaledidx.txt')
scaleData(0.8, '0.8scaledidx.txt')

