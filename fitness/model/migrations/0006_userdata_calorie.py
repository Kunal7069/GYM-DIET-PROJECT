# Generated by Django 4.2.4 on 2024-07-03 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0005_food'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='calorie',
            field=models.FloatField(default=0),
        ),
    ]
