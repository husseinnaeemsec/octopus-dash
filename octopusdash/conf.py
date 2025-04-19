from django.conf import settings as django_settings

try:
    settings = django_settings.OCTOPUSDASH_SETTINGS

except AttributeError:
    
    settings = {
        "INCLUDE_ALL_APPS":False
    }