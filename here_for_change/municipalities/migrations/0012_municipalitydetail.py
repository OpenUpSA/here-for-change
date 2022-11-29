# Generated by Django 3.2.15 on 2022-11-29 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('municipalities', '0011_auto_20221109_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='MunicipalityDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('field_name', models.CharField(max_length=90)),
                ('field_type', models.CharField(choices=[('string', 'String'), ('int', 'Integer'), ('float', 'Float'), ('json', 'Json'), ('date', 'Date'), ('email', 'Email'), ('phone', 'Phone')], default='string', max_length=40)),
                ('field_value', models.CharField(max_length=90)),
                ('stage', models.CharField(choices=[('staging', 'Staging version'), ('production', 'Production version')], default='staging', max_length=40)),
                ('feedback', models.JSONField(blank=True, null=True)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipalities.municipality')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
