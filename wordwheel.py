#!/usr/bin/env python
# coding=utf-8

import sqlite3
import cgi
import cgitb
import re
import unicodedata

# strip the accents off of greek
def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

# handle the code column of lexicon rows
def decode(code):
    result = ""
    
    if code[0] == 'v':
        result += 'Verb'
        
        if code[2] == '1':
            result += ' - 1st person'
        elif code[2] == '2':
            result += ' - 2nd person'
        elif code[2] == '3':
            result += ' - 3rd person'
        
        if code[3] == 's':
            result += ' singular'
        elif code[3] == 'p':
            result += ' plural'
        elif code[3] == 'd':
            result += ' dual'
        
        if code[4] == 'p':
            result += ' - present'
        elif code[4] == 'i':
            result += ' - imperfect'
        elif code[4] == 'a':
            result += ' - aorist'
        elif code[4] == 'r':
            result += ' - perfect'
        elif code[4] == 'f':
            result += ' - future'
        elif code[4] == 'l':
            result += ' - pluperfect'
        elif code[4] == 't':
            result += ' - future perfect'
        
        if code[6] == 'a':
            result += ' active'
        elif code[6] == 'm':
            result += ' middle'
        elif code[6] == 'p':
            result += ' passive'
        elif code[6] == 'e':
            result += ' middle-passive'
        
        if code[5] == 'i':
            result += ' indicative'
        elif code[5] == 's':
            result += ' subjunctive'
        elif code[5] == 'o':
            result += ' optative'
        elif code[5] == 'm':
            result += ' imperative'
        elif code[5] == 'p':
            result += ' participle'
            if code[7] == 'm':
                result += ' - masculine'
            elif code[7] == 'f':
                result += ' - feminine'
            elif code[7] == 'n':
                result += ' - neuter'
            elif code[7] == 'c':
                result += ' - common'
                
            if code[8] == 'n':
                result += ' nominative'
            elif code[8] == 'g':
                result += ' genitive'
            elif code[8] == 'd':
                result += ' dative'
            elif code[8] == 'a':
                result += ' accusative'
            elif code[8] == 'b':
                result += ' ablative'
            elif code[8] == 'v':
                result += ' vocative'
        elif code[5] == 'n':
            result += ' infinitive'
        elif code[5] == 'g':
            result += ' gerundive'
        elif code[5] == 'd':
            result += ' gerund'
        elif code[5] == 'u':
            result += ' supine'

    elif code[0] == 'n':
        if code[1] == 'e':
            result += 'Proper-name noun'
        else:
            result += 'Noun'

        if code[7] == 'm':
            result += ' - masculine'
        elif code[7] == 'f':
            result += ' - feminine'
        elif code[7] == 'n':
            result += ' - neuter'
        elif code[7] == 'c':
            result += ' - common'
            
        if code[8] == 'n':
            result += ' - nominative'
        elif code[8] == 'g':
            result += ' - genitive'
        elif code[8] == 'd':
            result += ' - dative'
        elif code[8] == 'a':
            result += ' - accusative'
        elif code[8] == 'b':
            result += ' - ablative'
        elif code[8] == 'v':
            result += ' - vocative'

        if code[3] == 's':
            result += ' singular'
        elif code[3] == 'p':
            result += ' plural'
        elif code[3] == 'd':
            result += ' dual'
            
    elif code[0] == 'a':
        if code[1] == 'e':
            result += 'Proper-name adjective'
        else:
            result += 'Adjective'

        if code[9] == 'c':
            result += ' - comparative'
        elif code[9] == 's':
            result += ' - superlative'
            
        if code[7] == 'm':
            result += ' - masculine'
        elif code[7] == 'f':
            result += ' - feminine'
        elif code[7] == 'n':
            result += ' - neuter'
        elif code[7] == 'c':
            result += ' - common'
            
        if code[8] == 'n':
            result += ' - nominative'
        elif code[8] == 'g':
            result += ' - genitive'
        elif code[8] == 'd':
            result += ' - dative'
        elif code[8] == 'a':
            result += ' - accusative'
        elif code[8] == 'b':
            result += ' - ablative'
        elif code[8] == 'v':
            result += ' - vocative'

        if code[3] == 's':
            result += ' singular'
        elif code[3] == 'p':
            result += ' plural'
        elif code[3] == 'd':
            result += ' dual'
            
    elif code[0] == 'p':
        if code[1] == 'e':
            result += 'Proper-name pronoun'
        elif code[1] == 's':
            result += 'Possessive pronoun'
        elif code[1] == 'a':
            result += 'Determinative pronoun'
        elif code[1] == 'd':
            result += 'Demonstrative pronoun'
        elif code[1] == 'i':
            result += 'Interrogative pronoun'
        elif code[1] == 'r':
            result += 'Relative pronoun'
        elif code[1] == 'x':
            result += 'Indefinite pronoun'
        else:
            result += 'Pronoun'
            
        if code[7] == 'm':
            result += ' - masculine'
        elif code[7] == 'f':
            result += ' - feminine'
        elif code[7] == 'n':
            result += ' - neuter'
        elif code[7] == 'c':
            result += ' - common'
            
        if code[8] == 'n':
            result += ' - nominative'
        elif code[8] == 'g':
            result += ' - genitive'
        elif code[8] == 'd':
            result += ' - dative'
        elif code[8] == 'a':
            result += ' - accusative'
        elif code[8] == 'b':
            result += ' - ablative'
        elif code[8] == 'v':
            result += ' - vocative'

        if code[3] == 's':
            result += ' singular'
        elif code[3] == 'p':
            result += ' plural'
        elif code[3] == 'd':
            result += ' dual'
            
    elif code[0] == 'd':
        if code[1] == 'e':
            result += 'Proper-name adverb'
        else:
            result += 'Adverb'
            
        if code[9] == 'c':
            result += ' - comparative'
        elif code[9] == 's':
            result += ' - superlative'
            
    elif code[0] == 'c':
        result += 'Conjunction'
        
    elif code[0] == 'r':
        result += 'Preposition'
        
    elif code[0] == 'g':
        if code[1] == 'm':
            result += 'Modal particle'
        else:
            result += 'Particle'
    
    return result

