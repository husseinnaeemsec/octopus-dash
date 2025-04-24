from django.conf import settings as django_settings

default_settings = {
        "INCLUDE_ALL_APPS":False,
        'USER_FORM_FIELDS':[
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'user_permissions',
            'groups',
        ]
    }

try:
    settings = django_settings.OCTOPUSDASH_SETTINGS
except AttributeError:
    settings = default_settings