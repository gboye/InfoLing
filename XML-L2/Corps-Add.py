
# coding: utf-8

# In[1]:

import time
import sys
import codecs
import re
import pdb # ajouter pdb.set_trace() à l'endroit où on veut le débugueur


# In[2]:

from os.path import expanduser
home = expanduser("~")
repRessources=home+"/Copy/Cours/Bordeaux/XML/XML-Ressources/"
repCorpus=home+"/Copy/Linguistique et corpus 2014-2015/CHOW-WING-BOM_PEDEZERT_VERCOUTERE/Phonémisation/scripts-Phonemisation-CWBCPPVE-"
text="petitsmots.txt"


# #Modif GB 12/04/14
# - mise en texte des deux blocs de traitement de la ligne de commande

# if len(sys.argv) < 3:
#     print ("Veuillez renseigner tous les champs  : \n 1. un fichier segmenté \n 2. le fichier du lexique \n 3. éventuellement un fichier d'exceptions")
#     sys.exit()
# 
# # ouvre le fichier segmenté et affiche un message d'erreur s'il ne peut pas être ouvert
# try:
#     fichier=codecs.open(sys.argv[1],"r")
# except IOError:
#     print ('le fichier "'+ sys.argv[1]+ '" ne peut pas être ouvert',)
#     sys.exit()
# # ouvre BDLex et affiche un message d'erreur s'il ne peut pas être ouvert
# try:
#     lexicon=codecs.open(sys.argv[2],"r")
# except IOError:
#     print ('le fichier "'+ sys.argv[2]+ '" ne peut pas être ouvert',)
#     sys.exit()
# # ouvre le fichier d'exceptions(s'il est là) et affiche un message d'erreur s'il ne peut pas être ouvert
# fichier_exceptions=False # pour ne pas exécuter la préparation des exceptions s'il n'y a pas de fichier
# if len(sys.argv) == 4:
#     try:
#         exceptions=codecs.open(sys.argv[3],"r")
#         fichier_exceptions=True
#     except IOError:
#         print ('le fichier "'+ sys.argv[3]+ '" ne peut pas être ouvert', )
#         sys.exit()
#                 
#                 # ajouter les liaisons facultatives ou pas ?
# facultatives=input("Voulez-vous ajouter les liaisons facultatives ou pas ?\n1 = Oui, 0 = Non (suivi d'Entrée) : ")
                
# #Modif GB 12/04/14
# - extension du bloc pour permettre d'ajouter les trois fichiers à la main

# In[3]:

fichierLexique=repRessources+"bdlexique-gb-110217-utf8.txt"
lexicon=codecs.open(fichierLexique,"r")
fichierCorpus=repCorpus+text
fichier=codecs.open(fichierCorpus,"r")
fichierExceptions=repCorpus+"inconnus.txt"
exceptions=codecs.open(fichierExceptions,"r")
fichier_exceptions=True


# In[4]:

facultatives = 0


# In[5]:

phrases=[]
phon={}
result=[]
nouvellesExceptions = []
output=[]


#### Préparation des fichiers

# algorithme
# 
# ajouter chaque ligne du fichier à phrases[]

# In[6]:

def lowerAccents(chaine):
    if isinstance(chaine,str):
        try:
            result=chaine.decode("utf8").lower().encode("utf8")
        except:
            print chaine
        return result
    elif isinstance(chaine,unicode):
        return chaine.lower().encode('utf8')


# In[7]:

for line in fichier:
    line=line.strip()
    if line != '':
        phrases.append(line)


# In[8]:

fichier.close()


# algorithme
# 
# extraire de BDLex 0.forme fléchie, 1.phonétique, 2.liaison, 3.cat-gram, 4.genre+nombre

# In[9]:

for entry in lexicon:
    entry=entry.strip()
    p=entry.split(';')
    phon[p[0].lower()]=(p[0],p[1],p[2],p[3],p[4])


# In[10]:

lexicon.close()


# algorithme
# 
# extraire du fichier d'exceptions les mêmes données que pour BDLex

