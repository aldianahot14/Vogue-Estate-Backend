# Generated by Django 5.0.2 on 2024-02-15 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_agent_license_alter_agent_email_alter_client_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='client',
            name='phone',
        ),
    ]
