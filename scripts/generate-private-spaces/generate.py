import sys
import os
import io
import csv2map
from PIL import Image

# parse arguments
if len(sys.argv) < 4:
    print("Usage: %s <csv file> <input dir> <output dir>" % sys.argv[0])
    sys.exit(1)

# glow image for pasting later
glow = Image.open("table-glow.png")

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


workshopMap = csv2map.transform(sys.argv[1], 'input')

outpath = sys.argv[2]
target_resolution = (glow.width, glow.height)
print("Creating thumbnails with %dx%d\n\n"%target_resolution)

# for input image
for imagePath in workshopMap:
    imageName = os.path.splitext(os.path.basename(imagePath))[0].lower()
    userImage = Image.open(imagePath)
    userImage = userImage.convert('RGBA')
    userImage.thumbnail(target_resolution)
    
    #
    # Thumbnail
    #
    
    # creates transparent base
    finalThumbnail = Image.new("RGBA",target_resolution, (255,255,255,255))
    
    # add user image at the center
    finalThumbnail.paste(userImage, (target_resolution[0]//2 - userImage.width//2, target_resolution[1]//2 - userImage.height//2), userImage)
    
    # stamp it
    finalThumbnail.paste(border, (0,0), border)
    outputFirstThumb = "%s.png" % imageName
    finalThumbnail.save(os.path.join(outpath, outputFirstThumb))
    
    # glow it
    finalThumbnail.paste(glow, (0,0), glow)
    outputSecondThumb = "%s-active.png" % imageName
    finalThumbnail.save(os.path.join(outpath, outputSecondThumb))
    
    #
    # Link
    #
    
    # cleans title from any weird html tag / character
    title = workshopMap[imagePath]["title"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
    
    # remove trailing spaces
    link = workshopMap[imagePath]["link"].strip()
    
    if len(link) == 0:
        link = contentNotFoundLink
    
    outputHtmlName = "%s.html" % imageName
    with io.open(os.path.join(outpath, outputHtmlName),'w',encoding='utf8') as f:
        f.write(templateHTML % (link, title, link))
        
    print("%s\thttps://s3-us-west-2.amazonaws.com/ubicomp.gather/workshop/%s\thttps://s3-us-west-2.amazonaws.com/ubicomp.gather/ubicompiswc_loading.png\thttps://s3-us-west-2.amazonaws.com/ubicomp.gather/workshop/%s\thttps://s3-us-west-2.amazonaws.com/ubicomp.gather/workshop/%s\t" % 
    (imageName, outputSecondThumb, outputFirstThumb, outputHtmlName))



