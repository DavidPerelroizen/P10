# Generated by Django 4.0.3 on 2022-05-25 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('softdeskapp', '0009_alter_issues_assignee_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='assignee_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to=settings.AUTH_USER_MODEL),
        ),
    ]
