from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.db.models import JSONField as NativeJSONField  # Preferred
from datetime import timedelta

class Post(models.Model):
    # Basics
    title = models.CharField(max_length=150, blank=True)  # CharField
    likes = models.IntegerField(default=0, blank=True)    # IntegerField

    # Dates & Times
    updated_at = models.DateField(auto_now=True, blank=True)             # DateField
    publish_time = models.TimeField(auto_now_add=True, blank=True, null=True)  # TimeField
    published_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # DateTimeField
    
    # Using IntegerField to store duration in seconds (for SQLite)
    duration = models.IntegerField(default=10, blank=True)  # Duration in seconds

    # Text & Validation
    content = models.TextField(max_length=5000, blank=True)              # TextField
    email = models.EmailField(null=True, blank=True)                     # EmailField
    website = models.URLField(blank=True, null=True)                     # URLField
    slug = models.SlugField(unique=True, blank=True)                     # SlugField

    # Files
    file = models.FileField(upload_to="uploads/", null=True, blank=True)     # FileField
    image = models.ImageField(upload_to="images/", null=True, blank=True)    # ImageField

    # Boolean
    is_published = models.BooleanField(default=False, blank=True)            # BooleanField

    # Choices
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    )
    status_db = models.CharField(choices=STATUS_CHOICES, max_length=10, blank=True)

    # Multiple Choice
    TAG_CHOICES = (
        ("django", "Django"),
        ("python", "Python"),
        ("ai", "AI"),
    )

    # Regex Field (via validator)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        help_text="Phone number must be in the format: '+999999999'",
        blank=True
    )

    # Misc
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # GenericIPAddressField
    file_path = models.FilePathField(path=r"/tmp", match=r".*\.txt$", blank=True, null=True)  # FilePathField
    rating = models.FloatField(default=0.0, blank=True)               # FloatField
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)  # DecimalField
    json_data = NativeJSONField(default=dict, blank=True, null=True)         # JSONField

    # UUIDField with default to generate unique UUIDs
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'posts'


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='books')
