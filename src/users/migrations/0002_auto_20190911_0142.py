# Generated by Django 2.2.5 on 2019-09-11 01:42

from django.db import migrations, models
import helpers.date_helpers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_level',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='changed',
            field=models.DateTimeField(default=helpers.date_helpers.get_current_utc_datetime),
        ),
        migrations.AlterField(
            model_name='user',
            name='created',
            field=models.DateTimeField(default=helpers.date_helpers.get_current_utc_datetime),
        ),
    ]
