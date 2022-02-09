# Generated by Django 3.2.10 on 2022-02-02 22:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_auto_20220202_2200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pubreq',
            options={'verbose_name': 'Request for Pubblishing', 'verbose_name_plural': 'Requests for Pubblishing'},
        ),
        migrations.AddField(
            model_name='pubreq',
            name='request_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
