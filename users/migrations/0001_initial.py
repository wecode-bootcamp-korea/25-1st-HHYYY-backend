# Generated by Django 3.2.7 on 2021-10-07 02:09

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
                ('email', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('name', models.CharField(max_length=45, null=True)),
                ('address', models.CharField(max_length=300, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
