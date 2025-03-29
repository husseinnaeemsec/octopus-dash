from django.contrib import admin
from octopusDash.models import Post,Poll,AppConfig,ResourcesAccessLog,DashboardSetting
from .apps import OctopusdashConfig
from .core.registry import DashboardApp,ModelAdmin



app = DashboardApp(OctopusdashConfig,enable_res_middleware=True)

class PostAdmin(ModelAdmin):
    display_fields = ['id','title']

app.register(Post,PostAdmin)
app.register(Poll)
app.register(DashboardSetting)

admin.site.register(Post)

admin.site.register(AppConfig)
admin.site.register(ResourcesAccessLog)