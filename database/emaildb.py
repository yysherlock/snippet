
# install database browser
""" Relational databases apply cleverness
to how we would use random access data storage,
mostly disc drives.
The idea is that you model data at a connection point
rather than like here's data and we're starting here
and we're reading through it.
This notion of modeling stuff as a connection is the
underlying math that makes databases fast,
"""
import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = raw_input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: ') : continue
    pieces = line.strip().split()
    org = pieces[1].split('@')[1]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES ( ?, 1 )''', ( org, ) )
    else :
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?',
            (org, ))
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
#sqlstr = 'SELECT COUNT(*) FROM Counts'

#for row in cur.execute(sqlstr):
#    print str(row)
for row in cur.execute(sqlstr) :
    print str(row[0]), row[1]


cur.close()
