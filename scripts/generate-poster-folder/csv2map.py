import csv

def transform(filepath,id1,id2):
  result = {}
  with open(filepath) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    # extracting field names through first row to crate map
    fields = next(csvreader)
    
    # id not found
    if id1 not in fields:
      print("Field %s not found in %s" % (id1,filepath))
      return {}
      
    # id not found
    if id2 not in fields:
      print("Field %s not found in %s" % (id2,filepath))
      return {}
      
    # finds the location
    ID1Index = fields.index(id1)
    ID2Index = fields.index(id2)
    
    # for each line, serialize it 
    for line in csvreader:
      m = result["%s_%s" % (line[ID1Index], line[ID2Index])] = {}
      for el,id in zip(line,range(len(line))):
        m[fields[id]] = el
        
    return result
    