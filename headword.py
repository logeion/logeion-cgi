#!/usr/bin/env python
# coding=utf-8

import re
import sqlite3
import cgi
import cgitb
import sys
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, Tag

# enable cgi and get headword to search for
cgitb.enable()

form = cgi.FieldStorage()
st = form.getvalue("search_term")

# connect to the database
#try:
db = sqlite3.connect("dvlg-wheel.sqlite")
#except(Exception):
#	print "Couldn't connect to db."
#	sys.exit(0)
db.row_factory = sqlite3.Row
curs = db.cursor()

# initialize counting variables
numDicts = 0
numEntries = 0

# initialize dictionaries and their entry lists
#dictsLatin = {"LatinShortDefs":[], "BWL":[], "LewisShort":[], "Lewis":[], "DuCange":[], "Antiquities":[], "Geography":[], "Harpers":[], "PerseusEncyclopedia":[], "PrincetonEncyclopedia":[]}
dictsLatin = {"LatinShortDefs":[], "BWL":[], "LewisShort":[], "Lewis":[], "ExamplesFromTheCorpus":[], "LaNe":[], "DuCange":[], "Antiquities":[], "Geography":[], "Harpers":[], "PerseusEncyclopedia":[], "PrincetonEncyclopedia":[]}
#dictsGreek = {"GreekShortDefs":[], "LSJ":[], "Autenrieth":[], "Slater":[], "MiddleLiddell":[]}
dictsGreek = {"GreekShortDefs":[], "LSJ":[], "Autenrieth":[], "Slater":[], "MiddleLiddell":[], "ExamplesFromTheCorpus":[]}

dFound = []
lang = ""
lemmas = []

# figure out whether we're searching for Latin or Greek
try:
    st.decode("ascii")
except UnicodeDecodeError:
    lang = "greek"
    dicts = dictsGreek
    #dOrder = ["GreekShortDefs", "LSJ", "Autenrieth", "Slater", "MiddleLiddell"]
    dOrder = ["GreekShortDefs", "LSJ", "Autenrieth", "Slater", "MiddleLiddell", "ExamplesFromTheCorpus"]
    samplesDB = "greekInfo.db"
else:
    lang = "latin"
    dicts = dictsLatin
    #dOrder = ["LatinShortDefs", "BWL", "LewisShort", "Lewis", "DuCange", "Antiquities", "Geography", "Harpers", "PerseusEncyclopedia", "PrincetonEncyclopedia"]
    dOrder = ["LatinShortDefs", "BWL", "LewisShort", "Lewis", "LaNe", "DuCange", "ExamplesFromTheCorpus", "Antiquities", "Geography", "Harpers", "PerseusEncyclopedia", "PrincetonEncyclopedia"]
    samplesDB = "latinInfo.db"

# perform the search and get all the results
st2 = (st.decode("utf-8"),)
curs.execute("SELECT * FROM Entries WHERE lookupform=?", st2)

rows = curs.fetchall()

#if rows == []:
#    numEntries += 1
#    if lang == "greek":
#        lex = sqlite3.connect("GreekLexicon.db")
#        curs2 = lex.cursor()
#    else:
#        lex = sqlite3.connect("LatinLexicon.db")
#        curs2 = lex.cursor()
    
#    while rows == []:
#        st2 = (st.decode("utf-8"),)
#        curs2.execute("SELECT lemma FROM Lexicon WHERE token=?", st2)
    
#        lrows = curs2.fetchall()
    
#        for lrow in lrows:
#            lemma = (lrow[0].encode("utf-8"),)
            
#            if lemma[0] not in lemmas:
#                lemmas += lemma
            
#            if rows != []:
#                continue
            
#            curs.execute("SELECT * FROM Entries WHERE lookupform=?", lemma)
        
#            rows = curs.fetchall()
        
#        if rows == []:
#            st = st[0:len(st)-1]

#    lex.close()    
    
db.close()

headword = ""

