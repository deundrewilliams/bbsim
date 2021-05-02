# Generated by Django 3.2 on 2021-05-02 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0013_evictionceremony'),
    ]

    operations = [
        migrations.AddField(
            model_name='evictionceremony',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='evictionceremony',
            name='evicted',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='evicted_hg', to='simulator.houseguest'),
        ),
    ]