# Generated by Django 3.0 on 2019-12-08 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_auto_20191208_2225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardcategory',
            name='c_name',
        ),
        migrations.AddField(
            model_name='board',
            name='identifier',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AddField(
            model_name='boardcategory',
            name='identifier',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
