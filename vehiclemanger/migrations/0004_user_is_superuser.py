# Generated by Django 4.1.2 on 2022-10-21 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiclemanger', '0003_alter_vehiclestab_vehicle_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
