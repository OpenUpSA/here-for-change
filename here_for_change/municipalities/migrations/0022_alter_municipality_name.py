# Generated by Django 3.2.16 on 2023-01-24 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipalities', '0021_auto_20230124_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipality',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]