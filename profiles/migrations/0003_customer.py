# Generated by Django 4.0.4 on 2022-04-24 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.organization')),
            ],
        ),
    ]
