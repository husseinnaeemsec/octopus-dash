from django.apps.config import AppConfig

class DuplicationError(Exception):
    pass

class Registry:
    
    _apps = {}
    
    
    def register_app(self,app:AppConfig):
        
        if not self._apps.get(app.name):
            self._apps[app.name] = {
                'app':app,
                'models':{}
            }

        else:
            raise DuplicationError("The app %s is already registered" % app.name)
        

    