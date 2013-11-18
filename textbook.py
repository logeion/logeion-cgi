#!/usr/bin/env python

import re
import sqlite3
import cgi
import cgitb
from BeautifulSoup import BeautifulStoneSoup, Tag

# enable cgi and get headword to search for
cgitb.enable()

form = cgi.FieldStorage()
st = form.getvalue("search_term")

# connect to the database
db = sqlite3.connect("dvlg-wheel.sqlite")
db.row_factory = sqlite3.Row
curs = db.cursor()

# perform the search and get all the results
st2 = (st.decode("utf-8"),)
curs.execute("select * from Sidebar where lookupform=?", st2)

rows = curs.fetchall()

alreadyDone = []
i = 0

# required to print out the html
print "Content-Type: text/html; charset=utf-8"
print

# for each row
for row in rows:
    #find the actual headword, the ???, the chapter, and the dictionary it's in
    hw = row['head'].encode("utf-8")
    #cont = row[1].encode('utf-8')
    cont = row['content']
    if cont: cont = cont.encode('utf-8')
    ch = row['chapter'].encode("utf-8")
    dict = row['dico'].encode("utf-8")
    
    if dict in alreadyDone:
        continue
    else:
        alreadyDone.append(dict)

    # print it out in list form
    print "<li id=\"t" + str(i) + "\" class=\"textbook_locs\">"
    
    if ch == "" and dict != "Wheelock":
        print "BWL"
    elif dict == "HansenQuinn":
        print "Hansen & Quinn " + ch
    else:
        print dict + " " + ch    
    
    i += 1
    