# #Modif GB 12/04/14
# - fait une liste des exceptions lues pour ne pas les rajouter à la fin
# - éviter de tenir compte des exceptions non renseignées
#  - les mots du fichier exceptions sans transcriptions étaient transcrits par une chaine vide...

# In[11]:

if fichier_exceptions:
    oldExceptions=[]
    for entry in exceptions:
        entry=entry.strip()
        p=entry.split(';')
        if len(p[1])!=0:
            phon[p[0].lower()]=(p[0],p[1],p[2],p[3],p[4])
        oldExceptions.append(p[0].lower())


# In[12]:

exceptions.close()


# In[13]:

for exception in oldExceptions:
    print (exception)


### Fonctions

#### 1. Vérifier si le mot existe

# algorithme
# 
# + si le mot est dans BDLex, ok
# + s'il y a un espace dans le mot,
#     * le mot est divisé en deux et
#     * si les mots existent dans bdlex, ok
#     * sinon les mots sont ajoutés aux nouvelles exceptions et mis entre étoiles
# + s'il y a un apostrophe dans le mot,
#     * le mot est divisé en deux
#     * si les mots existent dans bdlex, ok
#     * sinon les mots sont ajoutés aux nouvelles exceptions et mis entre étoiles
# + dans les autres cas, le mot est ajouté aux nouvelles exceptions et mis entre étoiles

# In[14]:

def verifier_mot(mot):
        sampa=""
        if mot in phon.keys():
            sampa += phon[mot][0]
        elif " " in mot:
            mots = mot.split()
            for mot in mots:
                if mot in phon.keys():
                    sampa += phon[mot][0]+" "
                elif mot != "":
                    sampa += "***"+mot+"*** "
        elif "'" in mot:
            mots = mot.split("'")
            mots[0]=mots[0]+"'"
            for mot in mots:
                if mot in phon.keys():
                    sampa += phon[mot][0]+" "
                elif mot != "":
                    nouvellesExceptions.append(mot)
                    sampa += "***"+mot+"*** "
        elif mot != "": 
            nouvellesExceptions.append(mot)
            sampa="***"+mot+"*** "
        return sampa


# In[15]:

verifier_mot("manger")


# In[46]:

verifier_mot("aujourd'hui")


# In[17]:

verifier_mot("mangr")


# In[18]:

verifier_mot("jacqueline")


# In[19]:

verifier_mot("manger mot")


# In[20]:

verifier_mot("manger mt")


# In[21]:

verifier_mot("j'ai")


# In[22]:

verifier_mot("côté")


#### 2. traduire le SAMPA de BDLexique en API

# #Modif GB 12/04/14
# - ajout du r et du â
# - ajout des exemples associés en dessous

# In[62]:

# traduire SAMPA-BDLex en API
def sampa2apiORIG(sampa):
    api=re.sub('S','ʃ',sampa) 
    api=re.sub('Z','ʒ', api)
    api=re.sub('N','ŋ',api)
    api=re.sub('J','ɲ',api)
    api=re.sub('r','ʁ',api) 
    api=re.sub('H','ɥ',api)
    api=re.sub('E','ɛ',api)
    api=re.sub('2','ø',api)
    api=re.sub('9','œ',api)
    api=re.sub('6','ə',api)
    api=re.sub('O','ɔ',api)
    api=re.sub('è','e',api)   
    api=re.sub('ò','o',api)    
    api=re.sub('â','ɑ̃',api)   
    api=re.sub('ê','ɛ̃',api)   
    api=re.sub('û','œ̃',api)  
    api=re.sub('ô','ɔ̃',api)       
    api=re.sub('@','ə',api)
    api=re.sub('n"','n',api) 
    api=re.sub('t"','t',api) 
    api=re.sub('z"','z',api) 
    api=re.sub('R"','ʁ',api) 
    api=re.sub('p"','p',api) 
    return api

