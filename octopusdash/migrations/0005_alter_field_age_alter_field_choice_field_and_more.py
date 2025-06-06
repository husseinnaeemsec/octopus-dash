# Generated by Django 5.2 on 2025-05-02 09:50

import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('octopusdash', '0004_fieldimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='age',
            field=models.IntegerField(blank=True, help_text='Only 18+ are allowed to register in this website ', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='choice_field',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default='male', help_text='Another radio group select ', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='datefield',
            field=models.DateField(blank=True, help_text='Inter any valid date', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='datetimefield',
            field=models.DateTimeField(blank=True, help_text='Local Date and Time field', null=True, verbose_name='Date Time Field'),
        ),
        migrations.AlterField(
            model_name='field',
            name='desc',
            field=models.TextField(blank=True, help_text='Short descirption With Rich text editor', max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='duration',
            field=models.DurationField(blank=True, help_text='This field is only works with PostgreSQL ', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='email',
            field=models.EmailField(blank=True, help_text='Any active email', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='file_upload',
            field=models.FileField(blank=True, help_text='Make sure that the file format is one of these (image/png,jpg,svg , PDF , DOC )', null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='field',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], help_text='Choice Gender', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='image_upload',
            field=models.ImageField(blank=True, help_text='Only images are allowed ', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='field',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, help_text='Wither this Filed is active or not ', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='json_data',
            field=models.JSONField(blank=True, default=dict, help_text='JSON Formated data', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(blank=True, help_text='Name of the field', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='number',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='Any positive number', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Price with floating points', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='slug',
            field=models.SlugField(blank=True, help_text='SEO optamized url ex: (How to setup a Django Project. ) ', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='timefield',
            field=models.TimeField(blank=True, help_text='Time filed', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='url',
            field=models.URLField(blank=True, help_text='Any valid URL that starts with (www,https,etc)', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='Select users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='field',
            name='uuid_field',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='UUID Field auto-created', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='weight',
            field=models.FloatField(blank=True, help_text='Float field', null=True),
        ),
    ]
