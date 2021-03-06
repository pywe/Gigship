# Generated by Django 2.1.4 on 2020-03-31 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200331_0810'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gigs', '0003_auto_20200331_0856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.FloatField(default=0.0)),
                ('VAT', models.FloatField(default=0.0)),
                ('commission', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=1)),
                ('review', models.TextField(null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='ServiceFile',
            new_name='GigFile',
        ),
        migrations.AddField(
            model_name='order',
            name='VAT',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='order',
            name='commission',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='order',
            name='date_to_complete',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.RenameModel(
            old_name='Service',
            new_name='Gig',
        ),
        migrations.AddField(
            model_name='rating',
            name='gig',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ratings', to='gigs.Gig'),
        ),
        migrations.AddField(
            model_name='rating',
            name='rated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customization',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customizations', to='gigs.Order'),
        ),
    ]
