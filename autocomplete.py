#!/usr/bin/env python
# coding=utf-8

#from json import JSONEncoder
import sqlite3
import cgi
import cgitb
import re
import string

def bylength(w1, w2):
    w1 = w1.decode("utf-8")
    w2 = w2.decode("utf-8")
    if len(w1) > len(w2):
        return 1
    elif len(w1) == len(w2):
        return 0
    else:
        return -1

table = {'a':'α',
         'b':'β',
         'g':'γ',
         'd':'δ',
         'e':'ε',
         'z':'ζ',
         'h':'η',
         'q':'θ',
         'i':'ι',
         'k':'κ',
         'l':'λ',
         'm':'μ',
         'n':'ν',
         'c':'ξ',
         'o':'ο',
         'p':'π',
         'r':'ρ',
         's':'σ',
         't':'τ',
         'u':'υ',
         'f':'φ',
         'x':'χ',
         'y':'ψ',
         'w':'ω',
         'A':'Α',
         'B':'Β',
         'G':'Γ',
         'D':'Δ',
         'E':'Ε',
         'Z':'Ζ',
         'H':'Η',
         'Q':'Θ',
         'I':'Ι',
         'K':'Κ',
         'L':'Λ',
         'M':'Μ',
         'N':'Ν',
         'C':'Ξ',
         'O':'Ο',
         'P':'Π',
         'R':'Ρ',
         'S':'Σ',
         'T':'Τ',
         'U':'Υ',
         'F':'Φ',
         'X':'Χ',
         'Y':'Ψ',
         'W':'Ω'
         }

cgitb.enable()

form = cgi.FieldStorage()
st = form.getvalue("term")

db = sqlite3.connect("dvlg-wheel.sqlite")
curs = db.cursor()

print "Content-Type: text/html; charset=utf-8"
print

st2 = (st.decode("utf-8") + "%",)
try:
    st.decode("ascii")

except UnicodeDecodeError:
    curs.execute("select * from GreekHeadwords where head like ?", st2)
    
    hws = []
    
    for row in curs:
        hws.append(row[0].encode("utf-8"))
        
    curs.execute("select * from Transliterated where transhead like ?", st2)
    
    for row in curs:
        hw = row[0].encode("utf-8")
        if not hw in hws:
            hws.append(hw)

else:
    curs.execute("select * from LatinHeadwords where head like ?", st2)
    
    hws = []
    
    for row in curs:
        hws.append(row[0].encode("utf-8"))
    
    # Looks for transliterations
    st3 = st
    
    for l, g in table.iteritems():
        if l == 's':
            st3 = re.sub('s\Z', 'ς', st3)
        st3 = re.sub(l, g, st3)
    
    # Check for terminal sigma and normal sigma at end of search term
    st3_2 = re.sub('ς', 'σ', st3)
    st3 = (st3.decode("utf-8") + "%", st3_2.decode("utf-8") + "%")
    
    curs.execute("select * from Transliterated where transhead like ? or transhead like ?", st3)
    
    for row in curs:
        if not row[0].encode("utf-8") in hws:
            hws.append(row[0].encode("utf-8"))
    
    # Converts entire string to lower case and looks for transliterations
    st4 = string.lower(st)
    
    for l, g in table.iteritems():
        if l == 's':
            st4 = re.sub('s\Z', 'ς', st4)
        st4 = re.sub(l, g, st4)
    
    st4_2 = re.sub('ς', 'σ', st4)
    st4 = (st4.decode("utf-8") + "%", st4_2.decode("utf-8") + "%")
    
    curs.execute("select * from Transliterated where transhead like ? or transhead like ?", st4)
    
    for row in curs:
        if not row[0].encode("utf-8") in hws:
            hws.append(row[0].encode("utf-8"))

    # Capitalizes string and looks for transliterations
    st5 = string.capitalize(st)
    
    for l, g in table.iteritems():
        if l == 's':
            st5 = re.sub('s\Z', 'ς', st5)
        st5 = re.sub(l, g, st5)
    
   
    st5_2 = re.sub('ς', 'σ', st5)
    st5 = (st5.decode("utf-8") + "%", st5_2.decode("utf-8") + "%")
    
    curs.execute("select * from Transliterated where transhead like ? or transhead like ?", st5)
    
    for row in curs:
        if not row[0].encode("utf-8") in hws:    
            hws.append(row[0].encode("utf-8"))
            
hws.sort(cmp=bylength)

jsonString = "["

i = 1
count = len(hws)

for hw in hws:
    if i < count:
        jsonString += "\"" + hw + "\", "
    else:
        jsonString += "\"" + hw + "\"]"
    i += 1

print jsonString

#print "\"" + str(hws) + "\""
#print (JSONEncoder().encode(hws))
