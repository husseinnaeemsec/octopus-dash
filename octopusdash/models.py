from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=5000)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'posts'
        


class Book(models.Model):
    
    title = models.CharField(max_length=150)
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE,related_name='books')