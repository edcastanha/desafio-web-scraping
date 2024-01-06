# Generated by Django 4.2.7 on 2024-01-06 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InformacaoAlvo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('url_alvo', models.URLField()),
                ('codigo_acesso', models.CharField(max_length=12)),
                ('status', models.CharField(choices=[('Aguardando', 'Aguardando'), ('Finalizado', 'Finalizado'), ('Error', 'Error')], default='Aguardando', max_length=10)),
                ('url_arquivo', models.URLField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webScrappingTask.cliente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tarefas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('tarefa', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('data_inicio', models.DateTimeField(auto_now_add=True)),
                ('data_fim', models.DateTimeField(blank=True, null=True)),
                ('id_informacao_alvo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webScrappingTask.informacaoalvo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
