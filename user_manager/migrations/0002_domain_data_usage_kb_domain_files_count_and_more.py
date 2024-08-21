# Generated by Django 5.1 on 2024-08-18 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='data_usage_kb',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='domain',
            name='files_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='domain',
            name='requests',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='domain',
            name='visitors',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='current_storage_kb',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='max_storage_mb',
            field=models.IntegerField(default=500),
        ),
    ]
