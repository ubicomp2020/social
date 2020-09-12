import sys
import os
import io
import csv2map

contentNotFoundLink = "index.html"

# parse arguments
if len(sys.argv) < 4:
    print("Usage: %s <template.html> <csv file> <output dir>" % sys.argv[0])
    sys.exit(1)

# poster_default_glow.save("default-poster-glow.png")
with io.open(sys.argv[1],'r',encoding='utf8') as f:
    templateHTML = "".join(f.readlines())
posterMap = csv2map.transform(sys.argv[2], 'ID', 'ID in PCS')
outpath = sys.argv[3]

for folder in posterMap:
    # cleans title from any weird html tag / character
    title = posterMap[folder]["Title(49)"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
    
    # remove trailing spaces
    link = posterMap[folder]["main content"].strip()
    if len(link) == 0:
        link = contentNotFoundLink
    
    outputName = posterMap[folder][r"Whova/Gather"].replace(" ", "").lower()    
    with io.open(os.path.join(outpath, "%s.html" % outputName),'w',encoding='utf8') as f:
        f.write(templateHTML % (link, title, link))

    print("--> saved to %s to %s " % ("%s.html" % outputName, outpath))


