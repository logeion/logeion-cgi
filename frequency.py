#!/usr/bin/env python

import re
import sqlite3
import cgi
import cgitb

# enable cgi and get headword to search for
cgitb.enable()

form = cgi.FieldStorage()
st = form.getvalue("search_term")

lang = ''
    
# figure out whether we're searching for Latin or Greek
try:
    st.decode("ascii")
except UnicodeDecodeError:
    dbname = "greekInfo.db"
    lang = 'greek'
else:
    dbname = "latinInfo.db"
    lang = 'latin'

db = sqlite3.connect(dbname)

curs = db.cursor()

# perform the search and get all the results
st2 = (re.sub('[\d\[\]]', '', st.decode("utf-8")),)
possible_lemmas = curs.execute('select lemma, rank from frequencies ' + \
                               'where lookupform=?', st2).fetchall()
st_mostfreq = st.decode('utf-8')
if possible_lemmas:
    st_mostfreq = sorted(possible_lemmas, key=lambda x: x[1])[0][0]

row = curs.execute("select * from frequencies where lemma=?", (st_mostfreq,)).fetchone()

# required to print out the html
print "Content-Type: text/html; charset=utf-8"
print

print '<span class="freq_spans">%s</span><br>' % st_mostfreq.encode('utf-8')

# if we found any frequency data
if row != None:
    rank = row[1]
    prefix = '<span class="freq_spans">(%s)'
    
    # print out its rank corectly
    if rank % 10 == 1:
        if rank == 1:
            print "<span class=\"freq_spans\">Most frequent word </span>"
        elif rank % 100 == 11:
            print "<span class=\"freq_spans\">" + str(rank) + "th most frequent word </span>"
        else:
            print "<span class=\"freq_spans\">" + str(rank) + "st most frequent word </span>"
    elif rank % 10 == 2:
        if rank % 100 == 12:
            print "<span class=\"freq_spans\">" + str(rank) + "th most frequent word </span>"
        else:
            print "<span class=\"freq_spans\">" + str(rank) + "nd most frequent word </span>"
    elif rank % 10 == 3:
        if rank % 100 == 13:
            print "<span class=\"freq_spans\">" + str(rank) + "th most frequent word </span>"
        else:
            print "<span class=\"freq_spans\">" + str(rank) + "rd most frequent word </span>"
    else:
        print "<span class=\"freq_spans\">" + str(rank) + "th most frequent word </span>"
# otherwise
else:
    print "<span class=\"freq_spans\">Unranked (appears less than 50 times)</span>"

print "<br><hr style=\"margin-left: -5px; width: 150px; border: 0; border-top: solid 1px #A39770;\">"

# perform the search and get all the results
#st2 = (st.decode("utf-8"),)
curs.execute("select * from authorFreqs where lemma=?", (st_mostfreq,))

rows = curs.fetchall()

# if we found any author frequency data
if rows != None:
    # print it out in table form
    #print "<table border=\"0\">"
    print "<span class=\"freq_spans\">Most frequently used by:</span>"
    i = 0
    print "<ol id=\"author_ranks\">"
    for row in rows:
        #print "<li class=\"author_rank\">" + row[2].encode("utf-8") + "</li>"
        author = row[2].encode("utf-8")
        if lang == "latin":
            authorSearch = "http://artflx.uchicago.edu/perseus-cgi/search3t?dbname=LatinAugust2011&word=lemma%3A" + st_mostfreq.encode('utf-8') + "&OUTPUT=conc&CONJUNCT=PHRASE&DISTANCE=3&author=" + re.sub(" ", "+", author) + "&title=&POLESPAN=5&THMPRTLIMIT=1&KWSS=1&KWSSPRLIM=500&trsortorder=author%2C+title&editor=&pubdate=&language=&shrtcite=&filename=&genre=&sortorder=author%2C+title&dgdivhead=&dgdivtype=&dgsubdivwho=&dgsubdivn=&dgsubdivtag=&dgsubdivtype="
        else:
            authorSearch = "http://artflx.uchicago.edu/perseus-cgi/search3torth?dbname=GreekFeb2011&word=lemma%3A" + st_mostfreq.encode('utf-8') + "&OUTPUT=conc&ORTHMODE=ORG&CONJUNCT=PHRASE&DISTANCE=3&author=" + re.sub(" ", "+", author) + "&title=&POLESPAN=5&THMPRTLIMIT=1&KWSS=1&KWSSPRLIM=500&trsortorder=author%2C+title&editor=&pubdate=&language=&shrtcite=&filename=&genre=&sortorder=author%2C+title&dgdivhead=&dgdivtype=&dgsubdivwho=&dgsubdivn=&dgsubdivtag=&dgsubdivtype="
        print "<li class=\"author_rank\"><as href=\"" + authorSearch + "\">" + author + "</as></li>"
        i += 1
    print "</ol>"
