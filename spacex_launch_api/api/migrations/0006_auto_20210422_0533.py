# Generated by Django 3.2 on 2021-04-22 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_launch_launch_date_unix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launch',
            name='launch_site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.launchsite'),
        ),
        migrations.AlterField(
            model_name='launch',
            name='rocket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.rocket'),
        ),
        migrations.AlterField(
            model_name='rocket',
            name='payloads',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.payload'),
        ),
    ]
