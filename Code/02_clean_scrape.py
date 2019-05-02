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
with open('../Data/records.csv','r') as in_file, open('../Data/records_unique.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    
    for line in in_file:
        
        cur_company = line.split(",")[5].strip()
        
        
        if cur_company in seen: continue # skip duplicate
        
        if cur_company.lower() != "none" and cur_company is not "NA" and len(cur_company) > 2:
            seen.add(cur_company)
        
        out_file.write(line)

out_file.close()
in_file.close()

from subprocess import check_output

with open('../Data/records_unique.csv','r') as in_file, open('../Data/wayback_changes.csv','w') as out_file:
    out_file.write("URL, created date, expires date, num changes, wayback URLs\n")
    for line in in_file:
        
         url = line.split(",")[2].strip()
         created_date = line.split(",")[3].strip()
         expires_date = line.split(",")[4].strip()
         
         
         if  line.split(",")[2].strip() == "hostName":
             continue
         
         wayback_unique_list = check_output("waybackpack " + url + " --list --uniques-only", shell=True)
         wayback_list = wayback_unique_list.decode('ASCII').strip()
         
         out_file.write(url + "," + created_date + "," + expires_date + ",")
         
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
         
         