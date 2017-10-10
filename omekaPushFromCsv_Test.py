# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:12:35 2017

@author: mnauge01
"""

import omekaPushFromCsv as omkPusher 

import omekaRestConnector as omkCon


baseUrl = "https://guarnido.nakalona.fr"
keyApi = "XXXXX76ebdf1e1444459254eccbda91b7d81XXXX"
    
    
def deleteItemsFromTitleInCsv_test():
    pathDataFile = "C:/Users/Public/Documents/MSHS/workflow/Guarnido/03-metadatas/"
    filename = 'itemsDoublons.csv'
    pathDataFile = pathDataFile+filename
    
    configOmk  = omkCon.objConfigOmekaRestApi(baseUrl, keyApi)
    omkPusher.deleteItemsFromTitleInCsv(configOmk, pathDataFile,'title old')
    
    
def main(argv):
    deleteItemsFromTitleInCsv_test()
    
if __name__ == "__main__":
    main(sys.argv) 
