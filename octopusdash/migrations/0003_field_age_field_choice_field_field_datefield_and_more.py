# Generated by Django 5.2 on 2025-05-01 11:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('octopusdash', '0002_field_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='choice_field',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='datefield',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='datetimefield',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date Time Field'),
        ),
        migrations.AddField(
            model_name='field',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='email',
            field=models.EmailField(blank=True, help_text='This is a test email', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='field',
            name='image_upload',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='field',
            name='json_data',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='number',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='timefield',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='uuid_field',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='desc',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
