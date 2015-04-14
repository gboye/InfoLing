
# coding: utf-8

# #Transformer les TRS
# ##Importer les modules nécessaires
# - codecs est le module qui permet de lire l'encodage UTF8 ou ISO-8859-1 au choix
# - re est le module qui permet d'utiliser des expressions régulières pour analyser une chaine de caractères

# In[13]:

import codecs, re, glob


# ##Déclaration des noms des fichiers

# In[14]:

repTRS="/Users/gilles/Copy/Linguistique et corpus 2014-2015/Corpus_VEGA_FOUCHARD_KANCEL/Transcriptions orthographiques/"
fichiersTRS=glob.glob(repTRS+"*.trs")


# In[15]:

def makeNameXML(nomTRS):
    return nomTRS.replace(".trs",".xml")


# ##Lecture du fichier TRS

# ##Ajout des lignes pour les disfluences et la mise en forme
# - après la ligne de déclaration de l'encodage : la référence de la feuille de style
# - après les lignes de début de disfluences : la balise &lt;disfluence>
# - avant les lignes de fin de disfluences : la balise &lt;/difluence>
# 
# Avec le fichier XML
# >pour chaque ligne
# >>nettoyer la ligne
# >>comparer la ligne avec un event de type disflu
# 
# >>si la ligne est la déclaration d'encodage
# >>>recopier la ligne
# >>>ajouter la référence de la feuille de style
# 
# >>si la ligne est la référence de la feuille de style
# >>>ne rien faire
# 
# >>si la ligne est celle de la DTD
# >>>remplacer la ligne par celle de la DTD adaptée pour accepter les disfluences
# 
# >>si la ligne est du type event de disfluence
# >>>si le dernier attribut vaut begin
# >>>>recopier la ligne
# >>>>ajouter une balise &lt;disfluence>
# 
# >>>si le dernier attribut vaut end
# >>>>ajouter une balise &lt;/disfluence>
# >>>>recopier la ligne
# 
# >>sinon
# >>>recopier la ligne

# In[16]:

for nomTRS in fichiersTRS:
    nomXML=makeNameXML(nomTRS)
    with codecs.open(nomTRS,"r",encoding="ISO-8859-1") as entree:
        transcription=entree.readlines()
    with codecs.open(nomXML,"w",encoding="UTF8") as sortie:
        for ligne in transcription:
            ligne=ligne.strip()
            disfluenceGen=re.match('<Event desc="disflu" type="(noise|lexical|pronounce|language|entities)" extent="(begin|end)"/>',ligne)
            disfluenceSpec=re.match('<Event desc="(Md|Rep|AutoC|NonFinie|MCoup)" type="pronounce" extent="(begin|end)"/>',ligne)        
            if ligne=='<?xml version="1.0" encoding="ISO-8859-1"?>':
                sortie.write(ligne.replace("ISO-8859-1","UTF-8")+"\n")
                sortie.write('<?xml-stylesheet type="text/xsl" href="TRS-Speakers.xsl" ?>'+"\n")
            elif ligne=='<?xml-stylesheet type="text/xsl" href="TRS-Speakers.xsl" ?>':
                pass
            elif ligne=='<!DOCTYPE Trans SYSTEM "trans-14.dtd">':
                sortie.write('<!DOCTYPE Trans SYSTEM "trans-14-corpus.dtd">'+"\n")
            elif disfluenceGen:
                if disfluenceGen.group(2)=="begin":
                    sortie.write(ligne+"\n")
                    sortie.write("<disfluence>"+"\n")
                elif disfluenceGen.group(2)=="end":
                    sortie.write("</disfluence>"+"\n")
                    sortie.write(ligne+"\n")
            elif disfluenceSpec:
                if disfluenceSpec.group(2)=="begin":
                    sortie.write(ligne+"\n")
                    sortie.write('<disfluence type="%s">'%disfluenceSpec.group(1)+"\n")
                elif disfluenceSpec.group(2)=="end":
                    sortie.write("</disfluence>"+"\n")
                    sortie.write(ligne+"\n")
            else:
                sortie.write(ligne+"\n")


# <Event desc="Md" type="pronounce" extent="begin"/> : pour "marqueurs du discours"
# <Event desc="Rep" type="pronounce" extent="begin"/> : pour "répétitions"
# <Event desc="AutoC" type="pronounce" extent="begin"/> : pour "auto correction"
# <Event desc="NonFinie" type="pronounce" extent="end"/> : pour "phrase non finie"
# <Event desc="MCoup" type="pronounce" extent="end"/> : pour "mot coupé"
# 
