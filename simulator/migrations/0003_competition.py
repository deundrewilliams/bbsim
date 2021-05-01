# Generated by Django 3.2 on 2021-05-01 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0002_auto_20210501_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_type', models.IntegerField(choices=[(1, 'HOH'), (2, 'POV')])),
                ('participants', models.ManyToManyField(to='simulator.Houseguest')),
            ],
        ),
    ]
