![Logo](static/od/logo/128.svg)
# OctopusDash

OctopusDash is a modern, open-source Django admin dashboard designed with **a beautiful UI**, **powerful filtering**, and **granular permission control** — crafted for developers and teams seeking more flexibility, clarity, and extensibility beyond the default Django admin.

> ⚡ **OctopusDash is actively under development!** Contributions, feedback, and feature requests are always welcome.

---

## 📸 Screenshots

![Screenshot](screenshots/Screenshot%20from%202025-06-28%2020-48-24.png)
![Screenshot](screenshots/Screenshot%20from%202025-06-28%2020-48-45.png)
![Screenshot](screenshots/Screenshot%20from%202025-06-28%2020-51-42.png)

---

## ✨ Key Features

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

🧩 **Coming Soon**  
- Plugin system to extend dashboards with new features  
- Widget support for custom charts, stats, and data cards  

---

## ❓ Why OctopusDash?

While Django’s default admin is powerful, it often feels limited and outdated when your projects demand:  
- More granular control over user permissions and data visibility  
- Customizable dashboards tailored to real business needs  
- A clean, modern UI that enhances developer and user experience  

OctopusDash addresses these with a fresh design, rich filtering options, and extensible architecture built from the ground up.

---

## 🏗️ How OctopusDash Was Built

Unlike many alternatives, OctopusDash is **not** just a skin or extension on top of Django’s default admin panel. Instead, it’s built **from scratch** to support ambitious features like plugins, custom widgets, auto API generation, and more.

This approach allows us to deeply understand Django’s internals while avoiding the constraints and limitations of the default admin — all without sacrificing Django’s powerful template system and generic views.

---

## 🛠 Installation

> ⚠ Requires Python 3.8+ and Django 4.x+

Install via pip:
```bash
pip install octopusdash
```

Add `octopusdash` to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    'octopusdash',
    # ...
]
```

Include OctopusDash URLs in your project:
```python
from django.urls import path, include

urlpatterns = [
    path('octopusdash/', include('octopusdash.urls')),
    # ...
]
```

Add required middlewares:
```python
MIDDLEWARE = [
    'octopusdash.middlewares.app.ViewErrorHandlerMiddleware',
    'octopusdash.middlewares.authentication.CheckAuthenticationMiddleware',
    # ...
]
```

Configure template context processors:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'octopusdash.context.global_context',
            ],
        },
    },
]
```

Add OctopusDash settings:
```python
OCTOPUSDASH = {
    'dashboard_path': '/dashboard',
}
```

---

## 🚀 Quick Start

Example of registering your app and model admin:

```python
from octopusdash.contrib import admin as od_admin
from .models import Post

app = od_admin.AppAdmin('home')

class PostAdmin(od_admin.ModelAdmin):
    model = Post
    list_display = ['title', 'content', 'is_active', 'author']

app.register_to_admin_panel(model_admin=PostAdmin)
```

Visit `/dashboard/` after running the server.

---

## ⚡ Custom Actions

Define custom actions on your model admin:

```python
class PostAdmin(od_admin.ModelAdmin):
    model = Post
    actions = ['set_to_active']

    @od_admin.action(desc="Change post state to active.")
    def set_to_active(self, queryset):
        for post in queryset:
            post.is_active = True
```

---

## ✏️ Inline Edit Support

Edit objects directly in the table using **Django formsets**:

```python
class PostAdmin(od_admin.ModelAdmin):
    model = Post
    list_display = ('title', 'content', 'author', 'is_active')
    list_editable = ('title', 'author', 'is_active')
```

**Note:** Fields in `list_editable` must be included in `list_display`.

---

## ⚙️ ModelAdmin Attributes

- `manager`: DashboardModelManager instance
- `model`: Django model
- `list_display`: fields to display
- `list_editable`: fields editable inline
- `search_fields`: fields to search
- `filter_fields`: fields to filter
- `readonly_fields`: non-editable fields
- `form_fields`: fields in create/update view (`'__all__'` by default)

> **Note:** Do not override methods in `ModelAdmin` as it follows a specific internal pattern.

---

## 📖 Documentation & Support

Documentation is in progress! Explore the code, open issues, and join the discussion.

---

## 🤝 Contributing

OctopusDash is open-source under the MIT license.  
Contributions, feature requests, and bug reports are welcome.  
Please ⭐ star the repo if you find it useful!

---

Made by [husseinnaeemsec](https://github.com/husseinnaeemsec)

---