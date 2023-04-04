# Generated by Django 3.2.18 on 2023-04-03 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('file', models.FileField(upload_to='stories/')),
            ],
            options={
                'verbose_name': 'Story',
                'verbose_name_plural': 'Story',
            },
        ),
    ]
