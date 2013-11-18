#!/usr/bin/env python

import re
import sqlite3
import cgi
import cgitb

# enable cgi and get headword to search for
cgitb.enable()

form = cgi.FieldStorage()
st = form.getvalue("search_term")
    
# figure out whether we're searching for Latin or Greek
try:
    st.decode("ascii")
except UnicodeDecodeError:
    db = sqlite3.connect("greekInfo.db")
else:
    db = sqlite3.connect("latinInfo.db")

curs = db.cursor()

# perform the search and get all the results
st2 = (st.decode("utf-8"),)
curs.execute("select * from collocations where lemma=?", st2)

rows = curs.fetchall()

# required to print out the html
print "Content-Type: text/html; charset=utf-8"
print

# if we found any collocation data
if rows != None:
    # print it out in list form
    i = 0
    for row in rows:
        sw = re.sub(r"\d","",row[1]).encode("utf-8")

        print "<li id=\"c" + str(i) + "\" class=\"collocation_hws\"><span class=\"searchable\" sw=\"" + sw + "\">" + row[1].encode("utf-8") + "</span> - " + str(row[2]) + "</li>"

        i += 1
