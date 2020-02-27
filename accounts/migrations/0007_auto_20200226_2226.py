# Generated by Django 2.1.4 on 2020-02-26 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0019_auto_20200226_2137'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('accounts', '0006_auto_20200226_2209'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Buyer',
            new_name='Shipper',
        ),
        migrations.AlterModelOptions(
            name='shipper',
            options={'verbose_name': 'Shipper'},
        ),
    ]
