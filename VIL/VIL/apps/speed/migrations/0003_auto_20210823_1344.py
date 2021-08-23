# Generated by Django 3.2.4 on 2021-08-23 10:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speed', '0002_alter_measurement_testdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mstats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='measurement',
            name='rec',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='testdata',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 23, 13, 44, 17, 767973)),
        ),
    ]