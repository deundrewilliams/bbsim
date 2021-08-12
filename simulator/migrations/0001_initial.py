# Generated by Django 3.2.4 on 2021-08-12 23:14

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('step', models.IntegerField(choices=[(0, 'HOH Competition'), (1, 'Nom Ceremony'), (2, 'POV Competition'), (3, 'Veto Ceremony'), (4, 'Eviction'), (5, 'Finale'), (6, 'Memory Wall')], default=6)),
                ('jury_size', models.IntegerField(default=0)),
                ('week_number', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Houseguest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('immune', models.BooleanField(default=False)),
                ('evicted', models.BooleanField(default=False)),
                ('competition_count', models.IntegerField(default=0)),
                ('nomination_count', models.IntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='simulator.game')),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('vote_count', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, default=list, size=None)),
                ('tied', models.BooleanField(default=False)),
                ('evicted', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evicted_weeks', to='simulator.houseguest')),
                ('final_nominees', models.ManyToManyField(default=[], related_name='final_noms_weeks', to='simulator.Houseguest')),
                ('hoh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weeks', to='simulator.houseguest')),
                ('initial_nominees', models.ManyToManyField(default=[], related_name='initial_noms_weeks', to='simulator.Houseguest')),
                ('pov', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pov_weeks', to='simulator.houseguest')),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=50)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affected_hg', to='simulator.houseguest')),
            ],
        ),
        migrations.AddField(
            model_name='houseguest',
            name='relationships',
            field=models.ManyToManyField(default=[], to='simulator.Relationship'),
        ),
        migrations.AddField(
            model_name='game',
            name='hoh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_hoh', to='simulator.houseguest'),
        ),
        migrations.AddField(
            model_name='game',
            name='jury',
            field=models.ManyToManyField(default=[], related_name='game_jury', to='simulator.Houseguest'),
        ),
        migrations.AddField(
            model_name='game',
            name='nominees',
            field=models.ManyToManyField(default=[], related_name='game_nominees', to='simulator.Houseguest'),
        ),
        migrations.AddField(
            model_name='game',
            name='pov',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_pov', to='simulator.houseguest'),
        ),
        migrations.AddField(
            model_name='game',
            name='prejury',
            field=models.ManyToManyField(default=[], related_name='game_prejury', to='simulator.Houseguest'),
        ),
        migrations.AddField(
            model_name='game',
            name='weeks',
            field=models.ManyToManyField(default=[], related_name='game_weeks', to='simulator.Week'),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_winner', to='simulator.houseguest'),
        ),
    ]
