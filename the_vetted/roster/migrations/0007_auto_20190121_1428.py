# Generated by Django 2.1.5 on 2019-01-21 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roster', '0006_user_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='in_roster',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invite',
            name='status',
            field=models.CharField(default='Inactive', max_length=20),
        ),
    ]
