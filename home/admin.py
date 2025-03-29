from django.contrib import admin
from .models import HomePage
from django.contrib.auth.models import User
from octopusDash.core import DashboardApp
from .apps import HomeConfig

app = DashboardApp(HomeConfig)

app.register(HomePage)
app.register(User)


admin.site.register(HomePage)
