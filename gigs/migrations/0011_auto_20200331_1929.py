# Generated by Django 2.2.3 on 2020-03-31 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0010_auto_20200331_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='GigPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(help_text='Basic,Standard,Premium', max_length=10, null=True)),
                ('delivery_time', models.IntegerField(default=1, help_text='Number of days')),
                ('revision', models.IntegerField(default=1, help_text='How many times will you review?')),
                ('gig', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plans', to='gigs.Gig')),
            ],
        ),
    ]
