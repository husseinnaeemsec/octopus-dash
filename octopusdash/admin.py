from django.contrib import admin
from .registry import dashboard


def mark_as_published(modeladmin, request, queryset):
    updated = queryset
    modeladmin.message_user(request, f"{updated} post(s) marked as published.")

mark_as_published.short_description = "Mark selected posts as published"
# Register your models here.
from .models import Post,Book

dashboard.register(Post)
dashboard.register(Book)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','content']
    actions = [mark_as_published]