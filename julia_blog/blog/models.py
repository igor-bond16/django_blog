from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from ckeditor.fields import RichTextField

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(null=True,blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    thumbnail = models.ImageField(default='default.jpg',upload_to='thumbnails/')

    def __str__(self):
        return self.title

    def crop_center(self,pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                            (img_height - crop_height) // 2,
                            (img_width + crop_width) // 2,
                            (img_height + crop_height) // 2))

    def crop_max_square(self,pil_img):
        return self.crop_center(pil_img, min(pil_img.size), min(pil_img.size))

    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        new_image = self.crop_max_square(Image.open(self.thumbnail.path)).resize((300, 300), Image.LANCZOS)

        new_image_io = BytesIO()
        new_image.save(new_image_io, format='JPEG')

        temp_name = self.thumbnail.name
        self.thumbnail.delete(save=False)  

        self.thumbnail.save(
            temp_name,
            content=ContentFile(new_image_io.getvalue()),
            save=False
        )

        


class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]


