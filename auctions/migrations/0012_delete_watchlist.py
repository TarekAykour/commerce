# Generated by Django 4.0.5 on 2022-09-13 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_watchlist_listing_watchlist_listing'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]