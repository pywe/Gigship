# Generated by Django 2.1.4 on 2020-04-02 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_transaction_r_switch'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='categories',
            field=models.ManyToManyField(to='accounts.GiggerCategory'),
        ),
    ]
