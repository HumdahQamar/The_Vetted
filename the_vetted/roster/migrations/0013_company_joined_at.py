# Generated by Django 2.1.5 on 2019-01-23 08:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('roster', '0012_auto_20190123_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='joined_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
