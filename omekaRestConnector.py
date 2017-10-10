# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 09:10:29 2017

@author: Michael Nauge
"""

#description : Script permettant de réaliser les operations de bases sur omeka via l'api REST
#cretion de collection, creation d'item, creation d'une ressource, mise a jour metadata
#requete get, etc

import pycurl
import certifi
import json

#lib pour les requetes GET 
import urllib.request

#lib pour le parsing de xml ou html
from bs4 import BeautifulSoup


try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
    
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode
    
from math import ceil
    

class objConfigOmekaRestApi:
    """ class contenant les parametres pour la rest api 
    cela permet uniquemet de réduire artificiellement le nombre de parametre a passer aux fonctions
    """
    
    baseUrl=''
    keyApi=''

    def __init__(self, baseUrl, keyApi):
        self.baseUrl=baseUrl
        self.keyApi=keyApi
        

#pour manipuler les metadonnées omeka il faut connaitre leurs id    
def getDicoIdDctermOmekaHumaNum():
    #dans le cas des omeka d'humanum
    #warning : cette liste est partiel!
    #je prefererai obtenir cette liste de champs et id associés par requete ....
    #voilà c'est fait !! par la fonction getDicoDctermIdOmeka(baseUrl)
    dicoDctermsToId = {}
    dicoDctermsToId["dcterms:title"] = 50
    dicoDctermsToId["dcterms:subject"] = 49
    dicoDctermsToId["dcterms:description"] = 41
    dicoDctermsToId["dcterms:creator"] = 39
    dicoDctermsToId["dcterms:source"] = 48
    dicoDctermsToId["dcterms:publisher"] = 45
    dicoDctermsToId["dcterms:date"] = 40
    dicoDctermsToId["Contributor"] = 37
    dicoDctermsToId["dcterms:rights"] = 47
    dicoDctermsToId["dcterms:relation"] = 46
    dicoDctermsToId["dcterms:format"] = 42
    dicoDctermsToId["dcterms:language"] = 44 
    dicoDctermsToId["dcterms:type"] = 51
    dicoDctermsToId["Identifier"] = 43
    dicoDctermsToId["dcterms:coverage"] = 38
    dicoDctermsToId["dcterms:alternative"] = 52
    dicoDctermsToId["dcterms:abstract"] = 53
    dicoDctermsToId["Table Of Contents"] = 54
    dicoDctermsToId["Date Available"] = 55
    dicoDctermsToId["dcterms:created"] = 56
                   
    return dicoDctermsToId


def getDicoDctermIdOmeka(baseUrl):
    """
    pour manipuler les metadonnées omeka il faut connaitre leurs id...
    cette permet permet d'obtenir les id des dcterms !  

    :param baseUrl: chemin vers l'adresse du omeka cible
    :type baseUrl: str
    
    :return : un dictionnary de key dcterms et de veleurs l'id
    """
    #on commence par faire une requete GET sur le element_sets por connaitre
    #le id des elements de type Dublin Core
    
    myUrl = baseUrl+"/api/element_sets?"
    
    c = pycurl.Curl()
    c.setopt(c.VERBOSE, True)
    c.setopt(c.URL, myUrl)
    c.setopt(pycurl.CAINFO, certifi.where())
    buffer = BytesIO()
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    responseStr = str(buffer.getvalue().decode('utf-8'))
    
    dicJson = json.loads(responseStr)
    
    #on cherche a obtenir un dictionnary pour key l'id et pour valeurs un tuple avec le nom de chaque type 
    #de metadata ainsi que le nombre d'elements de ce type
    #afin de pouvoir ensuite obtenir la liste complete qui peut etre paginé si il y a plus de 50 valeurs
    
    dicEltType = {}
    for eltType in dicJson:
        #print('eltType id ', eltType['id'], 'named', eltType['name'], ' nb elt of this type',eltType['elements']['count'])
        dicEltType[eltType['name']] = (eltType['id'],eltType['elements']['count'])
    
    
    #maintenant on va chercher tous les ids des champs dublin core
    #en fesant plusieurs requetes utilisant la pagination
    pagination = 50
    #ceil pour l'entier supérieur
    nbPage = ceil(dicEltType['Dublin Core'][1]/pagination)
    
    #print('nb page',nbPage)
    dicEltDC = {}
    
    for pageCur in range(1,nbPage+1):
        #https://guarnido.nakalona.fr/api/elements?element_set=1&page=2&per_page=50
        myUrl = baseUrl+"/api/elements?element_set="+str(dicEltType['Dublin Core'][0])+'&page='+str(pageCur)+'&per_page='+str(pagination)
        
        print
        c = pycurl.Curl()
        c.setopt(c.VERBOSE, True)
        c.setopt(c.URL, myUrl)
        c.setopt(pycurl.CAINFO, certifi.where())
        buffer = BytesIO()
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()
        responseStr = str(buffer.getvalue().decode('utf-8'))
        
        dicJson = json.loads(responseStr)
        
        for eltCur in dicJson:
            #print('eltCur name ', eltCur['name'], ' id ', eltCur['id'])
            dicEltDC['dcterms:'+str.lower(eltCur['name'])]=eltCur['id']

    return dicEltDC
    
    
    
def getDicCollectionId(baseUrl):
    """
    fonction permettant d'obtenir un dictionnaire contenant la liste des collections existantes sur un site omeka et leurs id associées
        
    :param baseUrl: chemin vers l'adresse du omeka cible
    :type baseUrl: str
    
    :return : un dictionnary de key NameCollectionOmeka et de veleurs l'id
    """
    myUrl = baseUrl+"/api/collections?"
    
    c = pycurl.Curl()
    c.setopt(c.VERBOSE, True)
    c.setopt(c.URL, myUrl)
    c.setopt(pycurl.CAINFO, certifi.where())
    buffer = BytesIO()
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    responseStr = str(buffer.getvalue().decode('utf-8'))
    
    dicJson = json.loads(responseStr)
    
    dicRes = {}
    for collection in dicJson:
        #print('collection id ', collection['id'], 'named', collection['element_texts'][0]['text'])
        dicRes[collection['element_texts'][0]['text']] = collection['id'] 
        
    return dicRes
    
    
               

def createCollection(baseUrl,keyApi, dicMeta, dicIdDctermsOmeka):
    """
    fonction permettant de creer une collection sur un site omeka distant via l'api rest
    
    :param baseUrl: l'adresse du site web OMEKA.
    :type baseUrl: str. 
    
    :param keyApi: la key api pour les requetes REST
    :type keyApi: str. 
    

    :returns:  l'id attribué
    :raises: pycurl error
    """
    
    myUrl = baseUrl+"/api/collections?key="+keyApi
    
    c = pycurl.Curl()
    c.setopt(c.VERBOSE, True)
    
    buffer = BytesIO()
    
    #myUrl = 'http://localhost:1234'
    #lancer netcat nc - l -p 1234
    c.setopt(c.URL, myUrl)
    
    
    dataDic={}
    dataDic["public"]  = True
    dataDic["featured"] = False
           
    dataDic["element_texts"] = []
    
    for kdicMeta in dicMeta:
        dataDic["element_texts"].append({"html": False,"text": dicMeta[kdicMeta] ,"element": {"id": dicIdDctermsOmeka[kdicMeta]}})

    
    uploadmeta = json.dumps(dataDic)

    c.setopt(pycurl.POSTFIELDS, uploadmeta)
    
    c.setopt(pycurl.CAINFO, certifi.where())
    
    c.setopt(c.WRITEDATA, buffer)
    
    c.perform()
        
    responseStr = str(buffer.getvalue().decode('utf-8'))

    
    dicJson = json.loads(responseStr)
    
    #for k in dicJson:
    #    print('k :',k, dicJson[k])
    
    # HTTP response code, e.g. 200.
    print('Create Collection Status: %d' % c.getinfo(c.RESPONSE_CODE))

    c.close()    
    
    return dicJson["id"]

    
    

    

    
  
    
def createItem(baseUrl,keyApi, dicMeta, dicDctermsIdOmeka, idCollectionOmeka=None):
    """
    fonction permettant de creer un item sur un site omeka distant via l'api rest
    
    :param baseUrl: l'adresse du site web OMEKA.
    :type baseUrl: str. 
    
    :param keyApi: la key api pour les requetes REST
    :type keyApi: str. 
    
    :param dicMeta: le dico contenant les métas données descriptive de l'item
    :type dicMeta: str. 
       
    :param dicDctermsIdOmeka: le dictionnary contenant les id omeka des champs de métas dublincore
    :type dicDctermsIdOmeka: str. 
    
    :param idCollectionOmeka: le numero d'id d'une collection omeka deja existante
    :type idCollectionOmeka: int    
    

    :returns:  l'id attribué
    :raises: pycurl error
    """
    
    resId = None
    
    c = pycurl.Curl()
    c.setopt(c.VERBOSE, True)
    
    buffer = BytesIO()
    
    myUrl = baseUrl+"/api/items?key="+keyApi
    #myUrl = 'http://localhost:1234'
    #lancer netcat nc - l -p 1234
    c.setopt(c.URL, myUrl)
    
    #dataDic["tags"] = [{"name": "TTT"},{"name": "AAA"},{"name": "GGG"}]
    #dataDic["element_texts"] = []
    #dataDic["element_texts"].append({"html": False,"text": "sssssuubbbjjjecctttt","element": {"id": 49}})
    
    dataDic = {}
    dataDic["public"]  = True
    dataDic["featured"] = False
           
    if not(idCollectionOmeka==None):
        dataDic["collection"] = {"id": idCollectionOmeka}
           
    dataDic["element_texts"] = []
    
    for kdicMeta in dicMeta:
        #on teste le type de contenu pour etre caapble de traiter a la fois des listes et des valeurs simples
        if type(dicMeta[kdicMeta])==type([]):
            for vcur in dicMeta[kdicMeta]:
                dataDic["element_texts"].append({"html": False,"text": vcur ,"element": {"id": dicDctermsIdOmeka[kdicMeta]}})
                
        elif type(dicMeta[kdicMeta])==type(""):
            dataDic["element_texts"].append({"html": False,"text": dicMeta[kdicMeta] ,"element": {"id": dicDctermsIdOmeka[kdicMeta]}})
        else:
            pass

    uploadmeta = json.dumps(dataDic)
    
    c.setopt(pycurl.CAINFO, certifi.where())
    
    c.setopt(c.WRITEDATA, buffer)

    c.setopt(pycurl.POSTFIELDS, uploadmeta)

    c.perform()
        
    responseStr = str(buffer.getvalue().decode('utf-8'))

    dicJson = json.loads(responseStr)
    #for k in dicJson:
    #    print('k :',k, dicJson[k])
    
    # HTTP response code, e.g. 200.
    print('Status item create: %d' % c.getinfo(c.RESPONSE_CODE))

    c.close()  
    
    resId = dicJson["id"]
    return resId



def deleteItemById(baseUrl,keyApi, idItem):
    """
    fonction permettant de supprimer un item connaissant son Id
        
    :param baseUrl: l'adresse du site web OMEKA.
    :type baseUrl: str. 
    
    :param keyApi: la key api pour les requetes REST
    :type keyApi: str. 
    
    :param dicMeta: le dico contenant les métas données descriptive de l'item
    :type dicMeta: str. 
       
    :param dicDctermsIdOmeka: le dictionnary contenant les id omeka des champs de métas dublincore
    :type dicDctermsIdOmeka: str. 
    
    :param idItem: le numero d'id de l'item a modifier
    :type idItem: int
    """
    
    c = pycurl.Curl()
    c.setopt(c.VERBOSE, True)

    
    myUrl = baseUrl+"/api/items/"+str(idItem)+"/?key="+keyApi

    c.setopt(c.URL, myUrl)
            
    c.setopt(pycurl.CAINFO, certifi.where())


    c.setopt(pycurl.CUSTOMREQUEST, "DELETE")

    c.perform()

    print('Status item delete: %d' % c.getinfo(c.RESPONSE_CODE))

    c.close()  
    
    
    
    

def updateItem(baseUrl,keyApi, dicMeta, dicDctermsIdOmeka, idItem, idCollectionOmeka=None):
    """
    fonction permettant de mettre a jour un item sur un site omeka distant via l'api rest
    
    :param baseUrl: l'adresse du site web OMEKA.
    :type baseUrl: str. 
    
    :param keyApi: la key api pour les requetes REST
    :type keyApi: str. 
    
    :param dicMeta: le dico contenant les métas données descriptive de l'item
    :type dicMeta: str. 
       
    :param dicDctermsIdOmeka: le dictionnary contenant les id omeka des champs de métas dublincore
    :type dicDctermsIdOmeka: str. 
    
    
    :param idItem: le numero d'id de l'item a modifier
    :type idItem: int
    
    :param idCollectionOmeka: le numero d'id d'une collection omeka deja existante
    :type idCollectionOmeka: int    
    

    :returns:  l'id attribué
    :raises: pycurl error
    """
    
    resId = None
    
    c = pycurl.Curl()
    c.setopt(c.VERBOSE, True)
    
    buffer = BytesIO()
    
    myUrl = baseUrl+"/api/items/"+str(idItem)+"/?key="+keyApi

    c.setopt(c.URL, myUrl)
        
    dataDic = {}
    dataDic["public"]  = True
    dataDic["featured"] = False
           
    if not(idCollectionOmeka==None):
        dataDic["collection"] = {"id": idCollectionOmeka}
           
    dataDic["element_texts"] = []
    
    for kdicMeta in dicMeta:
        #on teste le type de contenu pour etre capble de traiter a la fois des listes et des valeurs simples
        if type(dicMeta[kdicMeta])==type([]):
            for vcur in dicMeta[kdicMeta]:
                dataDic["element_texts"].append({"html": False,"text": vcur ,"element": {"id": dicDctermsIdOmeka[kdicMeta]}})
                
        elif type(dicMeta[kdicMeta])==type(""):
            dataDic["element_texts"].append({"html": False,"text": dicMeta[kdicMeta] ,"element": {"id": dicDctermsIdOmeka[kdicMeta]}})
        else:
            pass
    uploadmeta = json.dumps(dataDic)
    
    c.setopt(pycurl.CAINFO, certifi.where())
    
    c.setopt(c.WRITEDATA, buffer)

    c.setopt(pycurl.POSTFIELDS, uploadmeta)
    c.setopt(pycurl.CUSTOMREQUEST, "PUT")

    c.perform()
        
    responseStr = str(buffer.getvalue().decode('utf-8'))

    dicJson = json.loads(responseStr)

    print('Status item update: %d' % c.getinfo(c.RESPONSE_CODE))

    c.close()  
    
    resId = dicJson["id"]
    return resId


def updateRessource(baseUrl,keyApi, dicMeta, dicDctermsIdOmeka, idRessource):
    """
    fonction permettant de mettre a jour les metas d'une ressource sur un site omeka distant via l'api rest
    
    :param baseUrl: l'adresse du site web OMEKA.
    :type baseUrl: str. 
    
    :param keyApi: la key api pour les requetes REST
    :type keyApi: str. 
    
    :param dicMeta: le dico contenant les métas données descriptive de l'item
    :type dicMeta: str. 
       
    :param dicDctermsIdOmeka: le dictionnary contenant les id omeka des champs de métas dublincore
    :type dicDctermsIdOmeka: str. 
    
    
    :param idRessource: le numero d'id de l'item a modifier
    :type idRessource: int
    
    :returns:  l'id de la ressource modifié
    :raises: pycurl error
    """
    
    resId = None
    
    c = pycurl.Curl()
    c.setopt(c.VERBOSE, True)
    
    buffer = BytesIO()
    
    myUrl = baseUrl+"/api/files/"+str(idRessource)+"/?key="+keyApi

    c.setopt(c.URL, myUrl)
        
    dataDic = {}
    dataDic["public"]  = True
    dataDic["featured"] = False
           
    dataDic["element_texts"] = []
    
    for kdicMeta in dicMeta:
        #on teste le type de contenu pour etre capble de traiter a la fois des listes et des valeurs simples
        if type(dicMeta[kdicMeta])==type([]):
            for vcur in dicMeta[kdicMeta]:
                dataDic["element_texts"].append({"html": False,"text": vcur ,"element": {"id": dicDctermsIdOmeka[kdicMeta]}})
                
        elif type(dicMeta[kdicMeta])==type(""):
            dataDic["element_texts"].append({"html": False,"text": dicMeta[kdicMeta] ,"element": {"id": dicDctermsIdOmeka[kdicMeta]}})
        else:
            pass
    uploadmeta = json.dumps(dataDic)
    
    c.setopt(pycurl.CAINFO, certifi.where())
    
    c.setopt(c.WRITEDATA, buffer)

    c.setopt(pycurl.POSTFIELDS, uploadmeta)
    c.setopt(pycurl.CUSTOMREQUEST, "PUT")

    c.perform()
        
    responseStr = str(buffer.getvalue().decode('utf-8'))

    dicJson = json.loads(responseStr)

    print('Status item update: %d' % c.getinfo(c.RESPONSE_CODE))

    c.close()  
    
    resId = dicJson["id"]
    return resId



    
def addRessourceToItem(baseUrl, keyApi, pathRessource, dicMeta, dicDctermsIdOmeka, idItem):
    """
    fonction permettant d'envoyer une ressource locale a un item sur un site omeka distant via l'api rest
    
    :param baseUrl: l'adresse du site web OMEKA.
    :type baseUrl: str. 
    
    :param keyApi: la key api pour les requetes REST
    :type keyApi: str. 
        
    :param idItem: le numero d'id de l'item a modifier
    :type idItem: int
    
    :param pathRessource: le chemin vers le fichier local a envoyer
    :type pathRessource: str   
    

    :returns:  l'id attribué
    :raises: pycurl error
    """

    c = pycurl.Curl()
    c.setopt(c.VERBOSE, True)
    
    buffer = BytesIO()
    
    
    myUrl = baseUrl+"/api/files/"+"?key="+keyApi
                                         
    c.setopt(c.URL, myUrl)
    
    dataDic = {}
    dataDic["item"] = {"id":idItem}
    dataDic["public"]  = True
    dataDic["featured"] = False
                     
    dataDic["element_texts"] = []
    
    for kdicMeta in dicMeta:
        #on teste le type de contenu pour etre caapble de traiter a la fois des listes et des valeurs simples
        if type(dicMeta[kdicMeta])==type([]):
            for vcur in dicMeta[kdicMeta]:
                dataDic["element_texts"].append({"html": False,"text": vcur ,"element": {"id": dicDctermsIdOmeka[kdicMeta]}})
                
        elif type(dicMeta[kdicMeta])==type(""):
            dataDic["element_texts"].append({"html": False,"text": dicMeta[kdicMeta] ,"element": {"id": dicDctermsIdOmeka[kdicMeta]}})
        else:
            pass
        
    uploadmeta = json.dumps(dataDic)
    
    filename = pathRessource
    
    c.setopt(pycurl.HTTPPOST, [('data', uploadmeta),('file', (pycurl.FORM_FILE,filename))])
    
    c.setopt(pycurl.CAINFO, certifi.where())
    
    c.setopt(c.WRITEDATA, buffer)
    
    c.setopt(pycurl.CUSTOMREQUEST, "POST")
    
    c.perform()
        
    # HTTP response code, e.g. 200.
    print('Status post ressource: %d' % c.getinfo(c.RESPONSE_CODE))

    c.close()



    
    
def getIdsItemFromTitle(baseUrl,keyApi, dicDctermsIdOmeka, title):
    """
    fonction permettant d'obtenir l'id d'un item via une requete get en utilisnt son title pour la retrouver
    on est censé en trouvé qu'un seul mais ce n'est pas garanti il y a pu avoir un doublon..
    donc on renvoi une liste
    
    :param baseUrl: l'adresse du site web OMEKA cible.
    :type baseUrl: str. 
    
    :param keyApi: la key api pour les requetes REST
    :type keyApi: str. 
        
    :param dicDctermsIdOmeka: le dictionnary contenant les id omeka des champs de métas dublincore
    :type dicDctermsIdOmeka: str. 
    
    :param title: le titre de l'item a chercher
    :type title: str. 
    

    :returns:  l'id attribué
    :raises: urlib error, dictionnary error
    """
    
    idRes = []
    
    #URL=https://guarnido.nakalona.fr/items/browse?search=&advanced%5B0%5D%5Belement_id%5D=50&advanced%5B0%5D%5Btype%5D=is+exactly&advanced%5B0%5D%5Bterms%5D=mon+beau+ttitreee+updateddd&range=&collection=&type=&user=&tags=&public=&featured=&exhibit=&submit_search=Recherches+de+contenus
    #https://guarnido.nakalona.fr/items/browse?search=&advanced[0][element_id]=50&advanced[0][type]=is+exactly&advanced[0][terms]=mon+beau+ttitreee+updateddd&output=omeka-xml
    
    params = {}
    params['advanced[0][terms]']= title
                                                   
    url = baseUrl+'/items/browse?search=&advanced[0][element_id]=50&advanced[0][type]=is+exactly&'+urllib.parse.urlencode(params)+'&output=omeka-xml'
    #print('url encoded',url)
    
    with urllib.request.urlopen(url) as x:
        
        html = x.read()

        soup = BeautifulSoup(html,'html.parser')

        if not(soup==None):
           
            listitem = soup.findAll('item')
            
            #print('nb item find ',len(listitem))
            
            for item in listitem:
                #print(" ---- item ---- ")
                #print(item['itemid']) 
                #print('item',item)
                idRes.append(item['itemid'])
                                                                         
    return idRes  
    

            
            
def getIdRessourceFromTitle(baseUrl,keyApi, dicDctermsIdOmeka, title, motherItemId):
    """
    fonction permettant d obtenir l'id d'une ressource connaissant son title et l'id de son item mere
    
    :param baseUrl: l'adresse du site web OMEKA cible.
    :type baseUrl: str

    :param keyApi:  la key api pour les requetes REST
    :type keyApi: str

    :param dicDctermsIdOmeka: le dictionnary de dcterms et idomeka associés
    :type dicDctermsIdOmeka:   dictionnary  
        
    :param title: le title de la ressource recherché
    :type title: str
        
    :param motherItemId: l'id de l'item mère censé porter la ressource
    :type motherItemId: int
    
    """
    
    idRes = []
    params = {}
    params['advanced[0][terms]']= title
                                                   
    url = baseUrl+'/items/show/'+str(motherItemId)+'?output=omeka-xml'
    print('url ',url)
    
    with urllib.request.urlopen(url) as x:
        
        html = x.read()

        soup = BeautifulSoup(html,'html.parser')

        if not(soup==None):
            #print(soup)
            listitem = soup.findAll('file')
            
            #print('nb item find ',len(listitem))
            
            for item in listitem:
                #print(" ---- item ---- ")
                #print(item['itemid']) 
                
                souplette = BeautifulSoup(str(item),'html.parser')
                listElement = souplette.findAll('element')
                #on cherche le title du file
                for element in listElement:
                    if element["elementid"]==str(dicDctermsIdOmeka['dcterms:title']):
                        souplette2 = BeautifulSoup(str(element),'html.parser')
                        letitletrouve = souplette2.find('text').text
                        #print('letitletrouve ',letitletrouve)
                        #print('letitlecible ',title)
                        
                        if letitletrouve == title:           
                            idRes.append(item['fileid'])
                                                                         
    return idRes  








