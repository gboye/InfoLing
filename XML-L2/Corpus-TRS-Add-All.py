
# coding: utf-8

# In[ ]:




# In[ ]:

import time
import sys
import codecs
import re
import pdb # ajouter pdb.set_trace() à l'endroit où on veut le débugueur
from lxml import etree
import bs4


# #Modifier pour permettre le traitement d'un répertoire ou d'une arborescence plutôt qu'un seul fichier à la fois.

# In[ ]:

import glob


# #Préparation de l'environnement pour le script
# - *dossier* doit être le répertoire où se trouvent vos fichiers (devrait finir par un /)
# - *fichierTRS* contient la liste des noms de vos fichiers TRS à traiter (rempli automatiquement)
# - *fichierLexique* doit être le nom du fichier BDLEXIQUE
# - *fichierExceptions* doit être le nom de votre fichier INCONNUS
# 

# In[ ]:

dossier="/Users/gilles/Copy/Cours/Bordeaux/XML/XML-Ressources/"
fichiersTRS=glob.glob(dossier+"*.trs")
fichierLexique=dossier+"bdlexique.txt"
fichierExceptions=dossier+"inconnus.txt"
fichier_exceptions=True


# Si vous n'avez pas de fichier *inconnus.txt* 
# >mettez *fichier_exceptions=False* au dessus

# #Modif GB 12/04/14
# - mise en texte des deux blocs de traitement de la ligne de commande

# In[ ]:

lexicon=codecs.open(fichierLexique,"r",encoding='utf8')
bdlexique=lexicon.readlines()
lexicon.close()
exceptions=codecs.open(fichierExceptions,"r",encoding='utf8')
inconnus=exceptions.readlines()
exceptions.close()


# In[ ]:

facultatives = 0


# In[ ]:

phon={}
result=[]
nouvellesExceptions = []
output=[]


# ### Préparation des fichiers

# algorithme
# 
# ajouter chaque ligne du fichier à phrases[]

# In[ ]:

def lowerAccents(chaine):
    return chaine.lower()


# ### Normaliser le mot en cours
# 
# algorithme
# 
# + la ponctuation est remplacée par un espace
# + les espaces aux extrémités sont effacés
# + le mot est mis en minuscules

# In[ ]:

def trimer(mot):
    mot=lowerAccents(mot)
    for p in u',;.:-?!()“”‘’‛‟′″´˝"«»':
        mot=mot.replace(p, ' ')
    mot=mot.strip()
    return mot


# In[ ]:

def listerMotsCorpus(rootTRS):
    phrases=[]
    motsPhrases=[]
    elementsPhrases=[]
    motsCorpus=set()
    nPhrases=0
    for ligne in rootTRS.xpath("//Turn//text()"):
        line=ligne.strip()
    #    print nPhrases, line
        phrases.append(line)
        elements=re.findall(ur"[\wâàéèêëîïôùûüçÂÀÉÈÊËÎÏÔÙÛÜÇæœÆŒ]+['’]?|[-.…,—–()\[\]\/#\"“”‘«»<>'’=~]| [;!?:]", line)
        mots=[x for x in elements if not x in u"-.…,—–()\[\]\/#\"“”‘«»<>'’=~" and not x in [" ;"," !"," ?"," :"]]
        elements=[x for x in elements if x!=" "]
        elementsPhrases.append(elements)
        phrasePropre = u""
        for mot in mots:
            mot = trimer(mot)
            phrasePropre += mot+u" "
            motsCorpus.add(mot)
        phraseMots = phrasePropre.strip()
        phraseMots = phrasePropre.split()        
        motsPhrases.append(phraseMots)
        nPhrases+=1
    return (motsCorpus,motsPhrases,elementsPhrases)


# algorithme
# 
# extraire de BDLex 0.forme fléchie, 1.phonétique, 2.liaison, 3.cat-gram, 4.genre+nombre

# algorithme
# 
# extraire du fichier d'exceptions les mêmes données que pour BDLex

# #Modif GB 12/04/14
# - fait une liste des exceptions lues pour ne pas les rajouter à la fin
# - éviter de tenir compte des exceptions non renseignées
#  - les mots du fichier exceptions sans transcriptions étaient transcrits par une chaine vide...

