from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from ckeditor.fields import RichTextField
import os
from taggit.managers import TaggableManager
from django.utils.safestring import mark_safe

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(null=True,blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    thumbnail = models.ImageField(default='thumbnailDefault.jpg',upload_to='thumbnails/')
    headerImage = models.ImageField(default='headerDefault.jpg',upload_to='headerImages/')
    likes = models.ManyToManyField(User,related_name='blog_posts')
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.content[0:40]

    def crop_center(self,pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                            (img_height - crop_height) // 2,
                            (img_width + crop_width) // 2,
                            (img_height + crop_height) // 2))

    def crop_max_square(self,pil_img):
        return self.crop_center(pil_img, min(pil_img.size), min(pil_img.size))

    def total_likes(self):
        return self.likes.count()

    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        new_image = self.crop_max_square(Image.open(self.thumbnail.path)).resize((300, 300), Image.LANCZOS)

        new_image_io = BytesIO()
        new_image.save(new_image_io, format='JPEG')

        temp_name = os.path.basename(self.thumbnail.name)
        self.thumbnail.delete(save=False)  

        self.thumbnail.save(
            temp_name,
            content=ContentFile(new_image_io.getvalue()),
            save=False
        )

    def display_my_safefield(self):
        return mark_safe(self.content)

# class PostImage(models.Model):
#     post = models.ForeignKey(Post,default=None,on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='images/')

#     def __str__(self):
#         return self.post.title

        
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]


