# Generated by Django 4.0.4 on 2022-07-19 21:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_service_end_date_alter_service_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=70)),
                ('is_conclusive', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='service',
            name='start_date',
            field=models.DateField(default=datetime.date(2022, 7, 19)),
        ),
    ]
