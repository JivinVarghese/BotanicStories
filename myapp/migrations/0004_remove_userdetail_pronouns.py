# Generated by Django 5.0.6 on 2024-07-17 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_userdetail_pronouns'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetail',
            name='pronouns',
        ),
    ]
