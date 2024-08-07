# Generated by Django 5.0.3 on 2024-06-16 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_choice', models.CharField(max_length=255)),
                ('media_choice', models.CharField(max_length=255)),
                ('user_input', models.TextField()),
                ('generated_response', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
