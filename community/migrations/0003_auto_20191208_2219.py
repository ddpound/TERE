# Generated by Django 3.0 on 2019-12-08 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_board_boardcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='id',
        ),
        migrations.AlterField(
            model_name='board',
            name='b_purpose',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='boardcategory',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]