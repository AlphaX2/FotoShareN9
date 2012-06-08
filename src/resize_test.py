import PIL
import os
from PIL import Image


path = "/home/user/MyDocs/DCIM/FotoShareN9_small/"
if not os.path.isdir(path):
    os.makedirs(path)

percent = 50
percent = percent * 0.01


img = Image.open("/home/user/MyDocs/streifen.jpg")
new_width = float((img.size[0])) * percent
new_height = float((img.size[1])) * percent

img = img.resize((int(new_width), int(new_height)), PIL.Image.ANTIALIAS)
img.save(path+"resized_streifen.jpg")

