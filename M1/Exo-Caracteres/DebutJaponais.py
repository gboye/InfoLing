
# coding: utf-8

# In[27]:

import codecs


# In[28]:

fExercice="Japonais.txt"
base=codecs.open(fExercice,"r", 'utf8')


# In[29]:

consigneLignes=[]
exercices=False
for ligne in base:
    if "===" in ligne:
        exercices=True
    else:
        if exercices:
            (kanji,choix)= ligne.split(":")
            reponses=choix.split(",")
            for element in reponses:
                if element.startswith("="):
                    print "bonne réponse", element[1:]
                else:
                    print "mauvaise réponse", element
        else:
            consigneLignes.append(ligne)


# In[31]:

for ligne in consigneLignes:
    print ligne
print kanji

