# Generated by Django 2.1.5 on 2019-01-21 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roster', '0008_auto_20190121_1441'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='using_roster',
            new_name='using_roster_app',
        ),
    ]