def sampa2api(sampa):
    api=sampa.decode("utf8")
    api=api.replace(u'S',u'ʃ') 
    api=api.replace(u'Z',u'ʒ')
    api=api.replace(u'N',u'ŋ')
    api=api.replace(u'J',u'ɲ')
    api=api.replace(u'r',u'ʁ') 
    api=api.replace(u'H',u'ɥ')
    api=api.replace(u'E',u'ɛ')
    api=api.replace(u'2',u'ø')
    api=api.replace(u'9',u'œ')
    api=api.replace(u'6',u'ə')
    api=api.replace(u'O',u'ɔ')
    api=api.replace(u'è',u'e')   
    api=api.replace(u'ò',u'o')    
    api=api.replace(u'â',u'ɑ̃')   
    api=api.replace(u'ê',u'ɛ̃')   
    api=api.replace(u'û',u'œ̃')  
    api=api.replace(u'ô',u'ɔ̃')       
    api=api.replace(u'@',u'ə')
    api=api.replace(u'n"',u'n') 
    api=api.replace(u't"',u't') 
    api=api.replace(u'z"',u'z') 
    api=api.replace(u'R"',u'ʁ') 
    api=api.replace(u'p"',u'p') 
    return api.encode("utf8")


# In[63]:

sampa2api(phon["ai"][1])


# In[64]:

sampa2api(phon["chat"][1])


# In[65]:

sampa2api(phon["aucun"][1])


# In[27]:

sampa2api(phon["chant"][1])


# In[28]:

sampa2api(phon["marché"][1])


# sampa2api(phon["jacqueline"][1])

#### 3. trimer le mot en cours

# algorithme
# 
# + la ponctuation est remplacée par un espace
# + les espaces aux extrémités sont effacés
# + le mot est mis en minuscules

# In[29]:

def trimer(mot):
    mot=lowerAccents(mot)
#    for p in ',;.:-?!()"':
    for p in ',;.:-?!()“”‘’‛‟′″´˝"«»':
        mot=mot.replace(p, ' ')
    mot=mot.strip()
    return mot


# In[30]:

trimer(",;. :trois-?!( )")


# In[31]:

trimer("(essai)chaud")


# In[32]:

trimer("garçon.")


# In[33]:

trimer("vont-ils")


# In[34]:

chaine=u"côté"
print chaine,len(chaine)
trimer(chaine)


# In[35]:

trimer("y'a")


#### 4. Vérifier si la liaison est possible

# algorithme
# 
# + si le mot courant et le suivant ne sont pas dans lexicon, pas de liaison
# + si le mot a une consonne dans le champ de la voyelle de liaison, check1 est vrai
# + si le mot suivant commence par une voyelle, check2 est vrai
# 
#   si check1 et check2 sont vrais, il y a liaison

# In[36]:

def liaison_possible(phrase ,mot , mot_numero):
    check1=0
    check2=0
    if mot in phon and phrase[mot_numero+1] in phon:
        consonnes=['k"', '(kt)"', 'n"', 'p"', 'R"', '@t"', 't"', '-V', '+V', '@z"', 'z"']
        phoneme=phon[mot][2]
        for phoneme in consonnes:
            check1=1
        
        voyelles=["H", "j", "w", "E", "a", "2", "9", "6", "@", "y", "u", "O", "ò", "o", "e", "è", "ê", "û", "ô", "i"]
        mot_suivant=phon[phrase[mot_numero+1]][1]
        for v in voyelles:
            if mot_suivant.startswith(v):
                check2=1

    if check1 and check2 :
        return True
    else:
        return False


#### 5. vérifier si la liaison est obligatoire

# algorithme
# 
# + si le mot courant et le suivant sont dans un des cas de figure, il y a liaison
# + sinon pas de liaison

# In[37]:

def liaison_obligatoire(phrase, mot, mot_numero):
    determinant=["d", "P"]
    nom=["N", "G", "M"]
    adjectif=["J", "G", "M"]
    pronompers=["P"]
    verbe=["V"]
    catgram_mot1=phon[phrase[mot_numero]][3]
    catgram_mot2=phon[phrase[mot_numero+1]][3]

    if catgram_mot1 in determinant and catgram_mot2 in nom :
        return True

    elif catgram_mot1 in determinant and catgram_mot2 in adjectif :
        return True
 
    elif catgram_mot1 in pronompers and catgram_mot2 in verbe :
        return True

    elif catgram_mot1 in verbe and catgram_mot2 in pronompers :
        return True

    else:
        return False


