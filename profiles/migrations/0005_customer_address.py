# Generated by Django 4.0.4 on 2022-04-26 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.ManyToManyField(blank=True, to='profiles.address'),
        ),
    ]
