#coding:utf-8

from datetime import date
from termcolor import colored

ijcai_due = date(2016, 2, 2)
ijcai = 'IJCAI, New York, USA'
acl_due = date(2016, 3, 18)
acl = 'ACL, Berlin, German'
cikm_due = date(2016, 5, 12)
cikm = 'CIKM, Singapore'
emnlp_due = date(2016, 6, 3)
emnlp = 'EMNLP, Austin, USA'
#aaai_due = date(2016, 0, 0)
#aaai = 'AAAI, Melbourne, Australian'

dic = {ijcai_due:ijcai, acl_due:acl, cikm_due:cikm, emnlp_due:emnlp}

today = date.today()

def duePrint(due):
    print '距 ', dic.get(due), ' 还有 ', colored((due-today).days,'yellow'), ' 天\n'

print ''
duePrint(ijcai_due)
duePrint(acl_due)
duePrint(cikm_due)
duePrint(emnlp_due)


