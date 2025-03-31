# Generated by Django 5.1.7 on 2025-03-26 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedEnhance', '0002_uploadedimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedimage',
            name='image_url',
        ),
        migrations.AddField(
            model_name='uploadedimage',
            name='image',
            field=models.ImageField(default=0, upload_to='uploads/'),
            preserve_default=False,
        ),
    ]
