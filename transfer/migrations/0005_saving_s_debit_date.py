# Generated by Django 4.1.3 on 2022-11-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0004_checking_c_debit_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='saving',
            name='s_debit_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
