# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:04:01 2017

@author: Michael Nauge
"""
#description : script contenant plusieurs fonctions permettant de manipuler des données sur un omeka distant


import os

#pour la lecture et ecriture de fichier csv
import csv

import toolsForCSV as toolCSV

import omekaRestConnector as omkCon



        
def metadataFileCSV2OmekaPush(configOmk, pathDataFile, pathMappingFile, pathDataFileOutput, dicCollectionId, dicDcTermId, listColumnRejectedForItem, listColumnRejectedForRessource, updateMetas = True, updateDatas = False):
    """
    fonction permettant de faciliter l'envoi massif sur omeka
    cette fonction gere l'envoi et la mise a jour des donnnées
    elle peut etre interrompu a tout instant et etre relancé sans que cela necessite une quelquonque intervention
    
    elle utilise un fichier dataFile contenant les données descriptives des fichiers ressources à verser sur omeka
    elle utilise un fichier mappingFile contenant les correpondances entre les étiquettes personnalisées du chercheur présente dans le fichier dataFile et des étiquettes dublincore utilisées par nakala
    
    le fichier dataFile doit contenir des colonnes specifiques pour omeka : [dcterms:title], [Linked in collection], [Linked in item], [Omk item id], [Omk statut]
    
    certaines colonnes doivent obligatoirement avoir du contenu
      il faut détecter si le fichier de data ne contient pas de valeurs pour certaines colonnes particuliere.
        dans noter cas les datas sont obligatoires pour [dcterms:title] pour retrouver les items omeka
        
        
    pour chaque ligne de donnée
       
        on regarde si il faut créer un item en regardant le contenu de la colonne [Linked in item]
          si il y a None ou Blank il n'y a pas de d'item a gérer
          si il y a un contenu on vérifie si cet item existe sur omeka a l'aide d'une requete GET basé sur le nom present dans la [Linked in item] qui doit aller dans dcterms:title 

            si cet item existe on a récupéré son id et on peut l'écrire dans la colonne [Omk item id] (il est surement déjà écrit, mais dans le doute...)
            
            si il n'existe pas on le créer par une requete POST item
              
                s'il y a une exception ou pas de idres on ecrit dans le fichier de sortie l'erreur dans la colonne [Omk statut]
                sinon a priori l'envoi c'est bien passé on a récupéré le handle, on peut l'écrire dans la colonne [Omk item id]
    
    
    
    lorsque les datas sont sur omeka (on peut obtenir leur id) on peut donc effecteur une mise ajour des métasdatas si c'est demandé via l'attribut  : updateMetas
    
    
        
    :param pathDataFile: le chemin vers le fichier CSV contenant les metas datas a envoyer
    :type pathDataFile: str. 
    
    :param pathMappingFile: le chemin vers le fichier CSV contenant le mapping entre les champs personnalisés et leurs transpositions vers une norme (dcterms)
    :type pathMappingFile: str. 
    
    :param pathDataFileOutput: le chemin vers le fichier CSV de sorti contenant la même chose que le dataFile mais complété pour les champs  [Omk item id],[Omk statut]
    :type pathDataFileOutput: str. 

    :param dicCollectionId: un dico contenant les id omekas pour la gestion des collections. ce dictionnary devra disparaitre dans ne prochaine version, car il doit pouvoir etre creer dynamiquement par requete GET et en fonction du contenu DataFile
    :type dicCollectionId: str. 

    """
    
    #####################################################################
    #### les verifications de validité des fichiers de data et mapping
    #####################################################################
    
    #on commence par vérifier la présence des colonnes obligatoires dans le fichier de data
    listColonneACheck = ['Linked in collection', 'Linked in item','dataType','dataFormat','Omk item id', 'Omk ressource id', 'Omk statut']
    resCheckColumn = toolCSV.checkColumnExist(listColonneACheck, pathDataFile)
    
    if resCheckColumn:
        #print('le datafile contient les colonnes obligatoires')
        pass
    else:
        print('[error] : le dataFile ne contient pas toutes les colonnes obligatoires')
        print('[help] : pensez à utiliser la fonction transformDataFileForOmekaPush()')
        return False
    
    
    #on verifie ensuite la validite du fichier de mapping avec le fichier de data
    resCheckMappingWithDataFile = toolCSV.checkMappingFileWithDataFile(pathMappingFile,pathDataFile) 
    if resCheckMappingWithDataFile:
        #print('le fichier de mapping est compatible avec le fichier de data')
        pass
    else:
        print("[error] : le fichier de mapping n'est pas compatible avec le fichier de data")
        return False
    
    #on vérifie la présence de valeurs dans le fichier de mapping 
    #car pour envoyer sur nakala il faut fournir certaines métas obligatoires
    listRequireMappedValues = ['dcterms:title']
    resCheckMappingValues = toolCSV.checkMappingFileValues(pathMappingFile,listRequireMappedValues)
    if resCheckMappingValues:
        #print('le fichier de mapping contient bien les valeurs obligatoires pour nakala')
        pass
    else:
        print("[error] : le fichier de mapping ne contient pas les valeurs obligatoires pour omeka")
        return False    
        
    #on vérifie que les fichiers locaux sont tous là !
    resCheckLocalFile = toolCSV.checkPathFileInDataFile(pathDataFile, 'file')
    if not resCheckLocalFile:
        print("[error] : le fichier de data ne contient des chemin vers des fichiers locaux introuvables")
        return False  
    
    #a priori nos fichiers données et mapping peuvent etre utilisés proprement
    #--------------------------------------------
    #on récupère le dictionnaire de mapping
    dicMapping = toolCSV.getMappingDicFromFile(pathMappingFile)
    #print('dicMapping',dicMapping)
    #--------------------------------------------
    
    # TODO : Gestion entierement dynamique des collections
    #pour le moment je prefere un controle pseudo manuel à l'extérieur de la fonction
    #je creer en une fois toutes les collections dans le bonne ordre
    #car pour le moment je ne sais pas comment changer l'ordre d'affichage des collections sur l'affichage public
    #deplus je n'ai pas géré automatiquement toutes les metas que peuvent porter les collections
    listCollectionToCreate = checkCollectionRequiered(configOmk,pathDataFile)
    
    if not (len(listCollectionToCreate)==0):
        print("[error] le fichier de données contient des collections inexistantes sur le omeka cible")
        print("veuillez creer manuellement ces collections via l'interface d'admin ou par l'appel d'une fonction createCollections() utilisant l'api rest")
        print("liste des collections a creer : ",listCollectionToCreate)
        return False
    
    #on ouvre le fichier de sortie permettant de sauvegarder les handles attribué et les eventuelles erreurs d'envoi
    outFile = None
    writerOut  = None
    #on traite les lignes du fichier de données
    with open(pathDataFile,encoding='utf-8') as dataFile:
        dataFile.seek(0)
        reader = csv.DictReader(dataFile, delimiter=';')
        #on obtient un dico par ligne
        countLine = 2 #on commence a 2 pour etre cohérent avec les lignes du tableau de donnée quand on l'ouvre sous Excell/libreOffice
        
        for dicDataCur in reader:
            #une variable qui jous permet de breaker le traitement d'une ligne posant probleme
            errorFatalForThisLine = False
            
            #on gere l'ouverture et l ecriture de la permiere ligne du fichier de sortie
            #---------------------------
            if countLine== 2 :
                outFile = open(pathDataFileOutput,'w', encoding='utf-8', newline="\n") 
                writerOut = csv.DictWriter(outFile, delimiter=';', fieldnames = reader.fieldnames)
                writerOut.writeheader()
            #---------------------------
            
            ##################################################
            ##### gestion des items                      #####
            ##################################################
            idItem = None
            
            #on regarde si il faut créer un item en regardant le contenu de la colonne [Linked in collection]
            linkedInItemTitle = dicDataCur['Linked in item']

            #si il y a None ou Blank il n'y a pas d'item a gérer
            if linkedInItemTitle=='' or linkedInItemTitle == None:
                print("L",countLine,": pas d'item a gerer")
            else :
                #si il y a un contenu 
                #on devra a terme avoir un id omeka de cet item branch        
                #on vérifie si cet item existe sur omeka a avec une requete GET
                #print(linkedInItemTitle+' existe ?')
                
                try :
                    idItem = omkCon.getIdsItemFromTitle(configOmk.baseUrl,configOmk.keyApi, dicDcTermId, linkedInItemTitle)
                    dicDataCur['Omk item id'] = str(idItem)#warning, c pour du debug... normalement c'est ecrasé juste après avec un idItem[0] ...
                except Exception as e:
                    print(e)
                    errorFatalForThisLine = True 
                    dicDataCur['Omk statut'] = 'error itemExistByTitle'+str(e)
            
            if not(errorFatalForThisLine):
                if not(idItem==None) and not(len(idItem)==0):
                    print('len(idItem)',len(idItem))
                    if len(idItem)==1:
                        idItem = idItem[0]
                        print("L",countLine,'cet item '+linkedInItemTitle+ " existe. Id trouvé:  "+ idItem)
                        
                        #on a bien retrouvé l'id de cet item on le conserve dans le fileoutput
                        dicDataCur['Omk item id'] = str(idItem)
                        
                        #puisque ca existe et qu'on a demandé un update
                        if updateMetas:
                            #TODO:
                            print('on a demandé un update')
                            dicMeta = makeDicoForOmekaPOST(dicMapping, dicDataCur, listColumnRejectedForItem)
                            
                            if not(dicDataCur['Linked in collection']==None and not(dicDataCur['Linked in collection']=='') and not(dicDataCur['Linked in collection'].lower()=='none')):
                                idCollectionOmeka = dicCollectionId[dicDataCur['Linked in collection']]
                                                            
                            try :
                                omkCon.updateItem(configOmk.baseUrl,configOmk.keyApi, dicMeta, dicDcTermId, idItem, idCollectionOmeka)
                            except Exception as e:
                                print(e)
                                errorFatalForThisLine = True 
                                dicDataCur['Omk statut'] = 'error Update item '+str(e) 
                            
                    else:
                        errorFatalForThisLine = True 
                        dicDataCur['Omk statut'] = 'error itemExistByTitle many instance with same title'+str(linkedInItemTitle)+str(idItem)
                        print('error itemExistByTitle many instance with same title'+str(linkedInItemTitle))
                
                #si elle n'existe pas on fait un POST          
                else:
                    #il faut creer cet item via l'api Rest 
                    print("L",countLine,"Il faut faire un POST item ! ")
                    
                    
                    dicMeta = makeDicoForOmekaPOST(dicMapping, dicDataCur, listColumnRejectedForItem)
                    idCollectionOmeka = None
                    
                    if not(dicDataCur['Linked in collection']==None and not(dicDataCur['Linked in collection']=='') and not(dicDataCur['Linked in collection'].lower()=='none')):
                        idCollectionOmeka = dicCollectionId[dicDataCur['Linked in collection']]
                        print('idCollectionOmeka',idCollectionOmeka)
                    
                    try :
                        idItem = omkCon.createItem(configOmk.baseUrl,configOmk.keyApi, dicMeta, dicDcTermId, idCollectionOmeka)
                    except Exception as e:
                        print(e)
                        errorFatalForThisLine = True 
                        dicDataCur['Omk statut'] = 'error POST item '+str(e) 
                        
                #gestion des ressources a associer dans l'item courant
                if not(errorFatalForThisLine):
                    idRessource = None
                    
                    dicMetaRessource = makeDicoForOmekaPOST(dicMapping, dicDataCur, listColumnRejectedForRessource)
                    #normalement ici on a un iditem valide!
                    #on regarde dans le champs file si il faut envoyer une ressource
                    fileCur = dicDataCur['file']
                    if fileCur==None or fileCur=='' or fileCur.lower()=='none':
                        #pas de ressource a gerer
                        pass
                    else:
                        #on test le chemin du fichier
                        if os.path.isfile(fileCur):
                            #le chemin du fichier est valide!
                            
                            #on test l'existance de cette ressource sur omeka via une resquete GET connaissant l'id de l'item mere
                            try :
                                idRessource = omkCon.getIdRessourceFromTitle(configOmk.baseUrl,configOmk.keyApi, dicDcTermId, dicMetaRessource['dcterms:title'][0],idItem)
                                
                            except Exception as e:
                                print(e)
                                errorFatalForThisLine = True 
                                dicDataCur['Omk statut'] = 'error RessourceExistByTitle'+str(e)

                            if not(errorFatalForThisLine):        
                                #si on a pa trouvé il faut le creer!
                                if (idRessource==None) or len(idRessource)==0 :
                                    try :
                                        idRessource =  omkCon.addRessourceToItem(configOmk.baseUrl,configOmk.keyApi, fileCur, dicMetaRessource, dicDcTermId, idItem)
                                        
                                    except Exception as e:
                                        print(e)
                                        errorFatalForThisLine = True 
                                        dicDataCur['Omk statut'] = 'error POST ressource '+str(e) 
                                        
                                #si la resssource existe deja 
                                elif len(idRessource)==1:
                                    #on le sauvegarde dans le fichier output
                                    dicDataCur['Omk ressource id'] = str(idRessource[0])
                                    #on gere l'update si besoin
                                    if(updateMetas):
                                        try :
                                            omkCon.updateRessource(configOmk.baseUrl,configOmk.keyApi, dicMetaRessource, dicDcTermId, idRessource[0])
                                            
                                        except Exception as e:
                                            print(e)
                                            errorFatalForThisLine = True 
                                            dicDataCur['Omk statut'] = 'error Update ressource '+str(e) 
                                    
                                else:
                                    pass
                                
                        else:
                            errorFatalForThisLine = True 
                            dicDataCur['Omk statut'] = 'error filepath'
                            print('error filepath ', fileCur)
                        
            #on ecrit dans le fichier de sortie
            writerOut.writerow(dicDataCur)
            outFile.flush() 
            
            print('----')
            countLine += 1
            
    outFile.close() 
    
    
def makeDicoForOmekaPOST(dicMapping, dicDataCur, listColumnRejectedCur, listColumnRejectedSplit=['dcterms:title']):
    """
    fonction facilitant la creation du dictionnary utile pour les fonctions de POST et  PUSH
        
    :param dicMapping: le dico contenant le mapping entre les champs personnalisé et les champs normalisés dcterms dans notre cas
    :type dicMapping: dictionary
    
    :param dicDataCur: le dico contenant les données
    :type dicDataCur: dictionary
    
    :param listColumnRejectedCur: liste contenant les champs a rejeter car inutil pour dans ce contexte
    :type listColumnRejectedCur: list 
    
    :param listColumnRejectedSplit: liste contenant les champs pour lesquels nous ne souhaitons pas creer de nouvelles instances
    :type listColumnRejectedSplit: list 
    
    return : dictionnary contenant les metas dcterms
    """   
    dicMeta = {}
   
    #on creer deux dico
    for km in dicMapping:
        if not(dicDataCur[km] == '' or dicDataCur[km] == None):
            if not(dicDataCur[km].lower() == 'none'):
                if not(km in listColumnRejectedCur):
                    if ('dcterms' in dicMapping[km]): 
                        #test le contenu si il y a un | on split pour creer plusieurs instances
                        listValues = []
                        if not(dicMapping[km] in listColumnRejectedSplit) and  ' | ' in dicDataCur[km]:
                            listValues = dicDataCur[km].split(' | ')
                            
                            for v in listValues:
                                #test si la key existe
                                if not(dicMapping[km] in dicMeta):
                                    dicMeta[dicMapping[km]]=[v]
                                else:
                                    dicMeta[dicMapping[km]].append(v)
                        else:
                            v = dicDataCur[km]
                            if not(dicMapping[km] in dicMeta):
                                    dicMeta[dicMapping[km]]=[v]
                            else:
                                dicMeta[dicMapping[km]].append(v) 
                    else:
                        #normalement il n'y a pas d'autre type de meta
                        pass
            else:
                #print('on rejette la colonne',dicMapping[km])
                pass
                
    return dicMeta            
            
def checkCollectionRequiered(configOmk, pathDataFile):
    """
    
    :param configOmk: un objet contenant les variables necessaire a la communication avec l'api omeka (url, keyApi)
    :type configOmk: obj configOmk
        
    :param pathDataFile: le chemin vers le fichier de données contenant toutes les collections attendu dans le champs 'Linked in collection'
    :type pathDataFile: str
    """
    
    #on parcours une premiere fois le fichier de données pour connaitre toutes les collections attendus
    listExpectedCollections = toolCSV.getDistinctValueInColumn(pathDataFile, 'Linked in collection')
    #on fait une requete get sur le site omeka pour obtenir la liste des collections existantes
    listExistingOmekaCollection = omkCon.getDicCollectionId(configOmk.baseUrl)
    
    listCollectionToCreate = []
    for v in listExpectedCollections:
        if not v in listExistingOmekaCollection:
            #print('il faut creer cette collection', v)
            listCollectionToCreate.append(v)    
            
    return listCollectionToCreate
    

def deleteItemsFromTitleInCsv(configOmk, pathDataFile, columnTitle):
    """
    fonction permettant de supprimmer de nombreux items omeka
    disposant dun fichier CSV contenant une column portant le 'title' des items omeka a supprimer
    
    :param configOmk: un objet contenant les attributs permettant l'utilisation de l'api rest sur un omeka cible
    :type configOmk: objConfigOmekaRestApi (cf omekaRestConnector)
    
    :param pathDataFile: le chemin vers le fichier CSV 
    :type pathDataFile: str. 
    
    
    :param columnTitle: le nom de la colonne contenant les titles des items à supprimer
    :type columnTitle: str. 
    
    """
    #on ouvre le pathDataFile
    
    #on cherche la column portant le nom indiqué par columnTitle
    
    #pour chaque "title"
    #on cherche l'id de l'item
    
    countitemsNotFind = 0
    with open(pathDataFile,encoding='utf-8') as dataFile:
        dataFile.seek(0)
        reader = csv.DictReader(dataFile, delimiter=';')
        #on obtient un dico par ligne
        countLine = 2 #on commence a 2 pour etre cohérent avec les lignes du tableau de donnée quand on l'ouvre sous Excell/libreOffice
        
        for dicDataCur in reader:
            
            titleCur = dicDataCur[columnTitle]
            print('titleCur', titleCur)
             
            #on cherche l'id des items par le title
            dicDctermsIdOmeka = omkCon.getDicoIdDctermOmekaHumaNum()
            idRes = omkCon.getIdsItemFromTitle(configOmk.baseUrl,configOmk.keyApi, dicDctermsIdOmeka, titleCur) 
            
            print('idRes',idRes)
            print('len(idRes)',len(idRes))
            if not(idRes==None) :
                if len(idRes)==0:
                    print('item not found len 0') 
                    countitemsNotFind+=1
                else:
                    for idcur in idRes:
                        print('idfind ',idcur)
                        
                        #maintenant quon a l'id on va envoyer une requete delete
                        omkCon.deleteItemById(configOmk.baseUrl,configOmk.keyApi, idcur)
            
            else:
                print('item not found none')
             
        countLine+=1  
        
        print('nb item not find',countitemsNotFind)
    
def main(argv):
    pass

if __name__ == "__main__":
    main(sys.argv) 



