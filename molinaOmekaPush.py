# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 09:11:57 2017

@author: Michael Nauge
description
"""
import sys
import csv
import os

import omekaRestConnector as omkCon

import omekaPushFromCsv as omkPusher 

import toolsForCSV as toolCSV

from shutil import copyfile

#pour outrepasser le nombre de caractere par cellule
csv.field_size_limit(sys.maxsize)


def transformDataFileForMolinaOmekaPush(pathDataFile, pathDirOut, pathDataFileTransformed):
    listOutputFileTmp = []
    
    #suppression des column 'urlEditItem','urlShowItem'
    outputFileTmp = pathDirOut+"Molina_delCol.csv"
    listOutputFileTmp.append(outputFileTmp)
    
    listColumnNames = ['urlEditItem','urlShowItem']
    toolCSV.suppColumn(pathDataFile, outputFileTmp, listColumnNames)
    
    
    #ajout des column
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molinao_addCol.csv"
    listOutputFileTmp.append(outputFileTmp)
    
    #['Linked in collection branch','Linked in collection leaf', 'Nkl dataType','Nkl dataFormat','Nkl hdl root collection','Nkl hdl branch collection','Nkl hdl leaf collection','Nkl hdl leaf data','Nkl statut']
    listColumnNames = ['Linked in collection', 'Linked in item','dataType','dataFormat','Omk item id','Omk ressource id','Omk statut']
    toolCSV.addColumnToFileWithoutValue(inputFile, outputFileTmp, listColumnNames)
    
    
    #duplication
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_dupCol.csv"
    listOutputFileTmp.append(outputFileTmp)
    
    columnNameIn = 'Type'
    columnNameDup = 'Linked in collection'
    appendMode =False
    separator = ''
    toolCSV.duplicateColumn(inputFile, outputFileTmp, columnNameIn, columnNameDup, appendMode, separator)
    
    
    #rename conditionel pour correction et ou fusion
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molinao_CorrecPresse.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Presse (Article rédigé par l’auteur)'
    valueReplace = 'Presse (Articles rédigés par l’auteur)'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_MergeTheatre1.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Théâtre (Pièce)'
    valueReplace = 'Théâtre'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_MergeTheatre2.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Théâtre (Intermède)'
    valueReplace = 'Théâtre'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_MergeTheatre3.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Mise en scène'
    valueReplace = 'Théâtre'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_MergePoesie1.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Poésie (Recueil)'
    valueReplace = 'Poésie'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_MergePoesie2.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Poésie (Poème)'
    valueReplace = 'Poésie'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_CorrecDoc.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Documentation - Autre type de document'
    valueReplace = 'Documentation - Autres types de documents'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_CorrecBio.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Dossier biographique - Autre type de document'
    valueReplace = 'Dossier biographique - Autres types de documents'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_MergeRecep1.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Réception de l’œuvre - Plan de classement et inventaire'
    valueReplace = 'Réception de l’oeuvre'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_MergeRecep2.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Réception de l’œuvre - Travail de valorisation'
    valueReplace = 'Réception de l’oeuvre'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_MergeRecep3.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'Linked in collection'
    valueTest = 'Réception de l’œuvre - Réception'
    valueReplace = 'Réception de l’oeuvre'
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    
    #ajout des prefix
    dicPrefix = {}
    
    dicPrefix['Auteur analyse'] = 'Auteur analyse : '
    dicPrefix['Auteur description'] = 'Auteur description : '
    dicPrefix['Auteur révision'] = 'Auteur révision : '
    dicPrefix['Auteur transcription'] = 'Auteur transcription : '
    #dicPrefix['Contexte géographique']
    #dicPrefix['Coverage']
    #dicPrefix['Creator']
    #dicPrefix['Date']
    #dicPrefix['Description']
    dicPrefix['Destinataire'] = 'Destinataire : '
    dicPrefix['Directeur de la publication'] = 'Directeur publication : '
    dicPrefix['Etat général'] = 'Etat général : '
    dicPrefix['Etat génétique'] = 'Etat génétique : '
    dicPrefix['Format'] = 'Pagination et Dimension : '
    #dicPrefix['Language'] =
    dicPrefix["Lieu d'expédition"] = 'Lieu expédition : ' 
    dicPrefix['Localisation'] = 'Localisation du document : '
    dicPrefix['Nature du document'] = "Mode d'agencement : "
    dicPrefix['Notes'] = 'Notes : '
    dicPrefix['Numéro de la publication'] = 'Numéro publication : '
    dicPrefix['Publication'] = 'Date de publication : '
    #dicPrefix['Publisher'] = 
    dicPrefix['Périodicité'] = 'Périodicité : '
    dicPrefix['Collection'] = 'Recueil : '
    #dicPrefix['Relation'] = 
    dicPrefix['Relations Génétiques'] = 'Relations Génétiques : '
    dicPrefix['Autres ressources en relations'] = 'Autres ressources en relations : '
             
    dicPrefix['Représentation'] = 'Représentation : '
    #dicPrefix['Rights'] = 
    #dicPrefix['Source'] = 'Cote du document : '
    dicPrefix['Sous-titre'] = 'Sous-titre : '
    #dicPrefix['Subject'] = 
    dicPrefix['Support'] = 'Support : ' 
    #dicPrefix['Title'] = 
    dicPrefix['Titre de la publication'] = 'Titre publication : '
    dicPrefix['Type'] = 'Genre : ' 
    dicPrefix['Type de publication'] = 'Type de publication : '
    #dicPrefix['Type document politique'] = 'Domaine : '
    dicPrefix['Lieu de publication'] = 'Lieu de publication : '
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_prefixDic.csv"
    
    toolCSV.addPrefixValueFixedFromDic(inputFile,outputFileTmp, dicPrefix)
    
    
    #remplir la column 'dataType' (par Text ou Image ou Sound)
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_dataType.csv"
    listOutputFileTmp.append(outputFileTmp)
    
    columnNameTest = 'Type'
    columnNameOut = 'dataType'
    contentValue = 'Iconographie'
    suffixValueTrue = 'Image'
    suffixValueFalse = 'Text'
    
    toolCSV.addSuffixValueConditional(inputFile, outputFileTmp, columnNameTest, columnNameOut, contentValue, suffixValueTrue, suffixValueFalse)
    
    #decoupage 1 ligne par fichier
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_splitByFile.csv"
    
    columnName = "file"
    separator = " | "
    columnNameNumbered = "Page"
    
    toolCSV.creatLineFromMultiValuesInColumn(inputFile, outputFileTmp, columnName, separator, columnNameNumbered)  
    
    
    #remplir la column 'dataFormat' (par JPG)
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_dataFormat.csv"
    listOutputFileTmp.append(outputFileTmp)
    #on a que du JPG (quand on en a pas c'est qu'on a pas encore le scan)
    columnNameOut = 'dataFormat'
    value = 'JPG'
    toolCSV.addValueFixed(inputFile,outputFileTmp,columnNameOut,value)
    
    
    #remplir les colonnes 'Linked in item' et 'Title'
    #'Title' omekaRessourcefile               >>> La rueda de la fortuna | Shelfnum : JMG-AA-0000 | Page : 12
    #'Linked in item'   >>> La rueda de la fortuna | Shelfnum : JMG-AA-0000 

    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_omkLinkItem1.csv"
    listOutputFileTmp.append(outputFileTmp)
       
    columnNameIn = 'Title'
    columnNameDup = 'Linked in item'
    appendMode = False
    separator = None
    toolCSV.duplicateColumn(inputFile, outputFileTmp, columnNameIn, columnNameDup, appendMode, separator)
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_omkLinkItem2.csv"
    listOutputFileTmp.append(outputFileTmp)
    
    columnNameIn = 'Source'
    columnNameDup = 'Linked in item'
    appendMode = True
    separator = ' | Shelfnum : '
    toolCSV.duplicateColumn(inputFile, outputFileTmp, columnNameIn, columnNameDup, appendMode, separator)   
    
    #'Title'   >>> La rueda de la fortuna | Shelfnum : JMG-AA-0000 | Page : 12
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_NewTitle2.csv"
    listOutputFileTmp.append(outputFileTmp)
    
    columnNameIn = 'Source'
    columnNameDup = 'Title'
    appendMode = True
    separator = ' | Shelfnum : '
    toolCSV.duplicateColumn(inputFile, outputFileTmp, columnNameIn, columnNameDup, appendMode, separator)   
    
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_NewTitle3.csv"
    listOutputFileTmp.append(outputFileTmp)
    
    columnNameIn = 'Page'
    columnNameDup = 'Title'
    appendMode = True
    separator = ' | Page : '
    toolCSV.duplicateColumn(inputFile, outputFileTmp, columnNameIn, columnNameDup, appendMode, separator)   
        
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_NewTitle4.csv"
    listOutputFileTmp.append(outputFileTmp)
    
    columnNameTest = 'dataFormat'
    columnNameOut = 'Title'
    contentValue = 'JPG'
    suffixValueTrue = ' | Content : facsimile'
    suffixValueFalse = ''
    
    toolCSV.addSuffixValueConditional(inputFile, outputFileTmp, columnNameTest, columnNameOut, contentValue, suffixValueTrue, suffixValueFalse)

    #changement de path dans la column file
    inputFile = outputFileTmp
    outputFileTmp = pathDirOut+"Molina_LocalPath.csv"
    listOutputFileTmp.append(outputFileTmp)
    columnNameTest = 'file'
    valueTest = 'http://eman-archives.org/hispanique/files/original/'
    valueReplace = 'C:/Users/Public/Documents/MSHS/workflow/Molina/02-numerisation/compress-Jpg/'
    
    toolCSV.replaceValueWithOther(inputFile, outputFileTmp, columnNameTest, valueTest, valueReplace)
    
    
    copyfile(outputFileTmp, pathDataFileTransformed)
    
    
def renameMolinaFile(inputCsvFile, outputCsvFile):
    """
    change les nom de fichier generés par omeka en nom de fichier intelligible
    """

    
    countFileFind = 0
    
    writerOut = None
    outFile = None
    with open(inputCsvFile, encoding='utf-8', newline="\n") as dataFile:
        reader = csv.DictReader(dataFile, delimiter=';')
        countLine = 2 #on commence a 2 pour etre cohérent avec les lignes du tableau de donnée quand on l'ouvre sous Excell/libreOffice
        for dicDataCur in reader:
            #on gere l'ouverture et l'ecriture de la permiere ligne du fichier de sortie
            #---------------------------
            if countLine== 2 :
                outFile = open(outputCsvFile, 'w', encoding='utf-8', newline="\n") 
                writerOut = csv.DictWriter(outFile, delimiter=';', fieldnames = reader.fieldnames)
                writerOut.writeheader()
                
            valueCur = dicDataCur['file']

            if not(valueCur==None) and not(valueCur=='') and not(valueCur.lower()=='none'):
                #on creer le nouveau nom 

                newNameFile = dicDataCur['Source']
                
                if dicDataCur['Page'] == None or dicDataCur['Page']=='':
                    pass
                else:
                    newNameFile = newNameFile+"_"+"{0:03}".format(int(dicDataCur['Page']))
                
                (head, tail) = os.path.split(valueCur)
                leFileNameCur = os.path.basename(tail) 
                
                (leFileNameCurSansExtension,extension) = os.path.splitext(leFileNameCur)
                
                #print(leFileNameCurSansExtension)
                dicDataCur['file'] = head+'/'+newNameFile+extension
                
                #si le fichier existe!
                if os.path.isfile(valueCur):
                    countFileFind+=1
                                       
                    try:
                            pathFileCur = valueCur
                            os.rename(pathFileCur, dicDataCur['file'])
                            
                    except:
                        print('pas pu renommer', pathFileCur)
                    
                else:
                    #print('pas trouve',valueCur )
                    pass  
                                
            else:
                pass
            
            writerOut.writerow(dicDataCur)
            countLine+=1
            
            
    outFile.close()    
    print('nb fichiers trouvées a renommer', str(countFileFind))
    

def suffixPageNumber(inputFile, outputFile):
    #maintenant qu'on a un champs Page on peut le prefixer

    dicPrefix = {}
    dicPrefix['Page'] = 'Page : '
    toolCSV.addPrefixValueFixedFromDic(inputFile, outputFile,dicPrefix)
    

def createMolinaCollections(baseUrl, keyApi):
    """
    fonction permettant de créer une liste de collection sur un site omeka distant via la REST API
    
    on ne veut pas recreer une collecion si elle existe deja sur le site omeka cible

    """
    
    #on commence par obtenir la liste des collections omeka existantes
    dicCollectionId = omkCon.getDicCollectionId(baseUrl)
    
    
    #après ue extraction de la liste des collections identifiée
    #on les créer a distance
    listCollection = []
    
    listCollection.append("Carnet / Cahier") # << 'Carnet / Cahier'
    listCollection.append("Correspondance")  # << 'Correspondance'
    listCollection.append("Presse (Articles rédigés par l’auteur)")  # << 'Presse (Article rédigé par l’auteur)'
    listCollection.append("Récit")  # << 'Récit'
    listCollection.append("Essai")  # << 'Essai'
    listCollection.append("Poésie")  # << 'Poésie (Recueil)', 'Poésie (Poème)'
    listCollection.append("Théâtre") # <<  'Théâtre (Intermède)', 'Théâtre (Pièce)', 'Mise en scène'
    #listCollection.append("Cours")  # << ...?
    listCollection.append("Radio (Script radiophonique)")  # << 'Radio (Script radiophonique)'
    #listCollection.append("Document politique") # << ..?
    listCollection.append("Documentation - Presse") # <<  'Documentation - Presse'
    listCollection.append("Documentation - Autres types de documents") # <<  'Documentation - Autre type de document'
    listCollection.append("Dossier biographique - Iconographie")  # << 'Dossier biographique - Iconographie'
    listCollection.append("Dossier biographique - Agenda")  # << 'Dossier biographique - Agenda'
    listCollection.append("Dossier biographique - Document officiel")  # << 'Dossier biographique - Document officiel'
    listCollection.append("Dossier biographique - Autres types de documents") # <<  'Dossier biographique - Autre type de document'
    listCollection.append("Réception de l’oeuvre")  # << 'Réception de l’œuvre - Plan de classement et inventaire', 'Réception de l’œuvre - Travail de valorisation', 'Réception de l’œuvre - Réception'
    
    
    #avec extration viatoolsForCSV.getDistinctValueInColumn_test()
    #tmpOldListeType  = ['Théâtre (Intermède)', 'Théâtre (Pièce)', 'Poésie (Recueil)', 'Poésie (Poème)', 'Récit', 'Documentation - Presse', 'Presse (Article rédigé par l’auteur)', 'Essai', 'Radio (Script radiophonique)', 'Carnet / Cahier', 'Mise en scène', 'Correspondance', 'Documentation - Autre type de document', 'Dossier biographique - Autre type de document', 'Dossier biographique - Agenda', 'Dossier biographique - Document officiel', 'Dossier biographique - Iconographie', 'none', 'Réception de l’œuvre - Plan de classement et inventaire', 'Réception de l’œuvre - Travail de valorisation', 'Réception de l’œuvre - Réception', '']

    dicIdOmeka = omkCon.getDicoDctermIdOmeka(baseUrl)
     
    dicMeta = {}  
    for nameCollection in reversed(listCollection):
        #si la collection n'existe pas a distance on la creer
        if not nameCollection in dicCollectionId:
            dicMeta["dcterms:title"] = nameCollection
            try:
                omkCon.createCollection(baseUrl,keyApi, dicMeta, dicIdOmeka)
            except Exception as e:
                print(e)

   
def correctionFileUrl(inputFile,pathOut,filenameOut):
    #il y a des  file du genre
    #http: //eman-archives. org/hispanique/files/original/dceb0a3ff7051393d151a15d2e97bdaf. | jpg |
    #donc des espaces en trop et des | dans le nom d'extension...

    columnNameTest = 'file'
    valueTest = '. | jpg'
    valueReplace = '.jpg'
    pathdatafileTmp = pathOut+'MolinaTmp1.csv'
    toolCSV.replaceValueWithOther(inputFile, pathdatafileTmp, columnNameTest, valueTest, valueReplace)
    
    columnNameTest = 'file'
    valueTest = ' '
    valueReplace = ''
    pathdatafileTmp2 = pathOut+'MolinaTmp2.csv'
    toolCSV.replaceValueWithOther(pathdatafileTmp, pathdatafileTmp2, columnNameTest, valueTest, valueReplace)
    
    columnNameTest = 'file'
    valueTest = '|'
    valueReplace = ' | '
    pathdatafileTmp3 = pathOut+filenameOut
    toolCSV.replaceValueWithOther(pathdatafileTmp2, pathdatafileTmp3, columnNameTest, valueTest, valueReplace)
    
    
def main(argv):
    baseUrl = "https://molina.nakalona.fr"
    keyApi = "XXXXX8185486099461dce81a26927f7594914937"

    
    #--------------------------------------------------------
    #createMolinaCollections(baseUrl, keyApi)
    #--------------------------------------------------------
    
    
    #---------------------------------------------
    #gestion des transformations du fichier input
    pathDataFile = "C:/Users/Public/Documents/MSHS/workflow/Molina/03-metadatas/"
    
    pathOutFiles = "C:/Users/Public/Documents/MSHS/workflow/Molina/03-metadatas/omeka/"
    #remplacer manuellement sur le xlsx dans la colone file . | par
    #fileBrut = pathDataFile+"Molina-revise.csv"
    fileBrut = pathDataFile+"Molina-AcRevisionGenetic.csv"
    
    dataReadyForPushFilename = "Molina_omkReadyPush.csv"

    pathDataFileReadyForPush = pathOutFiles+dataReadyForPushFilename
    
    """
    fileCorrectionPath =  "Molina_reviseCorrFile.csv"
    correctionFileUrl(fileBrut, pathOutFiles,fileCorrectionPath)
        
    dataV1 = "Molina_omkReadyP1.csv"
    pathDataV1 = pathOutFiles+dataV1
    transformDataFileForMolinaOmekaPush(pathOutFiles+fileCorrectionPath, pathOutFiles, pathDataV1)
    
    dataV2 = "Molina_omkReadyP2.csv"
    pathDataV2 = pathOutFiles+dataV2
    renameMolinaFile(pathDataV1, pathDataV2)
    
    suffixPageNumber(pathDataV2,pathDataFileReadyForPush)
    """
    
    #Attention j'ai fait des modifications manuelles sur le fichichier readypush en utilisant readyforpushtmp
    #pour ajouter les chemins fichiers audios 
    #et corriger les type et format
    
    #--------------------------------------------
    
    objConfigOmkApi = omkCon.objConfigOmekaRestApi(baseUrl, keyApi)
    
    outFilename = "Molina_OmkIded.csv"
    pathOutFileIded = pathOutFiles+outFilename
    
    pathMappingFile = "C:/Users/Public/Documents/MSHS/workflow/Molina/03-metadatas/omeka/"
    mappingFilename = "mappingOmk.csv"
    pathMappingFile = pathMappingFile+mappingFilename
    
    dicCollectionId = omkCon.getDicCollectionId(baseUrl)
    
    listColumnRejectedForItem = ["Title","dataFormat","dataType","file"]

    listColumnRejectedForRessource = ["Auteur analyse","Auteur description","Auteur révision","Auteur transcription",	"Contexte géographique","Coverage",	"Creator","Date","Description","Destinataire","Directeur de la publication","Etat général","Etat génétique","Format","Language","Lieu d'expédition","Localisation","Nature du document",	"Notes","Numéro de la publication","Publication","Publisher","Périodicité","Collection","Relations Génétiques","Autres ressources en relations","Représentation","Rights","Source","Sous-titre","Subject","Support","Titre de la publication","Type","Type de publication","Type document politique","Lieu de publication","file","tag","Linked in collection","Linked in item","dataType","dataFormat"]
    
    #"Auteur analyse","Auteur description","Auteur révision","Auteur transcription",	"Contexte géographique","Coverage",	"Creator","Date","Description","Destinataire","Directeur de la publication","Etat général","Etat génétique","Format","Language","Lieu d'expédition","Localisation","Nature du document",	"Notes","Numéro de la publication","Publication","Publisher","Périodicité","Collection","Relation","Représentation","Rights","Source","Sous-titre","Subject","Support","Title","Titre de la publication","Type","Type de publication","Type document politique","Lieu de publication","file","tag","Linked in collection","Linked in item","dataType","dataFormat","Omk item","id	Omk","ressource id","Omk statut	","Page"

    updateMetas = True
    updateDatas = False
    
    dicDcTermId = omkCon.getDicoDctermIdOmeka(baseUrl)

    
    omkPusher.metadataFileCSV2OmekaPush(objConfigOmkApi, pathDataFileReadyForPush, pathMappingFile, pathOutFileIded, dicCollectionId, dicDcTermId, listColumnRejectedForItem, listColumnRejectedForRessource, updateMetas, updateDatas)
    




if __name__ == "__main__":
    main(sys.argv) 
