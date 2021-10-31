# Generated by Django 3.2.8 on 2021-10-31 14:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eegtest', '0003_testresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Status'),
        ),
    ]