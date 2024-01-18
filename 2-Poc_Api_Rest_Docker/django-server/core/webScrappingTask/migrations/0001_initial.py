# Generated by Django 4.2.7 on 2024-01-16 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TargetSiteData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('target_url', models.URLField()),
                ('codes', models.JSONField()),
                ('status_process', models.CharField(choices=[('A', 'Aguardando'), ('P', 'Processando'), ('F', 'Finalizado'), ('E', 'Error')], default='A', max_length=1)),
                ('url_file', models.URLField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskProcessing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('access_code', models.IntegerField()),
                ('processing', models.BooleanField(default=False)),
                ('id_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webScrappingTask.targetsitedata')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
