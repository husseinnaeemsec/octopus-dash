from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class SimpleModel(models.Model):
    title = models.CharField(max_length=150,null=True, blank=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    summary = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    anonymously = models.BooleanField(default=False)
    def __str__(self):
        return self.text[:50]  # First 50 characters of the question


class Poll(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='polls')
    option_text = models.CharField(max_length=255)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.option_text} ({self.votes} votes)"