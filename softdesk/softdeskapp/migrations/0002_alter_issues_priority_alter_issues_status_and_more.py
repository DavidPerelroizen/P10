# Generated by Django 4.0.3 on 2022-05-04 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('softdeskapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='priority',
            field=models.CharField(choices=[('L', 'low'), ('M', 'medium'), ('H', 'high')], max_length=10),
        ),
        migrations.AlterField(
            model_name='issues',
            name='status',
            field=models.CharField(choices=[('T', 'to do'), ('I', 'in progress'), ('F', 'finished')], max_length=10),
        ),
        migrations.AlterField(
            model_name='issues',
            name='tag',
            field=models.CharField(choices=[('B', 'bug'), ('I', 'improvement'), ('T', 'task')], max_length=20),
        ),
        migrations.AlterField(
            model_name='projects',
            name='type',
            field=models.CharField(choices=[('BE', 'back-end'), ('FE', 'front-end'), ('IOS', 'ios'), ('AN', 'android')], max_length=30),
        ),
    ]
