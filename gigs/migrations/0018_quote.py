# Generated by Django 2.2.3 on 2020-04-03 09:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gigs', '0017_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_submitted', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_submitted', models.DateField(auto_now_add=True, null=True)),
                ('time_submitted', models.TimeField(auto_now_add=True, null=True)),
                ('updated', models.BooleanField(default=False)),
                ('time_updated', models.DateTimeField(blank=True, null=True)),
                ('accepted', models.BooleanField(default=False)),
                ('time_accepted', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(help_text='Who created the quote?', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quotes', to='gigs.Request')),
                ('submitted_by', models.ForeignKey(help_text='Who was this quote created for?', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submitted_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
