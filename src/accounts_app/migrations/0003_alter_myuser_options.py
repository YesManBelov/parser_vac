# Generated by Django 5.0.1 on 2024-02-08 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0002_myuser_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
