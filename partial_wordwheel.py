#!/usr/bin/env python

import sqlite3
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
st = form.getvalue("search_term")
d = int(form.getvalue("difference"))

db = sqlite3.connect("dvlg-wheel.sqlite")
curs = db.cursor()

st2 = (st.decode("utf-8"),)

try:
    st.decode('ascii')
except UnicodeDecodeError:
    dict = 'GreekHeadwords'
else:
    dict = 'LatinHeadwords'

curs.execute("select rowid from %s where head=?" % dict, st2)

#rownum = curs.fetchone()[0] - 21;

print "Content-Type: text/html; charset=utf-8"
print

if d < 0:
    rownum = curs.fetchone()[0] - 31;
    rownum2 = (rownum, -d)
    curs.execute("select * from %s where rowid > ? limit ?" % dict, rownum2);
    
else:
    rownum = curs.fetchone()[0] + 30 - d;
    rownum2 = (rownum, d)
    curs.execute("select * from %s where rowid > ? limit ?" % dict, rownum2);

hws = []

for row in curs:
    hws.append(row[0].encode("utf-8"))

if d < 0:
    i = 0
    while rownum < 1:
        print '<li id="w' + str(i) + '" class="other_hws" style="top: -315px; "></li>\n'
        rownum += 1
        i += 1
        if i == -d:
            break
    for hw in hws:
        if i == -d:
            break
        print '<li id="w' + str(i) + '" class="other_hws" style="top: -315px; ">' + hw + '</li>\n'
        i += 1
else:
    i = 61 - d
    for hw in hws:
        print '<li id="w' + str(i) + '" class="other_hws" style="top: -315px; ">' + hw + '</li>\n'
        i += 1
    while i < 61:
        print '<li id="w' + str(i) + '" class="other_hws" style="top: -315px; "></li>\n'
        i += 1
    
    #hw = row[0].encode("utf-8")
    #if hw == st and i < 20:
    #    hws = [''] * (20 - i) + hws
    #    i = 20 - i 
    #hws.append(hw)
    #if i == 10:
    #    break
    #i += 1

#if rownum < 0:
    #hws = ([''] * -rownum + hws)[:-d]
    
#if i < 41:
#    hws += [''] * (41 - i) 
    
#print (JSONEncoder().encode(hws))#.replace(" ", "").replace("\n", "")
