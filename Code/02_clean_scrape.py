import csv

# 
#with open('../Data/records.csv', 'rb') as in_file, open('records_unique.csv','w') as out_file:
#    records = csv.reader(in_file, delimiter=',', quotechar='|')
#
#    seen = set() # set for fast O(1) amortized lookup
#    for line in records:
#        if line in seen: continue # skip duplicate
#
#        seen.add(line[5])
#        out_file.write(line)
#

#with open('../Data/records.csv','r') as in_file, open('../Data/records_unique.csv','w') as out_file:
#    seen_company_name = set() # set for fast O(1) amortized lookup
#    seen_company_hostname = set()
#    
#    for line in in_file:
#        cur_company_name = line.split(",")[5].strip()
#        cur_company_hostname  = line.split(",")[2].strip()  
#
#        if cur_company_name in seen_company_name: continue # skip duplicate
#        if cur_company_hostname in seen_company_hostname: continue # skip duplicate
#
#        seen_company_hostname.add(cur_company_hostname)
#        if cur_company_name.lower() != "none" and cur_company_name is not "NA" and len(cur_company_name) > 2:
#            seen_company_name.add(cur_company_name)
#                
#        out_file.write(line)
#
#out_file.close()
#in_file.close()

from subprocess import check_output

with open('../Data/records_unique.csv','r') as in_file, open('../Data/wayback_changes.csv','w') as out_file:
    out_file.write("scrape_date, post_code, url, created_date, expired_date, company_name, num_changes, wayback_URLs\n")
    for line in in_file:
         scrape_date = line.split(",")[0].strip()
         post_code = line.split(",")[1].strip()
         url = line.split(",")[2].strip()
         created_date = line.split(",")[3].strip()
         expires_date = line.split(",")[4].strip()
         company_name = line.split(",")[5].strip()
         
         #Ignore the first line in the file
         if  line.split(",")[2].strip() == "hostName":
             continue
         
         wayback_unique_list = check_output("waybackpack " + url + " --list --uniques-only", shell=True)
         wayback_list = wayback_unique_list.decode('ASCII').strip()
         
         out_file.write(scrape_date + "," + post_code + "," + url + "," + created_date + "," + expires_date + "," + company_name + ",")
         
         if len(wayback_list) != 0:
            wayback_list_as_list = wayback_list.split("\n")
            no_changes = str(len(wayback_list_as_list))
            out_file.write(no_changes + ",")
            
            for wayback_data in wayback_list_as_list:
                 out_file.write(wayback_data.strip() + ";")
            out_file.write("\n")
         else:
            out_file.write("0\n")
            
out_file.close()
in_file.close()         
         
         
