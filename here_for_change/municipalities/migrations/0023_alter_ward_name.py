# Generated by Django 3.2.16 on 2023-01-24 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipalities', '0022_alter_municipality_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ward',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]