# Generated by Django 2.1.2 on 2018-10-28 13:18

from django.db import migrations, models
import questions.models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_auto_20181028_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='error_file',
            field=models.FileField(default='error.txt', upload_to=questions.models.get_error_upload_url),
        ),
    ]