# ## Fonctions

# ### Vérifier si le mot existe
# 
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

# In[ ]:

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
                    nouvellesExceptions.append(mot)
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


# ### 2. traduire le SAMPA de BDLexique en API

# #Modif GB 12/04/14
# - ajout du r et du â
# - ajout des exemples associés en dessous

# In[ ]:

# traduire SAMPA-BDLex en API

def sampa2api(sampa):
    if isinstance(sampa,str):
        api=sampa.decode("utf8")
    else:
        api=sampa
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
    return api


# ### 4. Vérifier si la liaison est possible

# algorithme
# 
# + si le mot courant et le suivant ne sont pas dans lexicon, pas de liaison
# + si le mot a une consonne dans le champ de la voyelle de liaison, check1 est vrai
# + si le mot suivant commence par une voyelle, check2 est vrai
# 
#   si check1 et check2 sont vrais, il y a liaison

# In[ ]:

def liaison_possible(phrase ,mot , mot_numero):
    check1=0
    check2=0
    if mot in phon and phrase[mot_numero+1] in phon:
        consonnes=['k"', '(kt)"', 'n"', 'p"', 'R"', '@t"', 't"', '-V', '+V', '@z"', 'z"']
        phoneme=phon[mot][2]
        for phoneme in consonnes:
            check1=1
        
        voyelles=["H", "j", "w", "E", "a", "2", "9", "6", "@", "y", "u", "O", u"ò", "o", "e", u"è", u"ê", u"û", u"ô", "i"]
        mot_suivant=phon[phrase[mot_numero+1]][1]
        for v in voyelles:
            if mot_suivant.startswith(v):
                check2=1

    if check1 and check2 :
        return True
    else:
        return False


# ### 5. vérifier si la liaison est obligatoire

# algorithme
# 
# + si le mot courant et le suivant sont dans un des cas de figure, il y a liaison
# + sinon pas de liaison

# In[ ]:

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

# In[ ]:

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

# ## Traitement

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

# In[ ]:

from lxml.builder import E


# #Début de l'enchassement en XML (7/12/15)
# - récupérer la ponctuation et les sauts de lignes pour rendre le texte lisible
# - ajouter le reste des informations du lexique dans la balise

# In[ ]:

def enchasseBDLexique(nphrase,nmot,liaison=False):
    mot=motsPhrases[nphrase][nmot]
    if mot in phon: 
        phono=sampa2api(phon[mot][1])
        if liaison:
            phono+=sampa2api(phon[mot][2])
        cat=phon[mot][3]
        if cat in [u"J",u"K"]:
            cat=u"Adj"
        ms=phon[mot][4]
        vs=phon[mot][5]
        lexeme=phon[mot][6].upper()
        if u" " in vs:
            vs=u""
    else:
        phono=verifier_mot(mot)[:-1]
        cat=u"???"
        ms=""
        vs=""
        lexeme="???"
    result=E.motBDL(mot,{"cat":cat,"ms":ms,"vs":vs,"phon":phono,"lexeme":lexeme})
#    print etree.tostring(result,encoding="utf8")
#    print (cat,ms,vs,phono,mot)
#    u'<mot cat="%s" ms="%s" vs="%s" phon="%s">%s</mot>' % (cat,ms,vs,phono,mot)
    return result
    
def enchasseXML(mot, phono):
    if isinstance(phono,str):
        phono=phono.decode("utf8")
    result=E.motBDL(mot,{"phon":phono})
#    u'<mot phon="%s">%s</mot>' % (phono, mot)
    return result

def enchasseTour(phrase):
    result=E.tour(phrase)
    return result

def enchasseNonMot(nonmot):
    result=E.punct(nonmot)
#    u'<punct>%s</punct>' % (nonmot)
    return result


# In[ ]:

