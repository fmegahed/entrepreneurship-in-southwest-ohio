# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 08:29:48 2019

@author: megahefm
"""

# Loading required libraries
import requests
import json
from datetime import datetime


# Function to overcome errors in printing Nones
def xstr(s):
    return '' if s is None else str(s)


# Defining how the files will be saved into csv
meta_data_file = open('../Data/meta_data.csv','w')
meta_data_file.write("scrape_date ,post_code ,record_count ,max_page\n")   
records_file = open('../Data/records.csv','w')
records_file.write("scrape_date ,post_code , hostName ,createdDate ,expiresDate ,companyName \n" )


# URL and post codes
url = "https://api.securitytrails.com/v1/domains/list"
# Zip Codes: Pasted from the CSV using text editor for our convenience 
postcodes = ["43101", "43103", "43106", "43113", "43115", "43116", "43117", "43128", "43142", "43145", "43146", "43156", "43160", "43164", "45001", "45002", "45003", "45004", "45005", "45011", "45012", "45013", "45014", "45015", "45018", "45030", "45032", "45033", "45034", "45036", "45039", "45040", "45041", "45042", "45044", "45050", "45051", "45052", "45053", "45054", "45055", "45056", "45061", "45062", "45063", "45064", "45065", "45066", "45067", "45068", "45069", "45070", "45071", "45101", "45102", "45103", "45105", "45106", "45107", "45111", "45112", "45113", "45114", "45115", "45118", "45119", "45120", "45121", "45122", "45123", "45130", "45131", "45132", "45133", "45135", "45140", "45142", "45144", "45146", "45147", "45148", "45150", "45152", "45153", "45154", "45155", "45156", "45157", "45158", "45159", "45160", "45162", "45164", "45166", "45167", "45168", "45169", "45171", "45172", "45174", "45176", "45177", "45201", "45202", "45203", "45204", "45205", "45206", "45207", "45208", "45209", "45211", "45212", "45213", "45214", "45215", "45216", "45217", "45218", "45219", "45220", "45221", "45222", "45223", "45224", "45225", "45226", "45227", "45229", "45230", "45231", "45232", "45233", "45234", "45235", "45236", "45237", "45238", "45239", "45240", "45241", "45242", "45243", "45244", "45245", "45246", "45247", "45248", "45249", "45250", "45251", "45252", "45253", "45254", "45255", "45258", "45262", "45263", "45264", "45267", "45268", "45269", "45270", "45271", "45273", "45274", "45275", "45277", "45280", "45296", "45298", "45299", "45301", "45305", "45307", "45309", "45311", "45314", "45315", "45316", "45320", "45321", "45322", "45324", "45325", "45327", "45330", "45335", "45338", "45342", "45343", "45345", "45347", "45354", "45370", "45377", "45378", "45381", "45382", "45384", "45385", "45387", "45401", "45402", "45403", "45404", "45405", "45406", "45409", "45410", "45412", "45413", "45414", "45415", "45416", "45417", "45419", "45420", "45422", "45423", "45424", "45426", "45428", "45429", "45430", "45431", "45432", "45433", "45434", "45435", "45437", "45439", "45440", "45441", "45448", "45449", "45458", "45459", "45469", "45470", "45475", "45479", "45481", "45482", "45490", "45601", "45612", "45613", "45616", "45617", "45618", "45624", "45628", "45629", "45630", "45633", "45636", "45642", "45644", "45646", "45647", "45648", "45650", "45652", "45653", "45657", "45660", "45661", "45662", "45663", "45671", "45673", "45677", "45679", "45681", "45682", "45683", "45684", "45687", "45690", "45693", "45694", "45697", "45699", "45999"]
# API key for Security Trails
querystring = {"apikey":"7GpQJYMryiL24bulfUWmqiQgeRrExUKx"}


# Querying the API
for postcode in postcodes:    
    payload = "{\"query\":\"whois_country='united states' and  whois_postalCode='" + postcode + "'\"}"
    response = requests.request("POST", url, data=payload, params=querystring)
    json_data = json.loads(response.text)
    
#   Obtaining meta data to identify number of pages and records per postal code
    if 'meta' in json_data:
        max_page = json_data["meta"]["max_page"]
        record_count = json_data['record_count']
        meta_data_file.write(xstr(datetime.today().strftime('%Y-%m-%d')) + "," + xstr(postcode) +"," + xstr(record_count) + "," + xstr(max_page) +"\n") 
    
#   Inner loop --> Going through first page
    if 'records' in json_data:
        for i in range(0, len(json_data['records'])):
            companyName = str(json_data['records'][i]['computed']['company_name']).replace(",", "").replace("/t", "")
            hostName = json_data['records'][i]['hostname']
            expiresDate = json_data['records'][i]['whois']['expiresDate']
            if expiresDate is not None:
                expiresDate = expiresDate * 0.001
                expiresDate = xstr(datetime.utcfromtimestamp(expiresDate).strftime('%Y-%m-%d'))
            else:
                expiresDate = "NA"
                
            createdDate = json_data['records'][i]['whois']['createdDate']
            if createdDate is not None:
                createdDate = createdDate * 0.001
                createdDate = xstr(datetime.utcfromtimestamp(createdDate).strftime('%Y-%m-%d'))
            else:
                createdDate = "NA"
            records_file.write(xstr(datetime.today().strftime('%Y-%m-%d')) + "," + xstr(postcode) + "," + xstr(hostName) + "," + createdDate + "," + expiresDate +"," + xstr(companyName) + "\n" )
#    If pages > 1 --> iterate through remaining pages and records
        if max_page > 1:    
            for pageno in range(2, max_page+1):
                querystring = {"apikey":"7GpQJYMryiL24bulfUWmqiQgeRrExUKx", "page":str(pageno)}
                payload = "{\"query\":\"whois_country='united states' and  whois_postalCode='" + postcode + "'\"}"
                response = requests.request("POST", url, data=payload, params=querystring)
                
                for i in range(0, len(json_data['records'])):
                    companyName = json_data['records'][i]['computed']['company_name']
                    hostName = json_data['records'][i]['hostname']
                    expiresDate = json_data['records'][i]['whois']['expiresDate']
                    if expiresDate is not None:
                        expiresDate = expiresDate * 0.001
                        expiresDate = xstr(datetime.utcfromtimestamp(expiresDate).strftime('%Y-%m-%d'))
                    else:
                        expiresDate = "NA"
                        
                    createdDate = json_data['records'][i]['whois']['createdDate']
                    if createdDate is not None:
                        createdDate = createdDate * 0.001
                        createdDate = xstr(datetime.utcfromtimestamp(createdDate).strftime('%Y-%m-%d'))
                    else:
                        createdDate = "NA"
                    records_file.write(xstr(datetime.today().strftime('%Y-%m-%d')) + "," + xstr(postcode) + "," + xstr(hostName) + "," + createdDate + "," + expiresDate +"," + xstr(companyName) + "\n" )
                
meta_data_file.close()
records_file.close()