# create a notice to be posted at the top of the result page    
def create_notice():
    l = len(lemmas)
    orig_st = form.getvalue("search_term")
    
    notice = '<img src=\'css/images/warning.png\'/ style=\'float: left; margin-right: 5px; margin-top: 5px;\'/>'
    
    if capFound:
        notice += '<p style=\'padding-top: 7px;\'>Found ' + orig_st + ' in the dictionaries with different capitalization.</p>'
        return notice
    elif accFound:
        notice += '<p style=\'padding-top: 7px;\'>Found ' + orig_st + ' in the dictionaries with different accentuation.</p>'
        return notice
    
    # if the orignal search term was not found
    if not found:
        # and if no potential parses were found
        if not lemmas:
            notice += '<p style=\'padding-top: 7px;\'>Could not find ' + st + ' in the dictionaries. Showing closest alphabetical location.</p>'
        
        # otherwise
        else:
            i = 1

            tooltip = '<br/>'.join(lemmas[mainLemma])
            notice += 'Could not find ' + st + ' in the dictionaries. Parsed ' + st + ' as a form of <parse title=\'' + tooltip + '\' class=\'searchable\'>' + mainLemma + '</parse>'
            
            if l > 1:
                notice += '. Other potential parsed forms include: '
                
                for lemma, parses in lemmas.iteritems():
                    if lemma == mainLemma:
                        continue
                
                    tooltip = '<br/>'.join(parses)        
                    notice += '<parse title=\'' + tooltip + '\' class=\'searchable\'>' + lemma + '</parse>'
                    
                    if i != l - 1:
                        notice += ', '
            
                    i += 1
    
    # if the orignal search term was found
    else:
        i = 0

        if l < 2:
            return ""
        
        notice += 'Found ' + st + ' in the dictionaries, but potential parsed forms include: '
    
        for lemma, parses in lemmas.iteritems():
            if lemma == st:
                continue
                
            tooltip = '<br/>'.join(parses)        
            if i == 0:
                notice += '<parse title=\'' + tooltip + '\' class=\'searchable\'>' + lemma + '</parse>'
            else:
                notice += ', <parse title=\'' + tooltip + '\' class=\'searchable\'>' + lemma + '</parse>'
            
            i += 1
    
    # if any potential parses were found, give instructions on what to do with them
    if lemmas:
        notice += '.<br/>Hover over lemma to see detail parses; click on lemma to see dictionary entry.'
    
    return notice
    
# enable cgi and get headword to search for
cgitb.enable()

