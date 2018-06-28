from PIL import Image
import os, sys

#create JPEG thumbnails from image
#PARAM: Image path
def create_thumbnail(img_file):
    #TODO: exception handling
    img_org = Image.open(img_file)
    img = img_org.copy()

    #max 300px
    size = (300, 300)

    #Set thumbail file path and name
    file_path = os.path.split(img_file)
    outfile = file_path[0] + '/thumbnails/' + file_path[1] + "_thumbnail"

    img.thumbnail(size)
    thumbnail = img.save(outfile, "JPEG")
    return true
