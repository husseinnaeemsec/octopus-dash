from .. import views
from django.urls import path,include
from . import auth_urls,app_urls

urlpatterns = [
    path('',views.DashboardView.as_view(),name='od-dashboard'),
    path('apps/',include(app_urls)),
    path("auth/",include(auth_urls))
]