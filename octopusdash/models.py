from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.db.models import JSONField as NativeJSONField  # Preferred
from datetime import timedelta
from django.contrib.auth import get_user_model

from django.contrib.staticfiles.storage import staticfiles_storage


User = get_user_model()



class Profile(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='octopusdash/avatars',blank=True,null=True)
    
    
    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        
        return staticfiles_storage.path('octopusdash/images/profile_picture.svg')