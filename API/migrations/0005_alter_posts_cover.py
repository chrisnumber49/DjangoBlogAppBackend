# Generated by Django 3.2.8 on 2021-11-09 00:14

import API.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=API.models.upload_path),
        ),
    ]
