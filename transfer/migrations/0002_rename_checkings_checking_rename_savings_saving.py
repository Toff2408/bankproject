# Generated by Django 4.1.3 on 2022-11-16 13:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transfer', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Checkings',
            new_name='Checking',
        ),
        migrations.RenameModel(
            old_name='Savings',
            new_name='Saving',
        ),
    ]