# Generated by Django 2.2.3 on 2020-04-03 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0017_quote_request'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('accounts', '0009_customuser_categories'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Shipper',
        ),
    ]