import sys
import os
import csv2map
from PIL import Image

# parse arguments
if len(sys.argv) < 4:
    print("Usage: %s <csv file> <input dir from gdrive> <output dir>" % sys.argv[0])
    sys.exit(1)

# glow image for pasting later
glow = Image.open("poster-glow.png")

# default poster
poster_default = Image.open("default-poster.png")
poster_default_glow = Image.open("default-poster.png")
poster_default_glow.paste(glow, (0,0), glow)

# poster_default_glow.save("default-poster-glow.png")
posterMap = csv2map.transform(sys.argv[1], 'ID', 'ID in PCS')

inpath = sys.argv[2]
outpath = sys.argv[3]
valid_file_ext = set(['.png','.jpg','.jpeg'])
target_resolution = (glow.width, glow.height)

for folder in posterMap:
    documentPath = os.path.join(inpath,folder)
    
    candidateThumbnail = None
    if os.path.exists(documentPath):
        print("[%s]"%documentPath)
        for document in os.listdir(documentPath):
            fullpath = os.path.join(documentPath, document)
            filename, file_extension = os.path.splitext(fullpath)
            if (file_extension.lower() in valid_file_ext):
                candidate = Image.open(fullpath)
                if candidate.width < 300 and candidate.height < 300:
                    print("--> found %s with %dx%d" % (document, candidate.width, candidate.height))
                    candidate = candidate.convert('RGBA')
                    candidate.thumbnail(target_resolution)
                    candidateThumbnail = Image.new("RGBA",target_resolution, (0,0,0,0))
                    candidateThumbnail.paste(candidate, (target_resolution[0]//2 - candidate.width//2, target_resolution[1]//2 - candidate.height//2), candidate)
                    break
    else:
        print("[%s - NOT FOUND!]"%documentPath)
                
    outputName = posterMap[folder][r"Whova/Gather"].replace(" ", "").lower()
    if candidateThumbnail is not None:
        candidateThumbnail.save(os.path.join(outpath, "%s.png" % outputName))
        candidateThumbnail.paste(glow, (0,0), glow)
        candidateThumbnail.save(os.path.join(outpath, "%sa.png" % outputName))
    else:
        poster_default.save(os.path.join(outpath, "%s.png" % outputName))
        poster_default_glow.save(os.path.join(outpath, "%sa.png" % outputName))
        
    print("--> saved to %s and %s to %s " % ("%s.png" % outputName, "%sa.png" % outputName, outpath))


