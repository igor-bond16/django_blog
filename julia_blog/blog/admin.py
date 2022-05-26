from django.contrib import admin

# Register your models here.
from .models import Post,Message

# class PostImageAdmin(admin.StackedInline):
#     model = PostImage

admin.site.register(Post)
admin.site.register(Message)

# class PostImageAdmin(admin.StackedInline):
#     model = PostImage

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     inlines = [PostImageAdmin]

#     class Meta:
#        model = Post

# @admin.register(PostImage)
# class PostImageAdmin(admin.ModelAdmin):
#     pass



