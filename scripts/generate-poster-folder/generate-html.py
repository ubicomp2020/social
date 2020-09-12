import sys
import os
import csv2map

contentNotFoundLink = "index.html"

# parse arguments
if len(sys.argv) < 4:
    print("Usage: %s <template.html> <csv file> <output dir>" % sys.argv[0])
    sys.exit(1)

# poster_default_glow.save("default-poster-glow.png")
with open(argv[1]) as f:
    templateHTML = f.readlines()
posterMap = csv2map.transform(sys.argv[2], 'ID', 'ID in PCS')
outpath = sys.argv[3]

for folder in posterMap:


                
    outputName = posterMap[folder][r"Whova/Gather"].replace(" ", "").lower()
    if candidateThumbnail is not None:
        candidateThumbnail.save(os.path.join(outpath, "%s.png" % outputName))
        candidateThumbnail.paste(glow, (0,0), glow)
        candidateThumbnail.save(os.path.join(outpath, "%sa.png" % outputName))
    else:
        poster_default.save(os.path.join(outpath, "%s.png" % outputName))
        poster_default_glow.save(os.path.join(outpath, "%sa.png" % outputName))
        
    print("--> saved to %s and %s to %s " % ("%s.png" % outputName, "%sa.png" % outputName, outpath))


