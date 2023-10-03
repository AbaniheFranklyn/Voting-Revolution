# Generated by Django 4.1.3 on 2023-03-29 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='state',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='votingperiod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PoliticalParty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('party_name', models.CharField(max_length=100)),
                ('party_logo', models.ImageField(upload_to='vote_app/static/images/logos')),
                ('candidate_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.candidatelevel')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.state')),
            ],
        ),
        migrations.CreateModel(
            name='lg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lgs', models.CharField(max_length=200)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.state')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('manifesto', models.TextField()),
                ('political_party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.politicalparty')),
            ],
        ),
    ]