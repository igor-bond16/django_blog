# Generated by Django 3.2.12 on 2022-05-01 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='default.jpg', upload_to='thumbnails/'),
        ),
    ]
