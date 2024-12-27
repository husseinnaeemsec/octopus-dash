from django.apps import apps
from django.core.signals import setting_changed
from django.dispatch import receiver


# This class is to better access Dictonary objects
class DictToObject:
    def __init__(self,object:dict):
        for key,value in object.items():
            if not hasattr(self,key):
                setattr(self, key, value)
                
    
    def get_attr(self,key):
        return getattr(self, key, None)

class ObjectToDict(object):
    
    def __init__(self, obj):
        self.__dict__ = obj.__dict__
    
    def to_dict(self):
        return self.__dict__
    


