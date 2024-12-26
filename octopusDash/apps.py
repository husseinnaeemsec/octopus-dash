from django.apps import AppConfig


class OctopusdashConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'octopusDash'

    
    
    
    def ready(self):        
        
        
        return super().ready()