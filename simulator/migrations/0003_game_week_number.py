# Generated by Django 3.2.4 on 2021-07-24 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0002_auto_20210724_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='week_number',
            field=models.IntegerField(default=1),
        ),
    ]