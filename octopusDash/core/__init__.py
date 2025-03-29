from .registry import app_registry,DashboardApp,ModelAdmin

def configure_urlpatterns(urlpatterns):
    for app_name,app_data in app_registry.items():
        urlpatterns.extend(app_data.urlpatterns)
        for model_name,model_data in app_data.models.items():
            urlpatterns.extend(model_data.get("model_config").urlpatterns)
    return urlpatterns

