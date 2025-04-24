import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from faker import Faker

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post  # Replace with your actual app name
from django.utils.text import slugify

fake = Faker()

# Predefined real-world categories
category_names = [
    "Technology", "Health", "Finance", "Travel", "Food",
    "Education", "Lifestyle", "Entertainment", "Sports", "Science"
]

def random_timestamp():
    now = timezone.now()
    delta = timedelta(days=random.randint(0, 60), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return now - delta

# Create or update categories
categories = []
for name in category_names:
    slug = slugify(name)
    timestamp = random_timestamp()
    category, created = Category.objects.get_or_create(name=name, slug=slug)
    category.created_at = timestamp
    category.updated_at = timestamp
    category.save()
    categories.append(category)

print(f"✅ Seeded {len(categories)} realistic categories.")

# Fetch users
users = list(User.objects.all())
if not users:
    print("❌ No users found! Add users before seeding posts.")
    exit()

# Create 35 realistic blog-style posts
posts = []
for i in range(35):
    title = fake.sentence(nb_words=random.randint(4, 8)).rstrip(".")
    content = "\n\n".join([fake.paragraph(nb_sentences=random.randint(3, 6)) for _ in range(random.randint(3, 5))])
    likes = random.randint(0, 250)
    slug = slugify(title)
    author = random.choice(users)
    category = random.choice(categories)
    timestamp = random_timestamp()

    post = Post.objects.create(
        title=title,
        content=content,
        likes=likes,
        slug=slug,
        author=author
    )
    post.created_at = timestamp
    post.updated_at = timestamp
    post.save()

    # You could link to category via a field if one exists (e.g., post.category = category)
    posts.append(post)

print(f"✅ Created {len(posts)} blog-style posts with rich content.")
