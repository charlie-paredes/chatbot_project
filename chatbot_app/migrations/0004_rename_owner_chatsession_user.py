# Generated by Django 5.0.3 on 2024-07-15 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0003_chatsession_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatsession',
            old_name='owner',
            new_name='user',
        ),
    ]
