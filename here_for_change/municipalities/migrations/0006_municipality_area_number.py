# Generated by Django 3.2.15 on 2022-09-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipalities', '0005_ward_boundary'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipality',
            name='area_number',
            field=models.IntegerField(null=True),
        ),
    ]
