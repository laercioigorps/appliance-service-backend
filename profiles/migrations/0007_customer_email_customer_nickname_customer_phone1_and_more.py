# Generated by Django 4.0.4 on 2022-07-14 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_rename_address_customer_addresses'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='nickname',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone1',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone2',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='profession',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
