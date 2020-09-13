import csv

def transform(filepath,id):
  result = {}
  with open(filepath) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    # extracting field names through first row to crate map
    fields = next(csvreader)
    
    # id not found
    if id not in fields:
      print("Field %s not found in %s" % (id,filepath))
      return {}
           
    # finds the location
    IDIndex = fields.index(id)
    
    # for each line, serialize it 
    for line in csvreader:
      m = result[line[IDIndex]] = {}
      for el,id in zip(line,range(len(line))):
        m[fields[id]] = el
        
    return result
    