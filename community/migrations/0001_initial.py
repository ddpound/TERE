# Generated by Django 3.0 on 2019-12-04 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('ID', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('PassWords', models.CharField(max_length=20)),
                ('Name', models.CharField(max_length=20)),
                ('Identifier', models.CharField(max_length=20)),
                ('Grade', models.CharField(max_length=20)),
            ],
        ),
    ]
