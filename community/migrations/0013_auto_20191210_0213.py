# Generated by Django 2.2.6 on 2019-12-09 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0012_auto_20191210_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardcon',
            name='m_WriterID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.MyUser'),
        ),
    ]