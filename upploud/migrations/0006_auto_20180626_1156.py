# Generated by Django 2.0.6 on 2018-06-26 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upploud', '0005_auto_20180624_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='thumbnails'),
        ),
    ]
