# Generated by Django 3.2 on 2021-04-28 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TAApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='role',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