# In[48]:

phon["sommes"]


# In[39]:

phon["armes"]


# In[40]:

phon["cet"]


# Cas de figure possibles:
# 
# - DET + N
#     * ri + N:   d'animal, 
#     * di + N:   certains éléphants
#     * rd + N:   les animaux
#     * dd + N:   ces étés, cet été
#     * dp + N:   ton anorak
#     * rc + N:   aux armes
# - DET + ADJ:
#     * ri + ADJ:   d'énormes
#     * di + ADJ:   plusieurs immenses
#     * rd + ADJ:   les immenses
#     * dd + ADJ:   cet immense
#     * dp + ADJ:   son immense
#     * rc + ADJ:   aux immenses
# - PERS + V:
#     * SS + V:   m'épate
# - V + PRO PERS: 
#     * V + SS:   vont-ils
# 

# algorithme
# 
# + si le mot courant et le suivant sont dans un des cas de figure, il y a liaison
# + sinon pas de liaison

# In[41]:

# vérifier si la liaison est facultative
def liaison_facultative(phrase, mot, mot_numero):
    #pdb.set_trace()
    nom=["N", "G", "M"]
    pluriel=["MP", "FP"]
    adjectif=["J", "G", "M"]
    verbe=["V"]
    pronompers=["P"]
    adverbe=["A"]
    preposition=["p"]
    catgram_mot1=phon[phrase[mot_numero]][3]
    catgram_mot2=phon[phrase[mot_numero+1]][3]
    genre_mot1=phon[phrase[mot_numero]][4]
    
    if (catgram_mot1 in nom) and (phon[phrase[mot_numero]][4] in pluriel) and (catgram_mot2 in adjectif) : 
        return True

    elif (catgram_mot1 in verbe) and (catgram_mot2 not in pronompers):
        return True

    elif catgram_mot1 in adverbe :
        return True
    
    elif catgram_mot1 in preposition : 
        return True

    else :
        return False


# Cas de figure possibles :
# 
# - N pl + ADJ: 
#     * N + ADJ: monstres énormes 
#     * G + ADJ: rivaux énormes
# - VERBE + TOUT-SAUF-PRO-PERS:
#     * V + N sont éléphants
#     * V + G sommes abdicaires
#     * V + V sommes assis
#     * V + A sommes admirablement
#     * V + p sommes autour de
#     * V + di ont aucune
#     * V + rc sommes au
# - ADV + QQCH:
#     * ADV + N vraiment abruti
#     * ADV + G vraiment abandonné
#     * ADV + V vraiment aimé
#     * ADV + J vraiment étonnant
#     * ADV + ss vraiment ils
#     * ADV + A vraiment étonnamment
#     * ADV + p vraiment attendu
#     * ADV + di vraiment autre 
#     * ADV + rc vraiment au
# - PREP + QQCH:
#     * PREP + N très amoureux
#     * PREP + G très abandonné
#     * PREP + V très aimé
#     * PREP + J très étonnant
#     * PREP + SS très ils
#     * PREP + A très étonnamment
#     * PREP + p très attendu
#     * PREP + di très autre
#     * PREP + rc très au
# 

### Traitement

# + Partie 1
# *chaque phrase est prise individuellement,
#     * découpée en blocs,
#         * qui sont chacuns trimés si ce sont des mots
#         * s'il y a plusieurs mots dans le bloc, ils sont séparés
#     + Partie 2
#     * pour chaque couple de mots
#         * si la liaison est possible,
#             * et qu'elle est obligatoire, l'api avec la liaison est généré
#             * et qu'elle est facultative,
#                 * si l'utilisateur l'a choisi, l'api avec la liaison est généré
#                 * sinon l'api sans la liaison est généré
# 
#         + Partie 3
#         * si la liaison n'est pas possible,
#             * si le mot est dans bdlex, l'api est généré
#             * sinon le mot est laissé tel quel (il a déjà les étoiles)        
# 
#     * pour le dernier mot de la phrase, 
#         * si le mot est dans bdlex, l'api est généré
#         * sinon le mot est laissé tel quel (il a déjà les étoiles) 
# 
# + Partie 4
# * le message à l'utilisateur et la phrase en api est imprimée

