# Generated by Django 2.0.6 on 2018-06-21 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upploud', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='file',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