# for each row
for row in rows:
    # find the actual headword, the entry, and the dictionary it's in
    #hw = row[0].encode("utf-8")
    #orth_orig = row[1].encodeI("utf-8")
    #entry = row[2].encode("utf-8")
    #dict = row[3].encode("utf-8")
    hw = row['head'].encode("utf-8")
    orth_orig = row['orth_orig'].encode("utf-8")
    entry = row['content'].encode("utf-8")
    dict = row['dico'].encode("utf-8")

    # Where the orth_orig replacement is handled; it's separate for now to facilitate debugging
    if dict == 'Antiquities':
        orth_patt = re.compile("(<label[^>]*>)[^<]*(</label>)")
    
    if orth_orig: entry = re.sub("(<head[^>]*>)[^<]*(</head>)", "\1"+orth_orig+"\2", entry)
    
    if headword == "":
        headword = hw

    # add the to dictionary count if we haven't already for this dictionary
    if not dict in dFound:
        numDicts += 1
        
    dFound.append(dict)
    
    # get rid of the title tags in all of the dictionaries
    entry = re.sub('<title>', '<text>', entry)
    entry = re.sub('</title>', '</text>', entry)
    
    # whatever the dictionary we convert from the entry to BeautifulStoneSoup and back again
    # to make it a little nicer to read (and sometimes perform some changes to the hierarchy)
    
    # if the dictionary is either of the ShortDefs
    if dict == "LatinShortDefs" or dict == "GreekShortDefs":
        soup = BeautifulStoneSoup(entry)
        entry = soup.prettify()
        
        #add headword (which are numbered in ShortDefs) to the beginning of the entry
        entry = hw + ", " + entry

        dicts[dict].append(entry)
        numEntries += 1
    
    # if the dictionary is Lewis & Short, LSJ, Slater, or MiddleLiddell
    elif dict == "LewisShort" or dict == "LSJ" or dict == "Slater" or dict == "MiddleLiddell":
        soup = BeautifulSoup(entry)
        
        # get the first sense tag
        s = soup.sense
        orig_level = -1
        
        # one-by-one, convert all of the sense tags to li tags with various levels of indentation
        # based on its attributes
        while s != None:
            if s.has_key('level'):
                level = int(s.get('level'))
            
            li = Tag(soup, 'li', [('style', 'margin-left: ' + str((level - 1) * 20) + 'px;')])
            
            if (orig_level == -1):
                orig_level = level
            
            if ((level - orig_level) % 3) == 0:
                li['class'] = 'l1'
            elif ((level - orig_level) % 3) == 1:
                li['class'] = 'l2'
            elif ((level - orig_level) % 3) == 2:
                li['class'] = 'l3'
            
            cs = s.contents
            i = 0
            for c in cs:
                li.insert(i, unicode(c))
                i += 1
            
            s.replaceWith(li)
            s = soup.sense
            
        entry = soup.prettify()
        
        # bookend the li tags with an ordered list
        entry = re.sub('<li', '<ol><li', entry, 1)
        entry = re.sub('</div1>', '</ol></div1>', entry)
        
        entry = re.sub('\s+,', ',', entry)
        entry = re.sub('\s+:', ':', entry)
        entry = re.sub('\s+;', ';', entry)        
        
        dicts[dict].append(entry)
        numEntries += 1

    # if the dictionary is Lewis
    elif dict == "Lewis":
        soup = BeautifulStoneSoup(entry)
        
        u = soup.findAll('usg')
        c = len(u) - 2
        
        #entry = soup.prettify()
        
        entry = re.sub('</etym>, ', '</etym>,<ol><li class="l1" style="margin-left: 10px; margin-top: 5px; list-style-type: none;">\xe2\x80\x94', entry)
        entry = re.sub('\xe2\x80\x94', '</li><li class="l1" style="margin-left: 10px; margin-top: 5px; list-style-type: none;">\xe2\x80\x94', entry)
        #entry = re.sub('<usg opt="n">', '</li>\n<li style="margin-left: 15px; margin-bottom: 3px; list-style-type: none;">', entry)
        #entry = re.sub('<usg opt="n">', '</li></ol>', entry)
        entry = re.sub('</sense>', '</li></ol></sense>', entry)
        
        # bookend the li tags with an ordered list
        #entry = re.sub('<li', '<ol><li', entry, 1)
        #entry = re.sub('</div1>', '</ol></div1>', entry)
        
        #
        #entry = re.sub('\.\n', '.', entry)
        #entry = re.sub('\n', '', entry)
        
        dicts[dict].append(entry)
        numEntries += 1
    
    # if the dictionary is BWL
    elif dict == "BWL":
        soup = BeautifulStoneSoup(entry)

        # find the number of sense tags    and subtract one
        s = soup.findAll('sense')
        c = len(s) - 1
        
        entry = soup.prettify()
        
        # add to all but the last sense tag two line breaks to space out the examples
        entry = re.sub('</sense>', '</sense><br><br>', entry, c)
    
        dicts[dict].append(entry)
        numEntries += 1

    # if the dictionary is LaNe
    elif dict == "LaNe":
        soup = BeautifulStoneSoup(entry)

        tag = soup.metalex
        tag.clear()

        entry = soup.prettify()

        entry = re.sub('1\.', '<ol><li class="l1" style="margin-left: 10px; margin-top: 5px; list-style-type: none;">1.\t', entry, 1)
        entry = re.sub(r'(\d+\.(?!\t))', r'</li><li class="l1" style="margin-left: 10px; margin-top: 5px; list-style-type: none;">\1\t', entry)
        
        entry = re.sub('<METALEX>.*</METALEX>', '', entry)
        
        entry = re.sub('&wit;', ' ', entry)
        entry = re.sub('&hk;', u'\u2014'.encode('utf-8'), entry)
        entry = re.sub('&pijl;', u'\u27A4'.encode('utf-8'), entry)
        entry = re.sub('&tilde;', u'\u007E'.encode('utf-8'), entry)
        entry = re.sub('&lquote;', u'\u2018'.encode('utf-8'), entry)
        entry = re.sub('&rquote;', u'\u2019'.encode('utf-8'), entry)
        entry = re.sub('&super1;', u'\u00B9'.encode('utf-8'), entry)
        entry = re.sub('&super2;', u'\u00B2'.encode('utf-8'), entry)
        entry = re.sub('&amacron;', u'\u0101'.encode('utf-8'), entry)
        entry = re.sub('&emacron;', u'\u0113'.encode('utf-8'), entry)
        entry = re.sub('&imacron;', u'\u012B'.encode('utf-8'), entry)
        entry = re.sub('&omacron;', u'\u014D'.encode('utf-8'), entry)
        entry = re.sub('&umacron;', u'\u016B'.encode('utf-8'), entry)
        
        #entry = re.sub(r'<sem>', r'<ol><li class="l1" style="margin-left: 10px; margin-top: 5px; list-style-type: none;">', entry, 1)
        #entry = re.sub(r'<sem>', r'<li class="l1" style="margin-left: 10px; margin-top: 5px; list-style-type: none;">', entry)
        #entry = re.sub(r'</sem>', r'</li>', entry)
        #entry = re.sub(r'</lentry>', r'</ol></lentry>', entry)
        
        dicts[dict].append(entry)
        numEntries += 1

    # if the dictionary is DuCange
    elif dict == "DuCange":
        entry = re.sub('<dictScrap', '&nbsp;&nbsp;&nbsp;&nbsp;<dictScrap', entry)
        entry = re.sub('dictScrap>', 'dictScrap><br><br>', entry)
    
        entry = re.sub(r'<form rend="b">(.*?)</form>', r'<b>\1</b>', entry)
        entry = re.sub(r'<form rend="sc">(.*?)</form>', r'<i>\1</i>', entry)
        entry = re.sub(r'<hi rend="i">(.*?)</hi>', r'<i>\1</i>', entry)

        dicts[dict].append(entry)
        numEntries += 1
        
    # if the dictionary is any other dictionary
    else:
        soup = BeautifulStoneSoup(entry)
        entry = soup.prettify()
        
        entry = re.sub('<sem>', '<ol><sem><li class="l1" style="margin-left: 10px; margin-top: 5px; list-style-type: none;">', entry, 1)
        entry = re.sub('<sem>', '<sem><li class="l1" style="margin-left: 10px; margin-top: 5px; list-style-type: none;">', entry)
        entry = re.sub('</sem>', '</li></sem>', entry)
        entry = re.sub('</lentry>', '</ol></lentry>', entry)
        dicts[dict].append(entry)
        numEntries += 1

