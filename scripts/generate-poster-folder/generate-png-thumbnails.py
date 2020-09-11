import sys
from PIL import Image


glow = Image.open("poster-glow.png")
poster_default = Image.open("default-poster.png")
poster_default_glow = Image.open("default-poster.png")

poster_default_glow.paste(glow, (0,0), glow)
poster_default_glow.save("default-poster-glow.png")

