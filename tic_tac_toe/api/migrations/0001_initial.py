# Generated by Django 3.1.7 on 2021-04-07 21:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('player', models.CharField(choices=[('X', 'X'), ('O', 'O')], default='X', max_length=1)),
                ('opponent_level', models.CharField(choices=[('R', 'Random'), ('B', 'Best')], default='B', max_length=1)),
                ('board', models.JSONField()),
            ],
        ),
    ]
