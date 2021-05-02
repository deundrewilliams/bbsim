# Generated by Django 3.2 on 2021-05-02 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0012_remove_vetoceremony_final_nominees'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvictionCeremony',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hoh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hoh_eviction', to='simulator.houseguest')),
                ('nominees', models.ManyToManyField(related_name='noms_eviction', to='simulator.Houseguest')),
                ('participants', models.ManyToManyField(related_name='parts_eviction', to='simulator.Houseguest')),
            ],
        ),
    ]