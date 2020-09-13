'''

Filters out student volunteers (SVs) and chairs from a CSV (comma separated values) file.

Assumptions:
-> input file is a csv file with the following columns email,name,role,affiliation
-> SVs have (SV) in their affiliation
-> chairs have (Something Chair) in their affiliation

'''

import sys
import os
import io
import csv


# parse arguments
if len(sys.argv) < 3:
    print("Usage: %s <input csv file> <output csv file>" % sys.argv[0])
    sys.exit(1)
    
# should we make everyone admin?
makeAdmin = True

# strings to check agains (I would use something more efficient it this had more than 10k elements, but with 1k elements 
# the expensive string search works just fine)
chairStr = "chair)"
svStr = "(sv"


chairsCount = 0
svsCount = 0
admins = 0


with open(sys.argv[1], encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    # opens output file
    with open(sys.argv[2], 'w', newline='', encoding="utf8") as outputfile:
        csvwriter = csv.writer(outputfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        # writing header (expecting: email, name, role, affiliation
        fields = next(csvreader)
        csvwriter.writerow(fields)

        # read each line and filter out only chairs,
        for line in csvreader:
        
            affiliationLower = line[3].lower()
            
            # chair?
            if chairStr in affiliationLower:
                csvwriter.writerow([line[0], line[1], 'admin' if makeAdmin else line[2], line[3]])
                chairsCount += 1
            # SV?
            elif svStr in affiliationLower:
                csvwriter.writerow([line[0], line[1], 'admin' if makeAdmin else line[2], line[3]])
                svsCount += 1
            # finally, add anyone with administrative powers to it
            elif line[2].lower() == 'admin':
                csvwriter.writerow(line)
                admins += 1
                
                

print ("Saved new list to %s with %d chairs, %d SVs, and %d guests previously set as admin" % (sys.argv[2], chairsCount, svsCount, admins))


