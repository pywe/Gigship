# Generated by Django 2.2.3 on 2020-01-26 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0014_auto_20200123_0635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='end_price',
        ),
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