form = cgi.FieldStorage()
st = form.getvalue("search_term")

# connect to the database
db = sqlite3.connect("dvlg-wheel.sqlite")
curs = db.cursor()

mainLemma = ''
lemmas = {}
found = 0
capFound = 0
accFound = 0

# figure out whether we're searching for Latin or Greek
try:
    st.decode('ascii')
except UnicodeDecodeError:
    dict = 'GreekHeadwords'
else:
    dict = 'LatinHeadwords'

# perform the search and get all the results
st2 = (st.decode("utf-8"),)
curs.execute("select rowid from %s where head=?" % dict, st2)

r = curs.fetchone()

if r == None:
    st3 = (st.decode("utf-8").capitalize(),)
    curs.execute("select rowid from %s where head=?" % dict, st3)
    r = curs.fetchone()
    if r != None:
        st = st.decode("utf-8").capitalize().encode("utf-8")
        capFound = 1
    else:
        st3 = (st.decode("utf-8").lower(),)
        curs.execute("select rowid from %s where head=?" % dict, st3)
        r = curs.fetchone()
        if r != None:
            st = st.decode("utf-8").lower().encode("utf-8")
            capFound = 1
        else:
            st3 = (strip_accents(st.decode("utf-8")),)
            curs.execute("select rowid from %s where head=?" % dict, st3)
            r = curs.fetchone()
            if r != None:
                st = strip_accents(st)
                accFound = 1
            else:
                curs.execute("select normhead from Transliterated where transhead like ?", st3)
                r = curs.fetchone()
                if r != None:
                    sts4 = (r[0],)
                    curs.execute("select rowid from %s where head like ?" % dict, sts4)
                    r = curs.fetchone()
                    if r != None:
                        st = sts4[0].encode("utf-8")
                        accFound = 1
                        
# required to print out the html
print "Content-Type: text/html; charset=utf-8"
print

print '{'

# if we found the search word
if r != None:
    # select 61 rows centered on the search word
    rownum = r[0] - 31;

    rownum2 = (rownum,)
    curs.execute("select * from %s where rowid > ? limit 61" % dict, rownum2);

    hws = []

    # add the headword of each row to a list
    for row in curs:
        hws.append(row[0].encode("utf-8"))

    i = 0
    
    print '"ww":"'
    
    # if we are close enough to the beginning of the wordwheel
    if hws.index(st) < 30:
        # print out enough blank list items at the beginning
        for j in range(30 - hws.index(st)):
            #print '<li id="w' + str(i) + '" class="other_hws" style="top: -315px;" ></li>'
            print '<li id=\'w' + str(i) + '\' class=\'other_hws\' style=\'top: -315px;\' ></li>'
            i += 1
    
    # print out the headwords in list form
    for hw in hws:
        #print '<li id="w' + str(i) + '" class="other_hws" style="top: -315px;" >' + hw + '</li>'
        print '<li id=\'w' + str(i) + '\' class=\'other_hws\' style=\'top: -315px;\' >' + hw + '</li>'
        if i == 60:
            break
        i += 1
    
    # if we are close enough to the end of the wordwheel
    if i < 60:
        # print out enough blank list items at the end
        while i < 61:
            #print '<li id="w' + str(i) + '" class="other_hws" style="top: -315px;" ></li>'
            print '<li id=\'w' + str(i) + '\' class=\'other_hws\' style=\'top: -315px;\' ></li>'
            i += 1
            
    found = 1

# look for potential parses of the search word

# choose the right lexicon
if dict == "GreekHeadwords":
    lex = sqlite3.connect("GreekLexicon.db")
    curs2 = lex.cursor()
else:
    lex = sqlite3.connect("LatinLexicon.db")
    curs2 = lex.cursor()

st2 = (st.decode("utf-8"),)
curs2.execute("SELECT lemma, code FROM Lexicon WHERE token=?", st2)

lrows = curs2.fetchall()

for lrow in lrows:
    lemma = re.sub('2', '', lrow[0].encode("utf-8"))
    pos = decode(lrow[1])
    
    if r == None:
        mainLemma = lemma
        
        curs.execute("SELECT rowid FROM %s WHERE head=?" % dict, (lrow[0],))

        r = curs.fetchone()
    
    if lemma not in lemmas:
        lemmas[lemma] = [pos]
    else:
        lemmas[lemma] += [pos]
    
lex.close()

