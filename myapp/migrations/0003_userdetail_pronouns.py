# Generated by Django 5.0.6 on 2024-07-16 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_comment_created_time_comment_updated_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='pronouns',
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