def traitementTRS(rootTRS):
    a=1
    nPhrase=0
    for ligne in rootTRS.xpath("//Turn//text()"):
        phrase=ligne.strip()
        api=E.tour()
        mot_numero=0
        element_numero=0
        while mot_numero <= len(motsPhrases[nPhrase])-2:
            while motsPhrases[nPhrase][mot_numero]!=elementsPhrases[nPhrase][element_numero].lower():
                api.append(enchasseNonMot(elementsPhrases[nPhrase][element_numero]))
                element_numero+=1
            if liaison_possible(motsPhrases[nPhrase], motsPhrases[nPhrase][mot_numero], mot_numero):

                if liaison_obligatoire(motsPhrases[nPhrase], motsPhrases[nPhrase][mot_numero], mot_numero):
                    api.append(enchasseBDLexique(nPhrase,mot_numero,True))

                elif liaison_facultative(motsPhrases[nPhrase], motsPhrases[nPhrase][mot_numero], mot_numero):
                    if facultatives:
                        api.append(enchasseBDLexique(nPhrase,mot_numero,True))
                    else :
                        api.append(enchasseBDLexique(nPhrase,mot_numero))
                else:
                    api.append(enchasseBDLexique(nPhrase,mot_numero))
            else:
                api.append(enchasseBDLexique(nPhrase,mot_numero))
            mot_numero = mot_numero+1
            element_numero+=1
        if len(motsPhrases[nPhrase])>0 and mot_numero==len(motsPhrases[nPhrase])-1:
            api.append(enchasseBDLexique(nPhrase,len(motsPhrases[nPhrase])-1))
        a=a+1
        ligne.getparent().append(api)
        nPhrase+=1


# #Modif GB 12/04/14
# - Insertion d'un set sur les nouvellesExceptions pour éviter les entrées multiples
# - Ajout d'un test pour vérifier que les nouvellesExceptions sont nouvelles
# 
# #TO DO
# - Ajouter un message pour dire que le résultat a été concaténé au fichier existant si c'est le cas.

# In[ ]:

def extraireMotsTRS(motsCorpus,phon):
    for entry in bdlexique:
        entry=entry.strip()
        p=entry.split(u';')
        if p[0].lower() in motsCorpus:
            if p[2]=="@" and not p[3] in ["N","V","J","K"]:
                p[1]+=p[2]
                p[2]=""
                if len(p)<7:
                    for i in range(len(p)+1,7):
                        p.append("")
            phon[p[0].lower()]=(p[0],p[1],p[2],p[3],p[4],p[5],p[6])
    return phon


# In[ ]:

if fichier_exceptions:
    oldExceptions=[]
    for entry in inconnus:
        entry=entry.strip()
        p=entry.split(";")
        if len(p[1])!=0:
            if len(p)<7:
                for i in range(len(p)+1,7):
                    p.append("")
            phon[p[0].lower()]=(p[0],p[1],p[2],p[3],p[4],p[5],p[6])
        oldExceptions.append(p[0].lower())


# In[ ]:

#1.2.b. mettre les phrases phonémisées dans un fichier
enteteXML=[
            u'<?xml version="1.0" encoding="UTF8" standalone="yes"?>',
            u'<?xml-stylesheet type="text/xsl" href="phonemise-TRS.xsl"?>',
            u'<!DOCTYPE Trans SYSTEM "trans-14-corpus.dtd">'
          ]

#print [etree.tostring(rootTRS,pretty_print=True,encoding="utf8").decode("utf8")]

for fichierTRS in fichiersTRS:
    fichierBDL=fichierTRS[:-4]+"-BDL.xml"
    xmlTRS=etree.parse(fichierTRS)
    rootTRS=xmlTRS.getroot()
    (motsCorpus,motsPhrases,elementsPhrases)=listerMotsCorpus(rootTRS)
    phon=extraireMotsTRS(motsCorpus,phon)
    traitementTRS(rootTRS)
    with codecs.open(fichierBDL, "w", encoding='utf8') as f:
        for ligne in enteteXML:
            f.write(ligne+u"\n")
        f.write(etree.tostring(rootTRS,pretty_print=True,encoding="utf8").decode("utf8"))


# In[ ]:

#1.2.a. mettre la liste des inconnus dans le fichier inconnus.txt
with codecs.open(fichierExceptions, "a", encoding='utf8') as f:
    for n in set(nouvellesExceptions):
        if not (n in oldExceptions): 
            f.write(n+u";;;;;;")
            f.write("\n")


# In[ ]:

nouvellesExceptions

