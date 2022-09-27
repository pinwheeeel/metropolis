# Generated by Django 3.2.15 on 2022-09-27 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_auto_20220308_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='status',
            field=models.CharField(choices=[('d', 'Draft'), ('p', 'Pending Approval'), ('a', 'Approved'), ('r', 'Rejected')], default='p', max_length=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='graduating_year',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(None, 'Does not apply'), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026)], null=True),
        ),
    ]
