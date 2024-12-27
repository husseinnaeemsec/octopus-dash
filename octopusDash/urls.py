from django.apps import apps
from octopusDash.core.model_registry import octopus_registry
from .views import DashboardView
from django.urls import path

urlpatterns =[
    path('',DashboardView.as_view(),name='dashboard')
]

if apps.ready:
    
    for key,value in octopus_registry.registry.items():
        
        app_registry_object = value.get("app_registry_object")
        urlpatterns.extend(app_registry_object.get_urlpatterns())

        for model in value.get("models"):
            
            urlpatterns.extend(model.get_urlpatterns())