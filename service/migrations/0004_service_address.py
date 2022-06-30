# Generated by Django 4.0.4 on 2022-06-26 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_customer_address'),
        ('service', '0003_alter_service_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.address'),
        ),
    ]