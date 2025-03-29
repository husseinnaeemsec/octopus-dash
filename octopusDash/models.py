from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class EmptyAppConfig:
    name = "Empty App"
    app_id = "empty_app"
    description = "This is default app description for the app Empty App"


class DashboardSetting(models.Model):
    MODES = (
        ('dark',"Dark"),
        ('light',"Light"),
    )
    mode = models.CharField(max_length=10,choices=MODES,default='light')
    site_id = models.PositiveIntegerField(default=1,unique=True,editable=False)
    



class AppConfig(models.Model):
    name = models.CharField(max_length=100)
    app_id = models.CharField(max_length=100,unique=True)
    description = models.TextField(max_length=2000)
    staff = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    
    def __str__(self):
        return self.name
    

class ModelConfig(models.Model):
    app = models.ForeignKey(AppConfig, on_delete=models.CASCADE,related_name='models_config')
    model_name = models.CharField(max_length=100)
    display_fields = models.CharField(max_length=2000, blank=True)
    model_form_fields = models.CharField(max_length=2000, blank=True)
    model_form_exclude = models.CharField(max_length=2000, blank=True)
    readonly_fields = models.CharField(max_length=2000, blank=True)
    search_fields = models.CharField(max_length=2000, blank=True)
    filter_fields = models.CharField(max_length=2000, blank=True)
    paginate_by = models.PositiveIntegerField(default=10)
    page_title = models.CharField(max_length=255, blank=True)
    icon = models.ImageField(upload_to='app_icons/', blank=True)



class SimpleModel(models.Model):
    title = models.CharField(max_length=150,null=True, blank=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    simple_model = models.ManyToManyField(SimpleModel,blank=True)

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


class TestModel(models.Model):
    
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()


class ResourcesAccessLog(models.Model):
    
    app = models.ForeignKey(AppConfig,on_delete=models.SET_NULL,null=True)
    model = models.CharField(max_length=150)
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='resources_access_logs')
    response_time = models.CharField(max_length=10)
    data_in = models.CharField(max_length=200)
    data_out = models.CharField(max_length=200)
    
    
    def __str__(self):
        
        return f"{self.app}"


class WebsiteStats(models.Model):
    total_requests = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    total_api_calls = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Total Requests: {self.total_requests}, Visitors: {self.unique_visitors}"


def get_website_stats():
    
    website_stats,creted = WebsiteStats.objects.get_or_create(id=1)
    
    return website_stats
