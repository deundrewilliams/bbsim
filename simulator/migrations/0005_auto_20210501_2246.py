# Generated by Django 3.2 on 2021-05-01 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0004_auto_20210501_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='participants',
            field=models.ManyToManyField(related_name='comp_participants', to='simulator.Houseguest'),
        ),
        migrations.CreateModel(
            name='NominationCeremony',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hoh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulator.houseguest')),
                ('nominees', models.ManyToManyField(default=[], related_name='nominees', to='simulator.Houseguest')),
                ('participants', models.ManyToManyField(related_name='nom_participants', to='simulator.Houseguest')),
            ],
        ),
    ]