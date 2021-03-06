# Generated by Django 2.1.4 on 2020-03-30 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('message_file', models.FileField(null=True, upload_to='static/messages/')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='accounts.Message')),
            ],
        ),
    ]
