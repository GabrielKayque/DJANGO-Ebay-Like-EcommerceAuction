# Generated by Django 4.0.4 on 2022-04-26 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_description_alter_listing_imgurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(max_length=400),
        ),
    ]
