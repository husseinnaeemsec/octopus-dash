from . import views
from . import octopusdash_views
from django.urls import path,include


edit_model_views = [
]

model_urls = [
    path('',views.ModelView.as_view(),name='model-view'),
    path("list/",views.ModelListView.as_view(),name='list-objects'),
    path("create/",views.CreateInstanceView.as_view(),name='create-object'),
    path("update/<int:pk>/",views.UpdateInstanceView.as_view(),name='update-object'),
    path("delete/<int:pk>/",views.DeleteInstanceView.as_view(),name='delete-object'),
]

app_urls = [
    path("",views.AppView.as_view(),name='app-view'),
    path("<str:model_name>/",include(model_urls),name='model-view')
]


apps_urls = [
    path('',views.apps_view,name='octopusdash-apps_list'),
    path("<str:app>/",include(app_urls),name='app-views'),
    
]

octopusdash_urls = [
    path('',octopusdash_views.dashboard_view,name='octopusdash-dashboard'),
    path("login/",octopusdash_views.login_view,name='octopusdash-login'),
    path('users/',octopusdash_views.UserListView.as_view(),name='octopusdash-users-list'),
    path('users/update/<int:pk>/',octopusdash_views.UpdateUserView.as_view(),name='octopusdash-update-user')
]

urlpatterns = [
    path('',include(octopusdash_urls)),
    path("apps/",include(apps_urls))
]

