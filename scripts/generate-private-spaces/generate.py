import sys
import os
import io
import csv2map
import re
from PIL import Image, ImageDraw

# parse arguments
if len(sys.argv) < 3:
    print("Usage: %s <csv file> <output dir>" % sys.argv[0])
    sys.exit(1)

# glow image for pasting later
glow = Image.open("table-glow.png")

# podium to be added on top of the rug
podium = Image.open("podium.png")

# table background
table_back = Image.open("table-background.png")

# mask to cut out tables from rub
rug_mask = Image.open("rug-mask.png")
rug_mask= rug_mask.convert('RGBA')
inputMaskData = rug_mask.getdata()

# default poster
table1_default = Image.open("default-table1.png")
table1_default_glow = Image.open("default-table1.png")

table2_default = Image.open("default-table2.png")
table2_default_glow = Image.open("default-table2.png")

icon_default = Image.open("default-teleporter.png")
rug_default = Image.open("default-rug.png")

# create glow effect for tables
table1_default_glow.paste(glow, (0,0), glow)
table2_default_glow.paste(glow, (0,0), glow)

# html template
with io.open("template-nocontent.html",'r',encoding='utf8') as f:
    templateHTMLBlank = "".join(f.readlines())

# html template when link is not there
with io.open("template.html",'r',encoding='utf8') as f:
    templateHTML = "".join(f.readlines())


outpath = sys.argv[2]
target_table_resolution = (glow.width, glow.height)
target_rug_resolution = (rug_default.width, rug_default.height)
target_icon_resolution = (icon_default.width, icon_default.height)

valid_file_ext = set(['.png','.jpg','.jpeg'])
valid_file_name = set(['table1,rug,icon,table2'])
valid_table_name = set(['table1', 'table2'])