# #Modif GB 12/04/14
# - suppression du délai dans la boucle
#  - pour 1500 lignes => 3 secondes sans ralentisseur, 1503 secondes avec 

# In[42]:

def enchasseXML(mot, phono):
    result='<mot phon="%s">%s</mot>' % (phono, mot)
    return result


# #Début de l'enchassement en XML (7/12/15)
# - récupérer la ponctuation et les sauts de lignes pour rendre le texte lisible
# - ajouter le reste des informations du lexique dans la balise

# In[43]:

# partie 1
a=1
for phrase in phrases:
    api = ""
    mots=re.split("[->< /@\_]", phrase)
    phrasePropre = ""
    for mot in mots:
        mot = trimer(mot)
        mot = verifier_mot(mot)
        phrasePropre += mot+" "
    phraseMots = phrasePropre.strip()
    phraseMots = phrasePropre.split()

    # partie 2    
    mot_numero=0
    while mot_numero <= len(phraseMots)-2:
        
        if liaison_possible(phraseMots, phraseMots[mot_numero], mot_numero):
 
            if liaison_obligatoire(phraseMots, phraseMots[mot_numero], mot_numero):
                api += enchasseXML(phraseMots[mot_numero],sampa2api(phon[phraseMots[mot_numero]][1])+sampa2api(phon[phraseMots[mot_numero]][2]))

            elif liaison_facultative(phraseMots, phraseMots[mot_numero], mot_numero):
                if facultatives:
                    api += enchasseXML(phraseMots[mot_numero],sampa2api(phon[phraseMots[mot_numero]][1])+sampa2api(phon[phraseMots[mot_numero]][2]))
                else :
                    api += enchasseXML(phraseMots[mot_numero],sampa2api(phon[phraseMots[mot_numero]][1]))+" "
            else:
                if phraseMots[mot_numero] in phon:
                    api += enchasseXML(phraseMots[mot_numero],sampa2api(phon[phraseMots[mot_numero]][1]))+" "
                else:
                    api += enchasseXML(phraseMots[mot_numero],"?phon?")+" "
        # partie 3
        else:
            if phraseMots[mot_numero] in phon:
                api += enchasseXML(phraseMots[mot_numero],sampa2api(phon[phraseMots[mot_numero]][1]))+" "
            else:
                api += enchasseXML(phraseMots[mot_numero],"?phon?")+" "
        mot_numero = mot_numero+1
    
    if phraseMots[len(phraseMots)-1] in phon:
        api += enchasseXML(phraseMots[len(phraseMots)-1],sampa2api(phon[phraseMots[len(phraseMots)-1]][1]))
    else:
        api += enchasseXML(phraseMots[mot_numero],"?phon?")+" "
    
    # partie 4
    sys.stdout.write("Traitement de "+str(a)+" sur "+ str(len(phrases))+ " phrases. "+"\n"+phrase+"\n"+api+"\n\n"+chr(20))
    sys.stdout.flush()
    #time.sleep(1)
    a=a+1
    output.append(api)


# #Modif GB 12/04/14
# - Insertion d'un set sur les nouvellesExceptions pour éviter les entrées multiples
# - Ajout d'un test pour vérifier que les nouvellesExceptions sont nouvelles
# 
# #TO DO
# - Ajouter un message pour dire que le résultat a été concaténé au fichier existant si c'est le cas.

# In[44]:

#1.2.a. mettre la liste des inconnus dans le fichier inconnus.txt
with open("inconnus.txt", "a") as f:
    for n in set(nouvellesExceptions):
        if not (n in oldExceptions): 
            f.write(n+";;;;;")
            f.write("\n")
        
#1.2.b. mettre les phrases phonémisées dans un fichier
with open("phonemise.xml", "a") as f:
    for o in output:
        f.write(o)
        f.write("\n")

with open("verification.txt", "a") as f:
    for a in range(len(output)-2):
        f.write(phrases[a]+"\n"+output[a])
        f.write("\n\n")


# In[44]:



