from .models import Tag, Image

#Takes string and Image instance ass arguments,
#parses tags from string and adds them to Image.Tag(ManyToMany field)
def strip_tagfield(tagfield, image):
    #split targfield into array using , as delimiter
    tag_list = tagfield.split(',')
    #remove whitespaces from beginning and end & change to lowercase
    tag_list = [i.strip().lower() for i in tag_list]
    #remove empty elements
    tag_list = [i for i in tag_list if i != '']
    #remove longer than 20 char tags
    tag_list = [i for i in tag_list if len(i) <= 20]

    #Get or create tags and add to image.Tags
    for t in tag_list:
        tag_obj = Tag.objects.get_or_create(name=t)
        image.tags.add(tag_obj[0])

    #Commit added tags
    image.save()