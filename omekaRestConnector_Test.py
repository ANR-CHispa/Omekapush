# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 10:13:39 2017

@author: Michael Nauge
"""
#unit test for omekaRestConnector functions


import sys

import omekaRestConnector as omkCon

from random import choice
from string import ascii_uppercase


#baseUrl = "http://transcrire.huma-num.fr"

baseUrl = "https://guarnido.nakalona.fr"
keyApi = "XXXXX76ebdf1e1444459254eccbda91b7d8XXXXX"





def createCollection_test():
    dicMeta = {}
    dicMeta["dcterms:title"] = "Collection TMP"
    
    dicIdDctermsOmeka = omkCon.getDicoIdDctermOmekaHumaNum()
    omkCon.createCollection(baseUrl,keyApi, dicMeta, dicIdDctermsOmeka)
    
    
        
def getDicCollectionId_test():
       
    #baseUrl = 'http://localhost:1234'
    dicRes  = omkCon.getDicCollectionId(baseUrl)
    #print(dicRes)
    
    for idcollection in dicRes:
        print(idcollection,' ', dicRes[idcollection])
    
def getDicoDctermIdOmeka_test():

    dicRes  = omkCon.getDicoDctermIdOmeka(baseUrl)

    
    for idEltType in dicRes:
        print(idEltType,' ', dicRes[idEltType])
    
    print('nb find elements:', len(dicRes))
        
def createItem_test():
    
    dicMeta = {}
    dicMeta["dcterms:title"] = "title TMP"
    dicMeta["dcterms:subject"] = "subject TMP"
    dicMeta["dcterms:description"] = "description TMP"
    dicMeta["dcterms:creator"] = "Auteur description : Miguel Naugera"
    
    #dicDctermsIdOmeka = omkCon.getDicoIdDctermOmekaHumaNum()
    dicDctermsIdOmeka = omkCon.getDicoDctermIdOmeka(baseUrl)          
    idCollectionOmeka = None
    
    omkCon.createItem(baseUrl,keyApi, dicMeta, dicDctermsIdOmeka, idCollectionOmeka)


def updateItem_test():
    
    idItem = 3
    
    dicMeta = {}
    dicMeta["dcterms:title"] = "title Updated"
    dicMeta["dcterms:subject"] = "subject Updated"
    dicMeta["dcterms:description"] = "description Updated"
    
    dicDctermsIdOmeka = omkCon.getDicoIdDctermOmekaHumaNum()
                   
    idCollectionOmeka = None

    
    omkCon.updateItem(baseUrl,keyApi, dicMeta, dicDctermsIdOmeka, idItem, idCollectionOmeka)
      
    
    
def addRessourceToItem_test():
    
    idItem = 3
    pathRessource = "./JMG-DC-063.jpg"
    
    dicMeta = {}
    dicMeta["dcterms:title"] = "title ressource TMP"
    dicMeta["dcterms:subject"] = "same subject mother item"
    dicMeta["dcterms:description"] = "description of this ressource"

    
    dicDctermsIdOmeka = omkCon.getDicoIdDctermOmekaHumaNum()
    
    omkCon.addRessourceToItem(baseUrl, keyApi, pathRessource, dicMeta, dicDctermsIdOmeka, idItem)
        
    
    
def getIdItemFromTitle_test():
    #title = "Panorámica hacia atrás [C1] | Shelfnum : JMG-AD1-02-C1"
    #title = "Panorámica hacia atrás | Shelfnum : JMG-AD1-02-C1"
    title= "La seda de primavera | Shelfnum : JMG-AB3-01-C1"
    #title = "bbbbbb"
    
    
    print('search item named', title)
    dicDctermsIdOmeka = dicDctermsIdOmeka = omkCon.getDicoIdDctermOmekaHumaNum()

    idRes = omkCon.getIdsItemFromTitle(baseUrl,keyApi, dicDctermsIdOmeka, title) 
    
    print('idRes',idRes)
    print('len(idRes)',len(idRes))
    if not(idRes==None) :
        if len(idRes)==0:
            print('item not found len 0') 
        else:
            for idcur in idRes:
                print('idfind ',idcur)

    else:
        print('item not found none')
            
            
             
def getIdRessourceFromTitle_test():
    
    dicDctermsIdOmeka = dicDctermsIdOmeka = omkCon.getDicoIdDctermOmekaHumaNum()
    
    title = "title ressource TMP"
    motherItemId = 3
    idRes = omkCon.getIdRessourceFromTitle(baseUrl,keyApi, dicDctermsIdOmeka,title, motherItemId)
    print(idRes)
    

def createItemWithRessource_test():
    
    ###########################################    
    #create first Item
    ###########################################
    
    #dictionnary containing item descriptive metadata 
    dicMeta = {}
    dicMeta["dcterms:title"] = "Item title TMP_" + randomword(3)
    dicMeta["dcterms:subject"] = "Item subject TMP AA "
    dicMeta["dcterms:description"] = "Item description TMP AA"
    dicMeta["dcterms:creator"] = "Item Auteur description : Miguel Naugera"
    
    dicDctermsIdOmeka = omkCon.getDicoIdDctermOmekaHumaNum()
                   
    idCollectionOmeka = None
    
    omkCon.createItem(baseUrl,keyApi, dicMeta, dicDctermsIdOmeka, idCollectionOmeka)
    ###########################################    
    
    ###########################################    
    #get Item id
    ###########################################
    idRes = omkCon.getIdsItemFromTitle(baseUrl, keyApi, dicDctermsIdOmeka, dicMeta["dcterms:title"]) 
    if not(idRes==None) :
        for idcur in idRes:
            print('idfind ',idcur)
    else:
        print('item not found')

    for idItem in idRes:
        ###########################################
        #add first ressource  to this item
        ###########################################
        
        #path to the local ressource must be send
        pathRessource = "./JMG-AI-42_023.jpg"
        
        #dictionnary containing item descriptive metadata 
        dicMetaRessource = {}
        dicMetaRessource["dcterms:title"] = "title first ressource " + randomword(4)
        dicMetaRessource["dcterms:subject"] = "same subject than mother's item"
        dicMetaRessource["dcterms:description"] = "description of this ressource"
    
        omkCon.addRessourceToItem(baseUrl, keyApi, pathRessource, dicMetaRessource, dicDctermsIdOmeka, idItem)
            
        motherItemId = idItem
        idRessourceRes = omkCon.getIdRessourceFromTitle(baseUrl, keyApi, dicDctermsIdOmeka, dicMetaRessource["dcterms:title"],motherItemId) 
        if not(idRessourceRes==None) :
            for idcur in idRessourceRes:
                print('id first Ressourcefind ',idcur)
        else:
            print('first ressource not found')
            
        ###########################################
        #add second ressource  to this item
        ###########################################    
        #path to the local ressource must be send
        pathRessource = "./JMG-AI-42_039.jpg"
        
        #dictionnary containing item descriptive metadata 
        dicMetaRessource = {}
        dicMetaRessource["dcterms:title"] = "title second ressource " + randomword(4)
        dicMetaRessource["dcterms:subject"] = "same subject than mother's item"
        dicMetaRessource["dcterms:description"] = "description of this ressource"
    
        omkCon.addRessourceToItem(baseUrl, keyApi, pathRessource, dicMetaRessource, dicDctermsIdOmeka, idItem)
            
        motherItemId = idItem
        idRessourceRes = omkCon.getIdRessourceFromTitle(baseUrl, keyApi, dicDctermsIdOmeka, dicMetaRessource["dcterms:title"],motherItemId) 
        if not(idRessourceRes==None) :
            for idcur in idRessourceRes:
                print('id second Ressourcefind ',idcur)
        else:
            print('second ressource not found')
            
        print('---------------------------------')
        print('show the online item at : ')
        urlResultat = baseUrl+'/items/show/'+str(motherItemId)
        print(urlResultat)
        print('---------------------------------')
        
    ###########################################    
    #create second Item
    ###########################################
    
    #dictionnary containing item descriptive metadata 
    dicMeta = {}
    dicMeta["dcterms:title"] = "Item title TMP_" + randomword(3)
    dicMeta["dcterms:subject"] = "Item subject BBB"
    dicMeta["dcterms:description"] = "Item description TMP BBB"
    dicMeta["dcterms:creator"] = "Item Auteur description : Michael Nauge"
    
    dicDctermsIdOmeka = omkCon.getDicoIdDctermOmekaHumaNum()
                   
    idCollectionOmeka = None
    
    omkCon.createItem(baseUrl,keyApi, dicMeta, dicDctermsIdOmeka, idCollectionOmeka)
    ###########################################    
    
    ###########################################    
    #get Item id
    ###########################################
    idRes = omkCon.getIdsItemFromTitle(baseUrl, keyApi, dicDctermsIdOmeka, dicMeta["dcterms:title"]) 
    if not(idRes==None) :
        for idcur in idRes:
            print('idfind ',idcur)
    else:
        print('item not found')

    for idItem in idRes:
        ###########################################
        #add first ressource  to this item
        ###########################################
        
        #path to the local ressource must be send
        pathRessource = "./JMG-DC-063.jpg"
        
        #dictionnary containing item descriptive metadata 
        dicMetaRessource = {}
        dicMetaRessource["dcterms:title"] = "title first ressource TMP_" + randomword(4)
        dicMetaRessource["dcterms:subject"] = "same subject than mother's item"
        dicMetaRessource["dcterms:description"] = "description of this ressource"
    
        omkCon.addRessourceToItem(baseUrl, keyApi, pathRessource, dicMetaRessource, dicDctermsIdOmeka, idItem)
            
        motherItemId = idItem
        idRessourceRes = omkCon.getIdRessourceFromTitle(baseUrl, keyApi, dicDctermsIdOmeka, dicMetaRessource["dcterms:title"],motherItemId) 
        if not(idRessourceRes==None) :
            for idcur in idRessourceRes:
                print('id first Ressourcefind ',idcur)
        else:
            print('first ressource not found')    
            
                        
        print('---------------------------------')
        print('show the online item at : ')
        urlResultat = baseUrl+'/items/show/'+str(motherItemId)
        print(urlResultat)
        print('---------------------------------')
        
        
def updateItemWithRessources_test():
    linkedInItemTitle = 'Item title TMP_YXU'
    title = 'title first ressource TMP_YGKV'
    
    #find item by linkedInItemTitle
    idItem = omkCon.getIdsItemFromTitle(baseUrl,keyApi, omkCon.getDicoIdDctermOmekaHumaNum(), linkedInItemTitle)
    print('idItem',idItem[0])
    idRessource = omkCon.getIdRessourceFromTitle(baseUrl, keyApi, omkCon.getDicoIdDctermOmekaHumaNum(), title, idItem[0]) 
    #find ressource by title
    print('idRessource',idRessource[0])
    
    #update item

    dicMeta = {}
    dicMeta["dcterms:title"] = linkedInItemTitle
    dicMeta["dcterms:subject"] = "subject Updated"
    dicMeta["dcterms:description"] = "description Updated"
                       
    idCollectionOmeka = None
    
    omkCon.updateItem(baseUrl,keyApi, dicMeta, omkCon.getDicoIdDctermOmekaHumaNum(), int(idItem[0]), idCollectionOmeka)
    
    
    print('---------------------------------')
    print('show the online item at : ')
    urlResultat = baseUrl+'/items/show/'+str(idItem[0])
    print(urlResultat)
    print('---------------------------------')
    
    #update ressources
    dicMetaRessource = {}
    dicMetaRessource["dcterms:title"] = title
    dicMetaRessource["dcterms:subject"] = "same subject than mother's item updated"
    dicMetaRessource["dcterms:description"] = "description of this ressource updated"
    omkCon.updateRessource(baseUrl,keyApi, dicMeta, omkCon.getDicoIdDctermOmekaHumaNum(), int(idRessource[0]))
    
    
    
    
def randomword(length):
    return ''.join(choice(ascii_uppercase) for i in range(length))

def deleteItemById_test():
    idItem = 2
    
    omkCon.deleteItemById(baseUrl,keyApi, idItem)
    
 
def deleteItemByTitle_test():
    title = "ccc"
    
    print('search item named', title)
    dicDctermsIdOmeka = omkCon.getDicoIdDctermOmekaHumaNum()
    idRes = omkCon.getIdsItemFromTitle(baseUrl,keyApi, dicDctermsIdOmeka, title) 
    
    print('idRes',idRes)
    print('len(idRes)',len(idRes))
    if not(idRes==None) :
        if len(idRes)==0:
            print('item not found len 0') 
        else:
            for idcur in idRes:
                print('idfind ',idcur)
                
                #maintenant quon a l'id on va envoyer une requete delete
                omkCon.deleteItemById(baseUrl,keyApi, idcur)

    else:
        print('item not found none')
        
    
        
def main(argv):
    #createCollection_test()
    
    #createItem_test()
    #getIdItemFromTitle_test()
    
    #updateItem_test()
    #addRessourceToItem_test()
    #getIdRessourceFromTitle_test()
    
    #createItemWithRessource_test()
    
    #updateItemWithRessources_test()
    
    #getDicCollectionId_test()
    #getDicoDctermIdOmeka_test()
    
    #getIdItemFromTitle_test()
    
    #deleteItemById_test()
    
    #deleteItemByTitle_test()
    
    getDicoDctermIdOmeka_test()
    
    pass

if __name__ == "__main__":
    main(sys.argv) 





