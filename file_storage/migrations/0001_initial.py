# Generated by Django 3.1.4 on 2020-12-26 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('file_hash', models.CharField(max_length=64, primary_key=True, serialize=False, unique=True)),
                ('file_path', models.FilePathField(null=True)),
            ],
        ),
    ]
