# Generated by Django 4.2.1 on 2023-05-17 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=10)),
            ],
        ),
    ]
