from ..registry.app_registry import registry


class ViewRegistry:
    _registry = {}
    
    
    def register_view(self,page,view):
        
        if not self._registry.get(view):
            self._registry[page] = {
                'view':view,
                'page_class':page
            }