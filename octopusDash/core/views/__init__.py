class DynamicView:
    
    
    def __init__(self,model_admin,**kwargs):
        self.model = model_admin.model
        self.model_admin = model_admin
        self.model_name = model_admin.label
        self.app_name = model_admin.app_label
        self.required_pk = False
        self.__view_urls = {}
        
    
    def add_view_url(self,url_text:str,view_url):
        url_key = url_text.replace(" ","_").lower()
        
        if not self.__view_urls.get(url_key):
            self.__view_urls[url_key] = {
                'text':url_text.capitalize(),
                'url':view_url
            }