# helper method
def PasteImageAtCenter(image, resolution):
    image = image.convert('RGBA')
    image.thumbnail(resolution)
    newImage = Image.new("RGBA",resolution, (255,255,255,0))
    newImage.paste(image, (resolution[0]//2 - image.width//2, resolution[1]//2 - image.height//2), image)
    return newImage



#
# first, go over the input folder to create thumbnails
#

# list all the folders inside the 'input' folder
folders = os.listdir("input")
missingInstitutions = set([x for x in range(16)])

folderMap = {}
for folderName in folders:
    n = re.search("(\d+)",folderName)
    
    if n[0]:
        spaceNumber = int(n[0])
        missingInstitutions.remove(spaceNumber)
        print("\n--> Found Institution %d at %s" % (spaceNumber,folderName))
        
        # now that we have a folder, we look for files
        folderPath = os.path.join("input", folderName)
        filesInFolder = os.listdir(folderPath)
        
        # checks
        
        # for each valid file, parse it and create a new file in <output dir>
        expectedFiles = set (['table1', 'table2', 'rug', 'icon'])
        for file in filesInFolder:
            fullpath = os.path.join(folderPath, file)
            filename, file_extension = os.path.splitext(file)
            filename = filename.lower()
            if (file_extension.lower() in valid_file_ext):
                # do we have a table?
                if filename in valid_table_name:
                    expectedFiles.remove(filename)
                    tableIMG = Image.open(fullpath)
                    print("> Table: %s in %s with %dx%d" % (filename, fullpath, tableIMG.width, tableIMG.height))
                    
                    # fixes table image within the expected resolution
                    newTableIMG = Image.new("RGBA",target_table_resolution, (255,255,255,0))
                    newTableIMG.paste(table_back, (-32,-32), table_back)
                    
                    tableIMG = tableIMG.convert('RGBA')
                    tableIMG.thumbnail(target_table_resolution)
                    newTableIMG.paste(tableIMG, (target_table_resolution[0]//2 - tableIMG.width//2, target_table_resolution[1]//2 - tableIMG.height//2), tableIMG)
                    
                    # saves table
                    newTableIMG.save(os.path.join(outpath, "s%d%s.png" % (spaceNumber,filename)))
                    
                    # saves active version
                    newTableIMG.paste(glow, (0,0), glow)
                    newTableIMG.save(os.path.join(outpath, "s%d%sa.png" % (spaceNumber,filename)))
                elif filename == "icon":
                    expectedFiles.remove(filename)
                    iconIMG = Image.open(fullpath)
                    print("> Icon/Teleporter: %s in %s with %dx%d" % (filename, fullpath, iconIMG.width, iconIMG.height))
                    # fixes table image within the expected resolution
                    newiconIMG = PasteImageAtCenter(iconIMG,target_icon_resolution)
                    
                    # saves icon
                    newiconIMG.save(os.path.join(outpath, "s%d%s.png" % (spaceNumber,filename)))
                elif filename == "rug":
                    expectedFiles.remove(filename)
                    rugIMG = Image.open(fullpath)
                    print("> Rug: %s in %s with %dx%d" % (filename, fullpath, rugIMG.width, rugIMG.height))
                    # fixes table image within the expected resolution
                    newrugIMG = PasteImageAtCenter(rugIMG,target_rug_resolution)
                    
                    # apply a mask to the rug
                    inputData = newrugIMG.getdata()

                    newRugData = []
                    for inputPixel,inputMaskPixel in zip(inputData,inputMaskData):
                        newRugData.append((inputPixel[0], inputPixel[1],inputPixel[2], inputMaskPixel[3]))
                    newrugIMG.putdata(newRugData)
                    newrugIMG.paste(podium, (10*32,14*32), podium)
                    
                    # saves icon
                    newrugIMG.save(os.path.join(outpath, "s%d%s.png" % (spaceNumber,filename)),'PNG')
                else:
                    print ("! Ignoring image file %s" % fullpath)
            else:
                print ("! Ignoring unkwnon file file %s" % fullpath)
                    
        # default file for each file that we did not find
        if "table1" in expectedFiles:
            print("! table1.png not found: using default")
            table1_default.save(os.path.join(outpath, "s%dtable1.png" % spaceNumber))
            table1_default_glow.save(os.path.join(outpath, "s%dtable1a.png" % spaceNumber))
            
        if "table2" in expectedFiles:
            print("! table2.png not found: using default")
            table2_default.save(os.path.join(outpath, "s%dtable2.png" % spaceNumber))
            table2_default_glow.save(os.path.join(outpath, "s%dtable2a.png" % spaceNumber))
        
        if "rug" in expectedFiles:
            print("! rug.png not found: using default")
            rug_default.save(os.path.join(outpath, "s%drug.png" % spaceNumber))
            
        if "icon" in expectedFiles:
            print("! icon.png not found: using default")
            rug_default.save(os.path.join(outpath, "s%dicon.png" % spaceNumber))
            
print("\n")
for institution in missingInstitutions:
    print("--> Creating default images for institution %d" % institution)
    table2_default.save(os.path.join(outpath, "s%dtable2.png" % institution))
    table2_default_glow.save(os.path.join(outpath, "s%dtable2a.png" % institution))
    table1_default.save(os.path.join(outpath, "s%dtable1.png" % institution))
    table1_default_glow.save(os.path.join(outpath, "s%dtable1a.png" % institution))
    rug_default.save(os.path.join(outpath, "s%drug.png" % institution))
    rug_default.save(os.path.join(outpath, "s%dicon.png" % institution))
    
    
#
# second, go over CSV to add links
#
print("")
privateSpaceMap = csv2map.transform(sys.argv[1], 'Space ID')
for privateSpace in privateSpaceMap:
    print("Creating links to space %s" % privateSpace)
    table1Link = privateSpaceMap[privateSpace]["Table 1 Link"].strip()
    table2Link = privateSpaceMap[privateSpace]["Table 2 Link"].strip()
    institution = privateSpaceMap[privateSpace]["Institution"].strip()
    
    # table 1
    outputHtmlName = "s%stable1.html" % privateSpace
    if len(table1Link) > 0:
        with io.open(os.path.join(outpath, outputHtmlName),'w',encoding='utf8') as f:
            f.write(templateHTML % (table1Link, institution, table1Link))
    else:
        with io.open(os.path.join(outpath, outputHtmlName),'w',encoding='utf8') as f:
            f.write(templateHTMLBlank)
        
    # table 2
    outputHtmlName = "s%stable2.html" % privateSpace
    if len(table2Link) > 0:
        with io.open(os.path.join(outpath, outputHtmlName),'w',encoding='utf8') as f:
            f.write(templateHTML % (table2Link, institution, table2Link))
    else:
        with io.open(os.path.join(outpath, outputHtmlName),'w',encoding='utf8') as f:
            f.write(templateHTMLBlank)