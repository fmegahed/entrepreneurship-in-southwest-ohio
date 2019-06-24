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
    
    with open('../Data/wayback_changes1.csv','r') as in_file, open('../Data/webshrinker.csv','a') as out_file, open('../Data/webshrinker_error.csv','a') as out_file1:
##        out_file.write("scrape_date, post_code, url, created_date, expired_date, company_name,num_change, wayback_URLs, Category1.Confidence, Category1.Score, Category1.ID, Category1.ParentID, Category1.Label, Category2.Confidence, Category2.Score, Category2.ID, Category2.ParentID, Category2.Label, Category3.Confidence, Category3.Score, Category3.ID, Category3.ParentID, Category3.Label, Category4.Confidence, Category4.Score, Category4.ID, Category4.ParentID, Category4.Label \n")
##        out_file1.write("url, Error\n")
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
              
                resp=requests.get(url, timeout = 30)
                
                
                #http_respone 200 means OK status 
                if resp.status_code==200:


                    try:
                        from urllib import urlencode
                    except ImportError:
                        from urllib.parse import urlencode

                    from base64 import urlsafe_b64encode
                    import hashlib
                    import json

                    def webshrinker_categories_v3(access_key, secret_key, url=b"", params={}):
                        params['key'] = access_key

                        request = "categories/v3/{}?{}".format(urlsafe_b64encode(url).decode('utf-8'), urlencode(params, True))
                        request_to_sign = "{}:{}".format(secret_key, request).encode('utf-8')
                        signed_request = hashlib.md5(request_to_sign).hexdigest()

                        return "https://api.webshrinker.com/{}&hash={}".format(request, signed_request)

                    access_key = "REf91OgMabbUZTmONupg"
                    secret_key = "ZOHNa2dSBvDwpg38QqC0"

                    api_url = webshrinker_categories_v3(access_key, secret_key, url)
                    response = requests.get(api_url)

                    status_code = response.status_code
                    data = response.json()

                    print(status_code)
                    if status_code == 200:
                        # Do something with the JSON response
                       # print(json.dumps(data, indent=4, sort_keys=True))
                        #categories = ""
                        out_file.write(line.strip() + ",")
                        for category in data['data'][0]['categories']:
                            out_file.write(str(category['confident']) + "," + str(category['score']) +"," + str(category['id']) +"," + str(category['parent']) + "," + category['label']+ ",") 
                        out_file.write("\n")
                    elif status_code == 202:
                        # The website is being visited and the categories will be updated shortly
##                        print(json.dumps(data, indent=4, sort_keys=True))
                        out_file1.write(url + ",uncategorized\n") 
                    elif status_code == 400:
                        # Bad or malformed HTTP request
                        out_file1.write(url + ",Bad or malformed HTTP request\n")
                    elif status_code == 401:
                        # Unauthorized
                        out_file1.write(url + ",Unauthorized - check your access and secret key permissions\n")
                    elif status_code == 402:
                        # Request limit reached
                        print("Account request limit reached")
                        print(json.dumps(data, indent=4, sort_keys=True))
                    else:
                        # General error occurred
                        print("A general error occurred, try the request again")
                else:
                    out_file1.write(url + ", " + str(resp.status_code) + "\n")
                    
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                out_file1.write(url + "," + str(e).replace(",", ";") + "\n")
                
    out_file.close()
    out_file1.close()
    in_file.close()

title()
