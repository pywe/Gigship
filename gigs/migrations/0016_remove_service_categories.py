# Generated by Django 2.2.3 on 2020-02-27 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0015_service_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='categories',
        ),
    ]
