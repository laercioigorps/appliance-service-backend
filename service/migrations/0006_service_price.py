# Generated by Django 4.0.4 on 2022-06-27 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_service_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
