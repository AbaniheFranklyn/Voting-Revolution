# Generated by Django 4.1.3 on 2023-04-20 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0015_voting_v_lg_voting_v_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voting',
            name='v_lg',
        ),
        migrations.RemoveField(
            model_name='voting',
            name='v_state',
        ),
    ]