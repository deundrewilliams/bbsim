# Generated by Django 3.2 on 2021-05-02 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0014_auto_20210502_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evictionceremony',
            name='evicted',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='evicted_hg', to='simulator.houseguest'),
        ),
    ]
