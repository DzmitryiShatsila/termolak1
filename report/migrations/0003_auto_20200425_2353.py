# Generated by Django 3.0.5 on 2020-04-25 20:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_auto_20200425_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
