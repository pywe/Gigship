# Generated by Django 2.2.3 on 2020-01-19 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gigs', '0005_auto_20200119_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='resume',
            name='months_experience',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resume',
            name='profession',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resume',
            name='years_experience',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ResumeSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='skills', to='gigs.Resume')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('position', models.CharField(max_length=100, null=True)),
                ('period_from', models.DateField(null=True)),
                ('period_to', models.DateField(null=True)),
                ('resume', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='experiences', to='gigs.Resume')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=100, null=True)),
                ('qualification', models.CharField(max_length=100, null=True)),
                ('period_from', models.DateField(null=True)),
                ('period_to', models.DateField(null=True)),
                ('resume', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='education', to='gigs.Resume')),
            ],
        ),
    ]