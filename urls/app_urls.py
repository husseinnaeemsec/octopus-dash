from ..views.app_views import AppView,ModelView
from ..views.model_views import CreateInstanceView,UpdateInstanceView,DeleteInstanceView
from django.urls import path,include

model_urls = [
    path("",ModelView.as_view(),name='od-model-view'),
    path("create/",CreateInstanceView.as_view(),name='od-create-instance'),
    path("<int:pk>/update/",UpdateInstanceView.as_view(),name='od-update-instance'),
    path("<int:pk>/delete/",DeleteInstanceView.as_view(),name='od-delete-instance')

]

urlpatterns = [
    path('<str:app>/',AppView.as_view(),name='od-app-view'),
    path('<str:app>/<str:model>/',include(model_urls))
]

