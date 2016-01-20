#coding:utf8

import re
import os.path
import datetime,time
import json

"""
task format:
    task_content1[due_h:due_m];task_content2[due2]
"""
tasks = {}

def add_task(content):
    task = content.split('[')[0]
    dueh, duem = map(int, re.search('\[(.*)\]',content).group(1).split(':'))
    now = datetime.datetime.now()
    nowh, nowm = now.hour, now.minute
    if dueh < nowh or (dueh == nowh and duem < nowm):
        print 'invalid task'
        return
    tasks.setdefault(task,[0,0,'todo'])
    tasks[task] = [dueh, duem,'todo']

if not os.path.exists('task.json'):
    
    if os.path.exists('todo.list'):
        x=time.localtime(os.path.getmtime('todo.list'))
        last_modified_date = datetime.date(x.tm_year, x.tm_mon, x.tm_mday)
        if last_modified_date == datetime.datetime.today().date():

            with open('todo.list') as f:
                for line in f:
                    content = line.strip()
                    add_task(content)

    else:
        contents = raw_input('Please enter today\'s task:\n')
        content_list = contents.split(';')

        for content in content_list:
            add_task(content)

    with open('task.json','w') as outf:
        outf.write(json.dumps(tasks, ensure_ascii=False))

else:
    tasks = json.loads(open('task.json').read())

with open('state.list','w') as outf:
    for k,v in tasks.items():
        outf.write(k+' '+v[2]+'\n')


        

