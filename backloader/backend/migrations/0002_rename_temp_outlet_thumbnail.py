# Generated by Django 4.2.3 on 2023-07-24 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outlet',
            old_name='temp',
            new_name='thumbnail',
        ),
    ]
