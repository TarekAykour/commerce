# Generated by Django 4.0.5 on 2022-09-13 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_delete_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
