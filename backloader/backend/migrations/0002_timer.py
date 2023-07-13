# Generated by Django 4.1.3 on 2023-07-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timer_id', models.TextField()),
                ('interval', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_run', models.DateTimeField()),
            ],
        ),
    ]
