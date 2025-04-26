import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from generate_actions import generate_fake_logs
from django.contrib.auth.models import User
from blog.models import Post

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


for user in User.objects.all():
    obj = Post.objects.first()
    generate_fake_logs(user,obj)