db = sqlite3.connect(samplesDB)
curs = db.cursor()

# perform the search and get all the results
st2 = (st.decode("utf-8"),)
curs.execute("select * from samples where lemma=?", st2)

rows = curs.fetchall()

db.close()

all = []

first = []
second = []
third = []
fourth = []

# if we found any sample data
if rows != None:
    for row in rows:
        lemma = row[0].encode("utf-8")
        rank = int(row[1])
        line = row[2].encode("utf-8")
        author = row[3].encode("utf-8")
        work = row[4].encode("utf-8")

        if lang == "latin":
            authorSearch = "http://perseus.uchicago.edu/cgi-bin/search3t?dbname=LatinAugust2011&word=lemma%3A" + lemma + "&OUTPUT=conc&CONJUNCT=PHRASE&DISTANCE=3&author=" + re.sub(" ", "+", author) + "&title=&POLESPAN=5&THMPRTLIMIT=1&KWSS=1&KWSSPRLIM=500&trsortorder=author%2C+title&editor=&pubdate=&language=&shrtcite=&filename=&genre=&sortorder=author%2C+title&dgdivhead=&dgdivtype=&dgsubdivwho=&dgsubdivn=&dgsubdivtag=&dgsubdivtype="
            workSearch = "http://perseus.uchicago.edu/cgi-bin/search3t?dbname=LatinAugust2011&word=lemma%3A" + lemma + "&OUTPUT=conc&&CONJUNCT=PHRASE&DISTANCE=3&author=" + re.sub(" ", "+", author) + "&title=" + re.sub(" ", "+", work) + "&POLESPAN=5&THMPRTLIMIT=1&KWSS=1&KWSSPRLIM=500&trsortorder=author%2C+title&editor=&pubdate=&language=&shrtcite=&filename=&genre=&sortorder=author%2C+title&dgdivhead=&dgdivtype=&dgsubdivwho=&dgsubdivn=&dgsubdivtag=&dgsubdivtype="
            sample = "<li lang=\"latin\">..." + line + "...  <as href=\"" + authorSearch + "\">" + author + "</as>, <ws href=\"" + workSearch + "\">" + work + "</ws></li><br>"
        else:
            authorSearch = "http://perseus.uchicago.edu/cgi-bin/search3torth?dbname=GreekFeb2011&word=lemma%3A" + lemma + "&OUTPUT=conc&ORTHMODE=ORG&CONJUNCT=PHRASE&DISTANCE=3&author=" + re.sub(" ", "+", author) + "&title=&POLESPAN=5&THMPRTLIMIT=1&KWSS=1&KWSSPRLIM=500&trsortorder=author%2C+title&editor=&pubdate=&language=&shrtcite=&filename=&genre=&sortorder=author%2C+title&dgdivhead=&dgdivtype=&dgsubdivwho=&dgsubdivn=&dgsubdivtag=&dgsubdivtype="
            workSearch = "http://perseus.uchicago.edu/cgi-bin/search3torth?dbname=GreekFeb2011&word=lemma%3A" + lemma + "&OUTPUT=conc&ORTHMODE=ORG&CONJUNCT=PHRASE&DISTANCE=3&author=" + re.sub(" ", "+", author) + "&title=" + re.sub(" ", "+", work) + "&POLESPAN=5&THMPRTLIMIT=1&KWSS=1&KWSSPRLIM=500&trsortorder=author%2C+title&editor=&pubdate=&language=&shrtcite=&filename=&genre=&sortorder=author%2C+title&dgdivhead=&dgdivtype=&dgsubdivwho=&dgsubdivn=&dgsubdivtag=&dgsubdivtype="
            sample = "<li lang=\"greek\">..." + line + "...  <as href=\"" + authorSearch + "\">" + author + "</as>, <ws href=\"" + workSearch + "\">" + work + "</ws></li><br>"
    
        if rank == 1:
            first += [sample]
        elif rank == 2:
            second += [sample]
        elif rank == 3:
            third += [sample]
        else:
            fourth += [sample]

