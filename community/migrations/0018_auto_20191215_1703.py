# Generated by Django 3.0 on 2019-12-15 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0017_myuser_sn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='identifier',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='boardcategory',
            name='identifier',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='boardcon',
            name='identifier',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='SN',
            field=models.CharField(max_length=20),
        ),
    ]