# Generated by Django 2.2.3 on 2020-02-27 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200227_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_type',
        ),
    ]
