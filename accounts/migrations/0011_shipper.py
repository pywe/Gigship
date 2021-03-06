# Generated by Django 2.2.3 on 2020-04-03 12:37

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_delete_shipper'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipper',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('referral_token', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'Shipper',
            },
            bases=('accounts.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
