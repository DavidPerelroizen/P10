# Generated by Django 4.0.3 on 2022-05-06 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('softdeskapp', '0003_remove_projects_project_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='comment_id',
        ),
    ]
