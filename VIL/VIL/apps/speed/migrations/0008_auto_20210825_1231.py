# Generated by Django 3.2.4 on 2021-08-25 09:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speed', '0007_auto_20210824_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='enddata',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 26, 7, 31, 30, 344639)),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='testdata',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 25, 12, 31, 30, 344639)),
        ),
    ]
