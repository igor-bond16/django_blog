# Generated by Django 3.2.12 on 2022-04-29 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20220426_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='default.jpg', upload_to='thumbnail_pics'),
        ),
    ]
