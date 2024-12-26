
# OctopusDash

⚠️ **IMPORTANT WARNING** ⚠️

**THIS PROJECT IS CURRENTLY IN DEVELOPMENT AND NOT READY FOR PRODUCTION USE**

This version of OctopusDash contains incomplete features and may cause serious bugs or errors in your Django application. Please DO NOT install it in production environments or critical projects at this time.

**Current Status:**
- Several core features are still under development
- API may change significantly
- Potential stability issues
- Not thoroughly tested in production environments

We recommend:
- Waiting for the official stable release
- Following our GitHub repository for updates
- Testing only in isolated development environments if you wish to explore the features

---



A lightweight, modern Django admin panel alternative that provides an enhanced UI/UX experience using TailwindCSS. OctopusDash offers seamless model management with drag-and-drop capabilities, advanced filtering, and built-in analytics while maintaining simplicity in setup and usage.



## Features

- **Modern UI with TailwindCSS**: Clean, responsive interface with modern design patterns
- **Simple Registration**: One-line model registration with extensive customization options
- **Enhanced Many-to-Many Fields**: Drag-and-drop interface for managing relationships
- **Advanced Search & Filtering**: Custom search functionality with dynamic filters
- **Built-in Analytics**: Website statistics and user activity analysis
- **Secure Access Management**: Built-in middleware for authorization and permission control
- **Lightweight**: Minimal impact on your project's performance
- **Custom Actions**: Enhanced action system with improved UI/UX

## Installation

```bash
pip install octopus-dash
```

Add OctopusDash to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    'octopus_dash',
    'django.contrib.admin',
    # ... other apps
]

# Add the authentication middleware
MIDDLEWARE = [
    # ... other middleware
    'octopus_dash.middleware.OctopusAuthMiddleware',
]
```

## Quick Start

1. Register your models using the simple registration function:

```python
from octopus_dash import octopus_registry
from .models import YourModel

# Basic registration
octopus_registry.register_model(YourModel)

# Registration with customization
octopus_registry.register_model(
    YourModel,
    display_fields=['name', 'created_at', 'status'],
    readonly_fields=['created_at'],
    custom_permissions=['can_approve', 'can_publish'],
    search_fields=['name', 'description']
)
```

2. Add OctopusDash URLs to your urls.py:

```python
from django.urls import path, include

urlpatterns = [
    path('octopus/', include('octopus_dash.urls')),
    # ... other URLs
]
```

## Configuration

Configure OctopusDash in your settings.py:

```python
OCTOPUS_DASH_SETTINGS = {
    'site_title': 'Your Project Dashboard',
    'site_header': 'Project Administration',
    
    # Analytics settings
    'enable_analytics': True,
    'tracking_period_days': 30,
    
    # Authorization settings
    'login_required': True,
    'permission_required': True,
    
    # UI Customization
    'primary_color': '#1e40af',
    'secondary_color': '#3b82f6',
    
    # Search settings
    'search_per_page': 20,
    'enable_quick_search': True
}
```

## Authentication and Permissions

OctopusDash includes a robust permission system:

```python
# Custom permission decorator
from octopus_dash.decorators import octopus_permission_required

@octopus_permission_required('can_view_analytics')
def your_view(request):
    # Your view logic here
    pass
```

## Many-to-Many Field Management

The drag-and-drop interface for many-to-many fields is automatically enabled for registered models. Customize the behavior:

```python
octopus_registry.register_model(
    YourModel,
    m2m_fields={
        'related_items': {
            'searchable': True,
            'order_by': 'name',
            'filter_fields': ['category', 'status']
        }
    }
)
```

## Analytics Integration

Access built-in analytics in your views:

```python
from octopus_dash.analytics import get_site_statistics

def your_dashboard_view(request):
    stats = get_site_statistics()
    return render(request, 'dashboard.html', {'stats': stats})
```

## Custom Actions

Define custom actions with enhanced UI:

```python
from octopus_dash.actions import register_action

@register_action(YourModel)
def publish_items(modeladmin, request, queryset):
    queryset.update(status='published')
publish_items.short_description = 'Publish selected items'
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<!-- ## Support -->

<!-- - Documentation: [Full Documentation](https://octopusdash.readthedocs.io/) -->
<!-- - Issues: [GitHub Issues](https://github.com/octopusdash/octopusdash/issues) -->
<!-- - Community: [Discord Server](https://discord.gg/octopusdash) -->

## Credits

Created and maintained by Hussein Naeem