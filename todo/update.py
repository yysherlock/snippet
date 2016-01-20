#coding:utf-8
import codecs
import json
import os.path

tasks = json.loads(codecs.open('task.json','r','utf-8').read())

with open('state.list') as f1:
    for line in f1:
        key = ' '.join(line.strip().split()[:-1])
        state = line.strip().split()[-1]
        tasks[key] = state

with codecs.open('task.json','w','utf-8') as outf:
    outf.write(json.dumps(tasks)) 
