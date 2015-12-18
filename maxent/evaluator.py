
from optparse import OptionParser

acc = 0.0
precision, recall = 0.0,0.0

def evaluate1(predict_file, golden_file):
	""" evalute by word with format1, trian_data as golden_data"""

	correct  = 0
	precision = 0.0
	recall = 0.0
	TCE,FCE,TN,FN = 0,0,0,0

	tot = 0
	for line1 in predict_file:
		line2 = golden_file.readline()
		golden_cat = ['N']*(len(line2.strip().split('\t')) - 4 + 1)
		i,j,k,l = map(int,line2.strip().split('\t')[0:4])
		for idx in range(i,j+1): golden_cat[idx] = 'C'
		for idx in range(k,l+1): golden_cat[idx] = 'E'
		
		golden_cat = golden_cat[1:]

		predict_cat = []
		predictedowrds = line1.strip().split()
		
		for word in predictedowrds:
			predict_cat.append(word[-1])
		
		# add by force
		#predict_cat[-1]='N'

		print golden_cat,"\n",predict_cat,"\n"

		assert len(golden_cat) == len(predict_cat)
		
		for i in range(len(golden_cat)):
			if golden_cat[i] == predict_cat[i]: 
				correct += 1
				if golden_cat[i] == 'N':
					TN += 1
				else: TCE += 1
			else:
				if golden_cat[i] == 'N': FCE+=1
				else: FN += 1

		tot += len(golden_cat)

	acc = float(correct) / tot
	precision = float(TCE) / (TCE+FCE)
	recall = float(TCE) / (TCE+FN)

	print "TCE: ",TCE," TCE+FCE: ",TCE+FCE,"CE: ",TCE+FN
	
	return (acc,precision,recall)


def main():
	parser = OptionParser()

	parser.add_option("-p","--predictfile",type="string",
		help="")
	parser.add_option("-s","--goldenfile",type="string",
		help="")

	(options, args) = parser.parse_args()
	
	if options.predictfile and options.goldenfile :
		predict_file = open(options.predictfile)
		golden_file = open(options.goldenfile)
			
		global acc,precision, recall

		acc,precision,recall = evaluate1(predict_file, golden_file)
	else:
		print >> stderr, 'not given predict filename or golden filename'
	
	print "Accuracy: ",acc
	print "Precision: ",precision
	print "Recall: ",recall
	print "F1: ", 2*precision*recall/(precision + recall)

if __name__=="__main__":
	main()
