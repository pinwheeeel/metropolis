# Generated by Django 3.2.6 on 2021-08-14 23:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_graduating_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='is_approved',
        ),
        migrations.AddField(
            model_name='announcement',
            name='rejection_reason',
            field=models.CharField(blank=True, max_length=140),
        ),
        migrations.AddField(
            model_name='announcement',
            name='status',
            field=models.CharField(choices=[('p', 'Pending Approval'), ('a', 'Approved'), ('r', 'Rejected')], default='p', max_length=1),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='approver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='announcements_approved', to=settings.AUTH_USER_MODEL),
        ),
    ]
