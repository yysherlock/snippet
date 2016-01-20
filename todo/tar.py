#coding:utf8
import codecs
import json

tasks = json.loads(codecs.open('task.json','r','utf-8').read())
with codecs.open('done.list','a','utf-8') as outf, codecs.open('backup.list','a','utf-8') as notf:
    for k,v in tasks.items():
        print k,v
        if v=="done":
            outf.write( k+' '+v+'\n')
        else:
            notf.write( k+' '+v+'\n')



