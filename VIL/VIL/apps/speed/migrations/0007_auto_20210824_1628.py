# Generated by Django 3.2.4 on 2021-08-24 13:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speed', '0006_auto_20210824_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='available',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='testdata',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 24, 16, 28, 1, 313683)),
        ),
    ]