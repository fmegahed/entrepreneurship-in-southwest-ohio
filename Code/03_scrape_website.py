# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:10:33 2019

@author: megahefm
"""


import requests 
from bs4 import BeautifulSoup 
import unirest

def title(): 
    # the target we want to open   
    
    with open('../Data/temp.csv','r') as in_file, open('../Data/websites_metadata1.csv','w') as out_file:
        out_file.write("URL, Title, Category\n")
        for line in in_file:
            
            if line.startswith("scrape_date"):
                continue
            
##            num_changes = int(line.split(",")[3])
##            if num_changes == 0:
##                contine
            
            url = "http://www." + line.split(",")[2]
            print(url)
           
            #open with GET method
            try:
                resp=requests.get(url)
                
          
                #http_respone 200 means OK status 
                if resp.status_code==200:

                    try:
                        from urllib import urlencode
                    except ImportError:
                        from urllib.parse import urlencode

                    from base64 import urlsafe_b64encode
                    import hashlib

                    def webshrinker_categories_v3(access_key, secret_key, url=b"", params={}):
                        params['key'] = access_key

                        request = "categories/v3/{}?{}".format(urlsafe_b64encode(url).decode('utf-8'), urlencode(params, True))
                        request_to_sign = "{}:{}".format(secret_key, request).encode('utf-8')
                        signed_request = hashlib.md5(request_to_sign).hexdigest()

                        return "https://api.webshrinker.com/{}&hash={}".format(request, signed_request)

                    access_key = "REf91OgMabbUZTmONupg"
                    secret_key = "ZOHNa2dSBvDwpg38QqC0"

                    print("here")
                    print(webshrinker_categories_v3(access_key, secret_key, url))


    ##                response = unirest.get("https://enclout-dmoz.p.rapidapi.com/show.json?url=" + url,
    ##                  headers={
    ##                    "X-RapidAPI-Host": "enclout-dmoz.p.rapidapi.com",
    ##                    "X-RapidAPI-Key": "59478c33c2mshd913bd4e63cb3f5p1aa632jsnae1b2bf6137e"
    ##                  }
    ##                )
    ##
    ##                print(response.body)
                    
    ##                #print(resp)
    ##                
    ##                # we need a parser,Python built-in HTML parser is enough . 
    ##                soup=BeautifulSoup(resp.text,'html.parser')     
    ##               
    ##                # l is the list which contains all the text i.e news  
    ##               # title = soup.title
    ##               # print(title)
    ##
    ##                meta = soup.findAll("a", {"class": "cat-url"}) 
    ##                print(meta)
    ##                out_file.write(url + "," + str(meta) +"\n")
                
                else: 
                    print("Error") 
          
title()