all = first + second + third + fourth

i = 0

samples = ""

for sample in all:
    if i == 10:
        break

    samples += sample
    
    i += 1

#samples.encode("utf-8")

dicts["ExamplesFromTheCorpus"] = [samples]

# required to print out the html
print "Content-Type: text/html; charset=utf-8"
print

if lemmas != []:
    print 'Could not find ' + st + '. Showing first parse.'
    if len(lemmas) > 1:
        print '<p>Other possible parses include: '
        for lemma in lemmas[1:]:
            print '<lemma>' + lemma + '</lemma>'
        

# intro line and instructions for usage
print '<p>' + str(numEntries) + ' definition(s) found in ' + str(numDicts) + ' dictionary(ies). Click on dictionary name to show/hide that dictionary. Click on entry number to focus/unfocus on that entry.</p><p>Double-click on any word in an entry to look it up.</p>' 

# for every dictionary (in a specific order) where the headword could have been found
for d in dOrder:
    # get the entries found in that dictionary
    es = dicts[d]
    if es == [] or es == [""]:
        continue
    
    dname = d if d != "ExamplesFromTheCorpus" else "Examples from the corpus"
    
    # print out the tab and controls of the box this specific dictionary's entries goes into
    print '<div id="' + d + '" class="dict_tab">'
    print '<div id="' + d + '_dn" class="dict_name">' + dname + '</div>'#<div class="entry_count">' + str(len(es)) + '</div>'
    if len(es) > 1:
        for i in range(len(es)):
            print '<div id="' + d + '_et' + str(i + 1) + '" class="entry_tab">' + str(i + 1) + '</div>'    
    print '</div>'
    
    # print out the entries or samples themselves
    print '<div id="' + d + '_eb" class="entry_box">'
    i = 1
    for e in es:
        print '<div id="' + d + str(i) + '" class="entry">' + e + '</div>'
        i+=1
    print '</div>'
