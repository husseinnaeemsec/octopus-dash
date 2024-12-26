from django.apps import apps
from django.core.signals import setting_changed
from django.dispatch import receiver

@receiver(setting_changed)
def load_views_on_ready(sender, **kwargs):
    if apps.ready:
        from .url_registry import url_registry
        from octopusDash.core.views import generate_urls_from_registry
        from django.conf import settings
        from django.urls import clear_url_caches

        if hasattr(settings, 'ROOT_URLCONF'):
            import importlib
            root_urlconf = importlib.import_module(settings.ROOT_URLCONF)
            urlpatterns = root_urlconf.urlpatterns

            # Generate URLs from your registry
            urlpatterns += generate_urls_from_registry(url_registry)

            # Clear URL caches to apply changes
            clear_url_caches()