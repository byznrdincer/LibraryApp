# Generated by Django 5.2.1 on 2025-05-16 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuedbook',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
