from . import views
from django.urls import path,include

edit_model_views = [
]

model_urls = [
    path("list/",views.ModelListView.as_view(),name='list-objects'),
    path("create/",views.CreateInstanceView.as_view(),name='create-object'),
    path("update/<int:pk>/",views.UpdateInstanceView.as_view(),name='update-object'),
]

app_urls = [
    path("",views.AppView.as_view(),name='app-view'),
    path("<str:model_name>/",include(model_urls),name='model')
]



urlpatterns = [
    path("<str:app>/",include(app_urls),name='app-views')
]

