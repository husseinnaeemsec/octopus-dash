from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=5000)
    likes = models.PositiveIntegerField(default=0)
    reads = models.ManyToManyField(User, related_name='user_read', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,null=True)
    tag = models.ForeignKey(Tag,on_delete=models.DO_NOTHING,null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)



class SimpleBook(models.Model):
    
    title = models.CharField(max_length=255,help_text='Name of the book')
    content = models.TextField(max_length=5000)


class ContentImage(models.Model):
    book = models.ForeignKey(SimpleBook,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/images',blank=True)
