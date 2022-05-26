# Generated by Django 3.2.12 on 2022-05-01 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(upload_to='thumbnail_pics'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]