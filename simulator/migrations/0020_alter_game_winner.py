# Generated by Django 3.2 on 2021-05-04 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0019_alter_game_weeks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='simulator.houseguest'),
        ),
    ]
