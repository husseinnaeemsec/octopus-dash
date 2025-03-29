from .views import DashboardView,UserManagement,Login,NewUserView
from django.urls import path
from .core import configure_urlpatterns

app_name ='octopus'

urlpatterns =[
    path('',DashboardView.as_view(),name='octopus-dashboard'),
    path('user-management/',UserManagement.as_view(),name='users-list'),
    path('user-management/add/',NewUserView.as_view(),name='add-new-user')
]

urlpatterns = configure_urlpatterns(urlpatterns)