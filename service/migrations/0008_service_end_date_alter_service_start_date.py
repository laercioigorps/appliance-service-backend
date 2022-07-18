# Generated by Django 4.0.4 on 2022-07-14 22:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_alter_service_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='start_date',
            field=models.DateField(default=datetime.date(2022, 7, 14)),
        ),
    ]