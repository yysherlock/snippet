import os,sys
import subprocess
p = subprocess.Popen(["svn","list","svn://202.120.38.146/papers/"],stdout=subprocess.PIPE)
dirs = p.communicate('xx')[0].split('\n')

svn_path = "svn://202.120.38.146/papers/"
for directory in dirs:
    if directory:
        cur_path = svn_path + directory.strip()
        subprocess.call(["echo",cur_path])
        subprocess.call(["svn","log",cur_path])
        
