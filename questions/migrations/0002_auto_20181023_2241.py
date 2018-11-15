# Generated by Django 2.1.2 on 2018-10-23 17:11

from django.db import migrations, models
import questions.models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catagory',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=questions.models.image_upload_url),
        ),
        migrations.AlterField(
            model_name='question',
            name='catagory',
            field=models.ManyToManyField(blank=True, to='questions.Catagory', verbose_name='Catagories'),
        ),
    ]
