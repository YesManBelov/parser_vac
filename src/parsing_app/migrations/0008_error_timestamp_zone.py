# Generated by Django 5.0.1 on 2024-02-09 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsing_app', '0007_alter_error_error_alter_error_url_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='error',
            name='timestamp_zone',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
