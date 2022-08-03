# Generated by Django 3.1.14 on 2022-08-03 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('municipality_code', models.CharField(max_length=6, unique=True)),
                ('municipality_type', models.CharField(choices=[('Metropolitan', 'Metro'), ('District', 'District'), ('Local', 'Local')], max_length=25)),
                ('province', models.CharField(choices=[('EasternCape', 'Eastern Cape'), ('Freestate', 'Fs'), ('Gauteng', 'Gp'), ('KwaZuluNatal', 'KwaZulu-Natal'), ('Limpopo', 'Lp'), ('Mpumalanga', 'Mp'), ('NorthernCape', 'Northern Cape'), ('NorthWest', 'North West'), ('WesternCape', 'Western Cape')], max_length=25)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipalities.municipality')),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
