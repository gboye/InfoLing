
# coding: utf-8

# In[1]:

import re
import sys
import codecs, csv


# In[2]:

cmuFile=codecs.open("cmudict-0.7b","r", 'utf8')


# In[3]:

elpFileCSV=codecs.open("ELP-Lexicon.csv","r", 'utf8')


# In[4]:

elpFile = csv.reader(elpFileCSV, delimiter=',', quotechar='"')


# In[5]:

lexiconELP=[]
for index,line in enumerate(elpFile):
    if line:
        word=line[0]
        if word.islower() or word.istitle() :
            lexiconELP.append(word.upper())
    else:
        print index


# In[6]:

get_ipython().magic(u'time')
dictionary={}
for index,line in enumerate(cmuFile):
    if ";;;" not in line: #delete header
        entry=line.strip().split("  ")#every entry contains 2 spaces
        word=entry[0] #word is in first column
        syllabes=entry[1:] #beginning of phonetic string in 2nd column
        if word in lexiconELP:
            dictionary[word]=syllabes
#            if len(dictionary)%1000==0:
#                print index,len(dictionary)


# In[7]:

with open('test.csv', 'w') as output:
    for key in sorted(dictionary):
        row=[key]+dictionary[key]
        output.write(key+"  "+" ".join(dictionary[key])+"\n")


# In[8]:

lexiconELP