# if we found any potential lemmas
if r != None:
    # if we found no word originally
    if not found:
        # act as if the first lemma was the original search term
        rownum = r[0] - 31;

        rownum2 = (rownum,)
        curs.execute("select * from %s where rowid > ? limit 61" % dict, rownum2);

        hws = []

        for row in curs:
            hws.append(row[0].encode("utf-8"))

        i = 0

        print '"ww":"'
        
        # if we are close enough to the beginning of the wordwheel
        if hws.index(mainLemma) < 30:
            # print out enough blank list items at the beginning
            for j in range(30 - hws.index(mainLemma)):
                print '<li id=\'w' + str(i) + '\' class=\'other_hws\' style=\'top: -315px;\' ></li>'
                i += 1
    
        # print out the headwords in list form
        for hw in hws:
            print '<li id=\'w' + str(i) + '\' class=\'other_hws\' style=\'top: -315px;\' >' + hw + '</li>'
            if i == 60:
                break
            i += 1
        
        # if we are close enough to the end of the wordwheel
        if i < 60:
            # print out enough blank list items at the end
            while i < 61:
                print '<li id=\'w' + str(i) + '\' class=\'other_hws\' style=\'top: -315px;\' ></li>'
                i += 1
                
        print '","notice":"' + create_notice() + '"'# + '", "length":' + str(len(lemmas)) + ',"lemmas":' + json.dumps(lemmas)
    
    else:
        print '","notice":"' + create_notice() + '"'# + '", "length":' + str(len(lemmas)) + ',"lemmas":' + json.dumps(lemmas)
        
# if we didn't find any lemmas
else:
    if not found:
        # get the original search term
        sts = st.decode("utf-8")

        # while its still not blank
        while sts != '':
            # remove a letter from the end
            sts = sts[:(len(sts)-1)]
            
            # add the symbol (%) for searching for like items
            sts_like = sts + '%'
            
            # perform the search and get the first result
            sts2 = (sts_like,)
            curs.execute("select rowid from %s where head like ?" % dict, sts2)
            
            r = curs.fetchone()
            
            if r == None:
                sts3 = (sts_like.capitalize(),)
                curs.execute("select rowid from %s where head like ?" % dict, sts3)
                r = curs.fetchone()
                if r == None:
                    sts3 = (sts_like.lower(),)
                    curs.execute("select rowid from %s where head like ?" % dict, sts3)
                    r = curs.fetchone()
                    if r == None:
                        sts3 = (strip_accents(sts_like),)
                        curs.execute("select rowid from %s where head like ?" % dict, sts3)
                        r = curs.fetchone()
                        if r == None:
                            curs.execute("select normhead from Transliterated where transhead like ?", sts3)
                            r = curs.fetchone()
                            if r != None:
                                sts4 = (r[0],)
                                curs.execute("select rowid from %s where head like ?" % dict, sts4)
                                r = curs.fetchone()
            
            if r != None:
                # perform the same actions as if that were the original search term
                rownum = r[0] - 31;

                rownum2 = (rownum,)
                curs.execute("select * from %s where rowid > ? limit 61" % dict, rownum2);

                hws = []

                for row in curs:
                    hws.append(row[0].encode("utf-8"))

                i = 0

                print '"ww":"'

                # if we are close enough to the beginning of the wordwheel
                #if hws.index(sts) < 30:
                    # print out enough blank list items at the beginning
                    #for j in range(30 - hws.index(sts)):
                        #print '<li id=\'w' + str(i) + '\' class=\'other_hws\' style=\'top: -315px;\' ></li>'
                        #i += 1
                        
                # print out the headwords in list form
                for hw in hws:
                    print '<li id=\'w' + str(i) + '\' class=\'other_hws\' style=\'top: -315px;\' >' + hw + '</li>'
                    if i == 60:
                        break
                    i += 1
                
                # if we are close enough to the end of the wordwheel
                #if i < 60:
                    # print out enough blank list items at the end
                    #while i < 61:
                        #print '<li id=\'w' + str(i) + '\' class=\'other_hws\' style=\'top: -315px;\' ></li>'
                        #i += 1
                
                print '","notice":"' + create_notice() + '"'# + ',"length":0,"lemmas":-1'
                
                break
                
print '}'

#hws = [''] * (20 - i) + hws

#hws += [''] * (41 - i) 
    
#print (JSONEncoder().encode(hws))
