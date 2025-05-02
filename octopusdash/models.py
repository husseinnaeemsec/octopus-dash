from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.db.models import JSONField as NativeJSONField  # Preferred
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from django.contrib.staticfiles.storage import staticfiles_storage


User = get_user_model()

class Field(models.Model):
    ''' This is just a test to try all kinds of fields on Octopusdash. '''
    
    GENDERS = (
        ("male", "Male"),
        ("female", "Female"),
    )
    
    # CharField for name
    name = models.CharField(max_length=150, null=True, blank=True,help_text='Name of the field')
    
    # TextField for description
    desc = models.TextField(max_length=4000, blank=True, null=True,help_text='Short descirption With Rich text editor')
    
    # Gender choice field
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDERS,help_text='Choice Gender')
    
    # ManyToManyField for users (assumed to be a relation to User)
    users = models.ManyToManyField(User, blank=True,help_text='Select users')
    
    # BooleanField for active status
    is_active = models.BooleanField(default=True, null=True, blank=True,help_text='Wither this Filed is active or not ')
    
    # URLField for website links
    url = models.URLField(blank=True, null=True,help_text='Any valid URL that starts with (www,https,etc)')
    
    # SlugField for URL-friendly strings
    slug = models.SlugField(blank=True, null=True,help_text='SEO optamized url ex: (How to setup a Django Project. ) ')
    
    # EmailField for email addresses
    email = models.EmailField(blank=True, null=True, help_text='Any active email')
    
    # PositiveIntegerField for non-negative integers (e.g., age, count)
    number = models.PositiveIntegerField(default=0, blank=True, null=True,help_text='Any positive number')
    
    # DateField for storing date values
    datefield = models.DateField(null=True, blank=True,help_text='Inter any valid date')
    
    # DateTimeField for date and time values
    datetimefield = models.DateTimeField(verbose_name='Date Time Field', null=True, blank=True,help_text='Local Date and Time field')
    
    # TimeField for storing time values (without date)
    timefield = models.TimeField(null=True, blank=True,help_text='Time filed')
    
    # Choices field (can be used for a predefined set of options)
    choice_field = models.CharField(max_length=20, choices=GENDERS, default='male', blank=True, null=True,help_text='Another radio group select ')
    
    # FileField for file uploads (not specified but included for testing purposes)
    file_upload = models.FileField(upload_to='uploads/', null=True, blank=True,help_text='Make sure that the file format is one of these (image/png,jpg,svg , PDF , DOC )')
    
    # ImageField for image uploads (optional, just for testing)
    image_upload = models.ImageField(upload_to='images/', null=True, blank=True,help_text='Only images are allowed ')
    
    # IntegerField for regular integer values (not limited to positive values)
    age = models.IntegerField(null=True, blank=True,help_text='Only 18+ are allowed to register in this website ')
    
    # DecimalField for fixed-point decimal numbers (useful for prices, etc.)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,help_text='Price with floating points')
    
    # FloatField for floating point numbers
    weight = models.FloatField(null=True, blank=True,help_text='Float field')
    
    # UUIDField for storing UUIDs (unique identifiers)
    uuid_field = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True,help_text='UUID Field auto-created')
    
    # JSONField for storing JSON data (available in Django 3.1+)
    json_data = models.JSONField(default=dict, blank=True, null=True,help_text='JSON Formated data')
    
    # DurationField for storing time spans (e.g., hours, minutes)
    duration = models.DurationField(null=True, blank=True,help_text='This field is only works with PostgreSQL ')
    
    def __str__(self):
        return self.name or ' '


class FieldImage(models.Model):
    field = models.ForeignKey(Field,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f"Image for field {str(self.field)}  "

class FieldAttr(models.Model):
    ''' This is just a test to try all kind of fields on Octopusdash. '''

    field  = models.ForeignKey(Field,on_delete=models.CASCADE)
    attr = models.CharField(max_length=140)
    desc = models.TextField(max_length=4000,blank=True)

class Profile(models.Model):
    ''' User's profile to manage Octopusdash.'''
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='octopusdash/avatars',blank=True,null=True)
    
    
    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        
        return staticfiles_storage.path('octopusdash/images/profile_picture.svg')