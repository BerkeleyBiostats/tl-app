# Generated by Django 2.1.2 on 2018-12-13 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_modelrun_last_heartbeat'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelRunListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(max_length=32)),
                ('backend', models.CharField(blank=True, max_length=32, null=True)),
                ('ghap_username', models.CharField(blank=True, max_length=256, null=True)),
                ('ghap_ip', models.CharField(blank=True, max_length=256, null=True)),
                ('base_url', models.CharField(blank=True, max_length=256, null=True)),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('output_url', models.URLField(blank=True, null=True)),
                ('traceback', models.TextField(blank=True, null=True)),
                ('postprocessing_attempts', models.IntegerField(default=0)),
                ('postprocessing_attempted_at', models.DateTimeField(blank=True, null=True)),
                ('postprocessing_traceback', models.TextField(blank=True, null=True)),
                ('is_batch', models.BooleanField(default=False)),
                ('last_heartbeat', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'core_modelrun',
                'managed': False,
            },
        ),
    ]
