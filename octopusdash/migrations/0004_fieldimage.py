# Generated by Django 5.2 on 2025-05-02 08:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('octopusdash', '0003_field_age_field_choice_field_field_datefield_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='octopusdash.field')),
            ],
        ),
    ]
