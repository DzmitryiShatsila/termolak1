# Generated by Django 3.0.5 on 2020-05-24 22:40

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import report.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cases',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('case_code', models.CharField(max_length=200)),
                ('images', models.CharField(choices=[('ct', 'CT'), ('mri', 'MRI')], default='ct', max_length=3)),
                ('case', models.CharField(choices=[('s', 'Standard'), ('o', 'MyOsteotomy')], default='s', max_length=1)),
                ('product', models.CharField(choices=[('spine', 'Spine'), ('knee', 'Knee'), ('hip', 'Hip'), ('shoulder', 'Shoulder'), ('forearm', 'Forearm'), ('wrist', 'Wrist'), ('ankle', 'Ankle')], max_length=30)),
                ('software', models.CharField(choices=[('mimics', 'Mimics'), ('avizo', 'Avizo')], max_length=10)),
                ('procedure', models.CharField(choices=[('rec', 'Reconstruction'), ('check', 'Control')], max_length=10)),
                ('time', models.IntegerField(validators=[report.models.validate_time])),
                ('author', models.ForeignKey(default=django.contrib.auth.models.User, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-created'],
            },
        ),
    ]
