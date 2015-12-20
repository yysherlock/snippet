print '\xd6\xd0'.decode('gbk')
print '\xd6\xd0'.decode('gbk').encode('utf-8')

# '\xd6\xd0' is the `ascii code`(which is the default coding of python interpretor, all kinds of characters in source file are transfered into such ascii codes in the interpretor ) represents `Chinese charater "zhong"` character if we decode '\xd6\xd0' in gbk.
#print '\xd6\xd0'.decode('ascii') # erros, `print` will decode \xd6\xd0 using 'ascii' (the system default encodes), but \xd6 is 214, can not decode into valid ascii characters
print '\xd6\xd0' # incorrect displaying characters, why?

#print '\xd6\xd0'.decode('utf-8') # error, since \xd6\xd0i(ascii codes) is valid chinese character decoded in gbk, but not valid decoded in utf-8

print '\xe4\xb8\xad'
print '\xe4\xb8\xad'.decode('utf-8')
print '\xe4\xb8\xad'.decode('utf-8').encode('utf-8')
#print '\xe4\xb8\xad'.decode('')
