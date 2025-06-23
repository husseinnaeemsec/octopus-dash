from django.urls import path
from ..views.auth_views import login_view


urlpatterns = [
    path('login/',login_view,name='od-login')
]