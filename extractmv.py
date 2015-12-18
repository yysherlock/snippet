import os
import shutil

datadir = "data/"
targetdir = "data1/"

if not os.path.exists(targetdir): os.mkdir(targetdir)

data_files = os.listdir(datadir)

def mv(suffix_parsed_files):# parsed_aa_fb / aa_fb
	for data_fn in data_files:
		if data_fn not in suffix_parsed_files:
			shutil.move(datadir+data_fn,targetdir+data_fn)

def generate_parsed_files(folder_list):
	result=[]
	for folder in folder_list:
		for fn in os.listdir(folder):
			result.append(fn[7:])
	return result

if __name__ == "__main__":
	suffix_parsed_files = generate_parsed_files(["parsed1"])
	mv(suffix_parsed_files)

