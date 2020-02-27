# Generated by Django 2.2.3 on 2020-02-27 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_customuser_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Gigger', 'Gigger'), ('Shipper', 'Shipper')], max_length=20, null=True),
        ),
    ]
