from django.test import TestCase
from .models import Image, Tag, Comment, User

# Create your tests here.
class HomeTest(TestCase):

    def setUp(self):
        self.images = Image.objects.create(description='testikuva', views=0, date=datetime.now(), uploaded_by=User.objects.first())