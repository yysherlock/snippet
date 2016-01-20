print '\xd6\xd0'
## print '\xe4\xb8\xad\xe6\x96\x87\xe6\xb5\x8b\xe8\xaf\x95' # ascii code for string `中文测试`, but this is illegal when you don't declare
#import sys
#print sys.getdefaultencoding()

#s1 = "python测试文件" # When you type `python unicodetest.py` in the command, 
	# python interpretor takes the .py file as ASCII encoding file, 
	# when it met the non-ascii character, it confused.
	# we should declare the coding way 
	# to help python interpretor recoganize those characters, `# coding=utf-8`
	# remove that line, you will get a Syntax error.
#print s1
#print type(s1)

#print s1 + u"Chinese Test"
#s2 = "python测试文件".decode('utf-8') + u"Chinese Test"
#s2 = "python测试文件" + u"Chinese Test".encode("utf-8")
#print s2

