# Generated by Django 3.0.3 on 2020-04-01 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0009_delete_gigplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='GigPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Basic,Standard,Premium', max_length=10, null=True)),
                ('description', models.TextField(null=True)),
                ('delivery_time', models.IntegerField(default=1, help_text='Number of days')),
                ('revision', models.IntegerField(default=1, help_text='How many times will you review?')),
                ('price', models.FloatField(default=0.0)),
                ('gig', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plans', to='gigs.Gig')),
            ],
        ),
    ]
