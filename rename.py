__author__ = 'Zanacross'

import os,random, sqlite3
from time import time

def gen_ran():
    global used
    s = ''
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for b in xrange(8):
        if random.randint(0,1) == 1:
            s += str(random.randint(0,9))
        else:
            s+= random.choice(letters)
    if s not in used:
        used.append(s)
        return s
    else:
        gen_ran()


rootdir = os.path.dirname(os.path.realpath(__file__))

used = []
sql = sqlite3.connect('test.db')
with sql:
    cur = sql.cursor()
    cur.execute("CREATE TABLE PornLinks(Id INTEGER PRIMARY KEY, Name TEXT, Type TEXT, Date INTEGER);")

    x = 2
    for subdir, dirs, files in os.walk(rootdir):
        for i in files:
            if not i == 'test.db':
                sa = gen_ran()
                l = i.split('.')
                name = sa
                type1 = l[len(l)-1]
                used.append(name)
                cur.execute("INSERT INTO PornLinks(Name, Type, Date) VALUES(?, ?, ?)", (name+'.'+type1, type1, time()))
                os.renames(rootdir+'/'+i, rootdir+'/'+name+'.'+type1)
                x+=1
print used

