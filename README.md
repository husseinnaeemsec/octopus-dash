# OctopusDash

OctopusDash is a modern, open-source Django admin dashboard designed with **a beautiful UI**, **powerful filtering**, and **granular permission control** — crafted for developers and teams seeking more flexibility, clarity, and extensibility beyond the default Django admin.

> ⚡ **OctopusDash is actively under development!** Contributions, feedback, and feature requests are always welcome.

---

## Key Features

**Modern UI & UX**  
- Clean, minimal design powered by TailwindCSS  
- Responsive, intuitive components  
- Smooth navigation optimized for productivity  

**Advanced Filtering & Search**  
- Dynamic filters supporting related fields  
- Full-text search across customizable fields  
- Multi-field filtering for faster, precise data exploration  

**Granular Permission Control**  
- Fine-grained access control by model, action, user, or group  
- Customizable admin classes enabling complex authorization logic  

⚙️ **Extensible & Pluggable**  
- Easily add or override views, templates, and behaviors  
- Designed as a standalone Django app for maximum flexibility  

**Coming Soon**  
- Plugin system to extend dashboards with new features  
- Widget support for custom charts, stats, and data cards  

---

## Why OctopusDash?

While Django’s default admin is powerful, it often feels limited and outdated when your projects demand:  
- More granular control over user permissions and data visibility  
- Customizable dashboards tailored to real business needs  
- A clean, modern UI that enhances developer and user experience  

OctopusDash addresses these with a fresh design, rich filtering options, and extensible architecture built from the ground up.

---

## How OctopusDash Was Built

Unlike many alternatives, OctopusDash is **not** just a skin or extension on top of Django’s default admin panel. Instead, it’s built **from scratch** to support ambitious features like plugins, custom widgets, auto API generation, and more.

This approach allows us to deeply understand Django’s internals while avoiding the constraints and limitations of the default admin — all without sacrificing Django’s powerful template system and generic views.

---

##  Installation

> ⚠ Requires Python 3.8+ and Django 4.x+

Install via pip:
```bash
pip install octopusdash
```

Add `octopusdash` to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'octopusdash',
]
```

Include OctopusDash URLs in your project:
```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('octopusdash/', include('octopusdash.urls')),
]
```

Add required middlewares to your `MIDDLEWARE` list:
```python
MIDDLEWARE = [
    # ...
    'octopusdash.middlewares.app.ViewErrorHandlerMiddleware',
    'octopusdash.middlewares.authentication.CheckAuthenticationMiddleware',
]
```

Configure template context processors to include OctopusDash’s context:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',      # Required for request in templates
                'django.contrib.auth.context_processors.auth',     # Required for auth context
                'django.contrib.messages.context_processors.messages',  # Required for messages
                'octopusdash.context.global_context',               # OctopusDash global context
            ],
        },
    },
]
```

Add OctopusDash settings to your `settings.py`:
```python
OCTOPUSDASH = {
    # This to limit the middlewares logic to this path only 
    'dashboard_path': '/dashboard',
}
```

---

## 🚀 Quick Start

Here’s a minimal example of registering your app and model admin:

```python
# Import OctopusDash admin utilities
from octopusdash.contrib import admin as od_admin

# Import your models
from .models import Post

# Create an app admin (app_label should match your app config)
app = od_admin.AppAdmin('home')

# Define model admin class for your model
class PostAdmin(od_admin.ModelAdmin):
    model = Post
    list_display = [
        'title',
        'content',
        'is_active',
        'author',
    ]

# Register the model admin with your app
app.register_to_admin_panel(model_admin=PostAdmin)
```

Run your server and visit:
```
/dashboard/
```

---

## 📖 Documentation & Support

Documentation is in progress! Meanwhile, feel free to explore the code, open issues, and contribute.

---

## 🤝 Contributing

OctopusDash is open-source under the MIT license.  
Contributions, feature requests, and bug reports are warmly welcome.  
Please consider starring the repo ⭐ and joining the discussion.

---

Made by [husseinnaeemsec](https://github.com/husseinnaeemsec)
---