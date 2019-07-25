# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:10:33 2019

@author: megahefm
"""


import requests 
from bs4 import BeautifulSoup 
import unirest

start_year = 1996
end_year = 2021

def title(): 
    # the target we want to open   

    urls_visted = set()
    
    with open('../Data/webshrinker.csv','r') as in_file, open('../Data/website_change_panel_v01.csv','w') as out_file:
        out_file.write("scrape_date, ZIP, url, created_date, expired_date, company_name, TAG_category, category1_confidence, category1_score, category1_ID, category1_parentID, category1_label, category2_confidence, category2_score, category2_ID, category2_parentID, category2_label, wayback_URLs, num_changes, " + ', '.join(["changes_in_"+str(i) for i in range(start_year, end_year)]) + "\n")
        
        for line in in_file:
            
            if line.startswith("scrape_date"):
                continue

            line_col = line.split(",")
            urls_visted.add(line_col[2])
            
            for i in range(6):
                out_file.write(line_col[i] + ",")

            TAG_category = "Category exists"
            if line_col[12] == "Uncategorized" or line_col[17] == "Under Construction":
                TAG_category = "Uncategorized or Under Construction"
            out_file.write(TAG_category + ",")

            for i in range(8, 18):
                out_file.write(line_col[i] + ",")


            wayback_urls = line_col[7]
            num_changes = int(line_col[6])
            out_file.write(wayback_urls + "," + str(num_changes) +",")

            if num_changes > 0:
                wayback_urls_list = wayback_urls.split(";")
                

                count = [0] * (end_year - start_year)
                for i in range(num_changes):
                    url = wayback_urls_list[i]                    
                    year = int(url.split("/")[4][0:4])
                    count[year - start_year] += 1

                out_file.write(', '.join(str(x) for x in count))
                
            out_file.write("\n")

    out_file.close()
    in_file.close()



    with open('../Data/wayback_changes.csv','r') as in_file, open('../Data/website_change_panel_v01.csv','a') as out_file:
        for line in in_file:
            
            if line.startswith("scrape_date"):
                continue

            line_col = line.split(",")
            
            if line_col[2] in urls_visted:
                continue

            for i in range(6):
                out_file.write(line_col[i] + ",")

            out_file.write("Webshrinker Error,")

            for i in range(8, 18):
                out_file.write(",")

            wayback_urls = line_col[7].strip()
            num_changes = int(line_col[6])
            out_file.write(wayback_urls + "," + str(num_changes) +",")

            if num_changes > 0:
                wayback_urls_list = wayback_urls.split(";")
                

                count = [0] * (end_year - start_year)
                for i in range(num_changes):
                    url = wayback_urls_list[i]                    
                    year = int(url.split("/")[4][0:4])
                    count[year - start_year] += 1

                out_file.write(', '.join(str(x) for x in count))
                
            out_file.write("\n")

    out_file.close()
    in_file.close()
                

title()
