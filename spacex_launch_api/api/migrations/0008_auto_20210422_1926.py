# Generated by Django 3.2 on 2021-04-22 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210422_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rocket',
            name='launch',
        ),
        migrations.AddField(
            model_name='launch',
            name='rocket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.rocket'),
        ),
    ]
