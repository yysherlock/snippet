#coding:utf-8

from datetime import date
from termcolor import colored

ijcai_due = date(2016, 2, 2)
ijcai = 'IJCAI, New York, American'
acl_due = date(2016, 3, 18)
acl = 'ACL, Berlin, German'
cikm_due = date(2016, 5, 12)
cikm = 'CIKM, Singapore'

dic = {ijcai_due:ijcai, acl_due:acl, cikm_due:cikm}

today = date.today()

def duePrint(due):
    print '距 ', dic.get(due), ' 还有 ', colored((due-today).days,'red'), ' 天\n'

print ''
duePrint(ijcai_due)
duePrint(acl_due)
duePrint(cikm_due)

