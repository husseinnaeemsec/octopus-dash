from django.views.generic import TemplateView
from..core import DashboardApp
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.views import View
from ..forms import NewUserModelForm  # Import the form
from django.utils import timezone
from django.db import connections
from django.db.utils import OperationalError
import psutil
import time
from datetime import datetime
import math
import shutil
from ..models import get_website_stats
from .users import NewUserView

User = get_user_model()

class Login(TemplateView):
    
    template_name = 'authentication/login.html'


class DashboardView(TemplateView):
    template_name = 'web/overview.html'

    def check_database(self):
        try:
            start_time = time.time()
            # Try to connect to the database and run a simple query
            connections['default'].cursor()
            query_time = time.time() - start_time  # Time taken for the query
            return {
                'status': 'Healthy',
                'query_time': round(query_time, 3)  # Round to 3 decimal places
            }
        except OperationalError:
            return {
                'status': 'Unhealthy',
                'query_time': None
            }

    def check_disk_space(self):
        total, used, free = shutil.disk_usage("/")
        free_space_percentage = (free / total) * 100
        return free_space_percentage > 20  # Healthy if >20%

    def check_system_resources(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_percent = memory_info.percent
        return cpu_percent < 80 and memory_percent < 80  # Healthy if less than 80% usage

    def check_system_health(self):
        database_health = self.check_database()
        disk_health = self.check_disk_space()
        resources_health = self.check_system_resources()

        if database_health and disk_health and resources_health:
            return "Healthy"
        else:
            return "Unhealthy"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Existing app and user counts
        context['apps_count'] = DashboardApp.get_apps_count()
        context['users_count'] = User.objects.count()

        # Active Sessions count
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        context['active_sessions_count'] = active_sessions.count()

        # System Health Status
        context['system_status'] = self.check_system_health()

        # CPU Usage
        context['cpu_usage'] = psutil.cpu_percent(interval=1)

        # Memory Usage
        memory = psutil.virtual_memory()
        context['memory_usage_percent'] = memory.percent
        context['memory_usage_available'] = math.ceil(memory.available / (1024 * 1024))  # in MB

        # Disk Space
        disk = psutil.disk_usage('/')
        context['disk_free_gb'] = math.ceil(disk.free / (1024 * 1024 * 1024))  # in GB
        context['disk_total_gb'] = math.ceil(disk.total / (1024 * 1024 * 1024))  # in GB

        # Database Health (Using check_database method)
        context['database_health'] = self.check_database()
        context['website_status'] = get_website_stats()

        # System Uptime
        uptime_seconds = psutil.boot_time()
        boot_time = timezone.make_aware(datetime.fromtimestamp(uptime_seconds))
        uptime = timezone.now() - boot_time
        context['system_uptime'] = str(uptime).split('.')[0]  # Format it as a human-readable string

        return context

    def post(self, *args, **kwargs):
        return super().get(*args, **kwargs)



class UserManagement(View):
    template_name = 'web/user_management.html'

    def get(self, request, *args, **kwargs):
        form = NewUserModelForm()
        context = {
            'groups_count': Group.objects.count(),
            'groups': Group.objects.all(),
            'users': User.objects.all(),
            'admins_count': User.objects.filter(is_superuser=True).count(),
            'form': form,  # Include the form in the context
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = NewUserModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-management')  # Redirect to the same page after successful submission

        # If form is not valid, re-render the page with errors
        context = {
            'groups_count': Group.objects.count(),
            'groups': Group.objects.all(),
            'users': User.objects.all(),
            'admins_count': User.objects.filter(is_superuser=True).count(),
            'form': form,
        }
        return render(request, self.template_name, context)

