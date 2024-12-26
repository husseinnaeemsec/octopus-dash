
class URLRegistry:
    def __init__(self):
        # Initialize an empty dictionary to store URLs, views grouped by app name
        self.registry = {}
        

    def register_app_url(self, app_name, url_pattern, view):
        
        
        
        """
        Register a URL pattern at the app level with its corresponding view.
        """
        if not self.registry.get(app_name):
            self.registry[app_name] = {
                "app":app_name,
                "views":[{"url": url_pattern, "view": view,'name':app_name}],
                "url":url_pattern,
                'models':[]
            }
        
        

    def register_model_url(self, model, url_pattern, view,name=""):
        app_label = model._meta.app_label.lower()
        from octopusDash.core.views import generate_app_view
        if not self.registry.get(app_label):
            self.registry[app_label] = {
                "app": app_label,
                "views": [{'url':app_label+'/','view':generate_app_view(app_label),'name':app_label}],
                'models':[{'model': model, 'url': url_pattern, 'view': view, 'name': name}]
            }
        
        else:
            self.registry[app_label].get("models").append({'model': model, 'url': url_pattern, 'view': view, 'name': name})
        
    def get_urls_by_app(self):
        """
        Return the registry of URLs grouped by app name, including views.
        """
        return self.registry

    def get_flattened_urls(self):
        """
        Return a flattened list of all registered URLs with their views.
        """
        all_urls = []
        for app_urls in self.registry.values():
            if isinstance(app_urls, list):
                # App-level URLs
                all_urls.extend(app_urls)
            else:
                # Model-level URLs
                for model_urls in app_urls.values():
                    all_urls.extend(model_urls)
        return all_urls
    
                
            


url_registry = URLRegistry()





def generate_urls_from_registry(url_registry):
    from django.urls import path
    urlpatterns = []
        
    for app, models in url_registry.get_urls_by_app().items():
        
        app_views = models.get("views")
        
        for view in app_views:
            urlpatterns.append(path(view.get("url"),view.get("view").as_view(),name=view.get("name"),))
        
        for model_view in models.get("models"):
            
            urlpatterns.append(path(model_view.get("url"),model_view.get("view").as_view(),name=model_view.get("name")))
        
    
    
    return urlpatterns