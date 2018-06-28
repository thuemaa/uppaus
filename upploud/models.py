from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image as PIL_Image
from io import BytesIO
import os, sys
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    #return name of the tag
    def __str__(self):
        return self.name

class Image(models.Model):
    file = models.ImageField(upload_to='images')
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True)
    description = models.CharField(max_length=50)
    views = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, related_name='user_images', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.description

    #custom save, required for thumbnail
    def save(self, *args, **kwargs):

        if not self.create_thumbnail():
            raise Exception('error creating thumbnail.')

        super(Image, self).save(*args, **kwargs)


    def create_thumbnail(self):
        img = PIL_Image.open(self.file)

        # max 300px
        size = (300, 300)

        # Set thumbail filename
        t_name, t_ext = os.path.splitext(self.file.name)
        thumbnail_filename = t_name + '_t' + t_ext

        img.thumbnail(size, PIL_Image.ANTIALIAS)
        temp_thumb = BytesIO()

        if t_ext in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif t_ext == '.gif':
            FTYPE = 'GIF'
        elif t_ext == '.png':
            FTYPE = 'PNG'
        else:
            return False

        img.save(temp_thumb, FTYPE)

        temp_thumb.seek(0)
        self.thumbnail.save(thumbnail_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

class Comment(models.Model):
    comment = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Image, related_name='image_comments', on_delete=models.CASCADE)
    nick = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)

    #return DateTimeField in numeral form
    #NOT IN USE
    def __str__(self):
        return self.date.strftime('%d.%m.%y %H:%M:%S')

