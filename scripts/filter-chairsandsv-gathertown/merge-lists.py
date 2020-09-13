'''
Merges two CSV files with by the given column name. If the other values differ, this script
will copy them from the first file

Output file will have columns in the same order as the first file

Example:
python merge-lists.py list1.csv list2.csv email list3.csv

'''


import sys
import os
import io
import csv
import csv2map


# parse arguments
if len(sys.argv) < 5:
    print("Usage: %s <input csv file> <input csv file2> <column> <outputcsv file>" % sys.argv[0])
    sys.exit(1)
    
file1 = csv2map.transform(sys.argv[1],sys.argv[3])
file2 = csv2map.transform(sys.argv[2],sys.argv[3])

with open(sys.argv[4], 'w', newline='', encoding="utf8") as outputfile:
    csvwriter = csv.writer(outputfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # basically copies the first file
    with open(sys.argv[1], 'r', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        fields = next(csvreader)
        csvwriter.writerow(fields)
        
        # copies first file
        for line in csvreader:
            csvwriter.writerow(line)
            
    # now copies what is left of the second file that we haven't seen yet
    for idel in file2:
        if idel not in file1:
            line = [file2[idel][field] if field in file2[idel] else "" for field in fields]
            csvwriter.writerow(line)
        