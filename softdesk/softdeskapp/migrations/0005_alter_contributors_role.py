# Generated by Django 4.0.3 on 2022-05-09 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('softdeskapp', '0004_remove_comments_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributors',
            name='role',
            field=models.CharField(choices=[('A', 'author'), ('CONTR', 'contributor')], max_length=30),
        ),
    ]