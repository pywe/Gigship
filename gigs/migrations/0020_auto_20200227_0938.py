# Generated by Django 2.1.4 on 2020-02-27 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0019_auto_20200226_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='category',
        ),
        migrations.AddField(
            model_name='service',
            name='categories',
            field=models.ManyToManyField(to='gigs.Skill'),
        ),
    ]
