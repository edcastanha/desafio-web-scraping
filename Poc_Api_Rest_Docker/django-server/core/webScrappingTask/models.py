from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from core.webScrappingTask.tasks import run_webScrappingTask

class baseModel(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Modelo para salvar informações sobre as URLs de destino, códigos de acesso, status e caminhos de arquivos
class InformacaoAlvo(baseModel):
    CHOICE_STATUS = ( # Nao usarei abreviacao
        ('Aguardando', 'Aguardando'), 
        ('Finalizado', 'Finalizado'),
        ('Error', 'Error'),
        ) 
    token = models.CharField(max_length=100, unique=True)
    url_alvo = models.URLField()
    codigo_acesso = models.CharField(max_length=12, blank=False, )
    status = models.CharField(max_length=10, choices=CHOICE_STATUS, default='Aguardando')
    url_arquivo = models.URLField()  # link bucket S3, url de download ou ate mesmo um ftp ()

    def __str__(self):
        return f"Codigo: {self.codigo_acesso}, URL: {self.url_alvo}"
    
    def get_data(self):
        return {
            'id': self.id,
            'token': self.token,
            'url_alvo': self.url_alvo,
            'codigo_acesso': self.codigo_acesso,
            'status': self.status,
            'path_arquivo': self.path_arquivo.url,
            'data_atualizado': self.data_atualizacao.strftime("%d/%m/%Y %H:%M:%S"),
        }
    
class Tarefas(baseModel):
    id_informacao_alvo = models.ForeignKey(InformacaoAlvo, on_delete=models.CASCADE)
    tarefa = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Tarefa: {self.tarefa}, Status: {self.status}"

    class Meta:
        # Definir o banco de dados a ser usado pelo modelo Tarefas
        using = 'mysql_db'


@receiver(post_save, sender=InformacaoAlvo)
def tarefa_pre_save(sender, instance, created, **kwargs):
    if created:

        # Criar um dicionário com os dados da instância Tarefas e InformacaoAlvo
        task_data = {
            'id_informacao_alvo': instance.id,
            'tarefa': instance.token,
            'data_inicio': instance.data_cadastro.strftime('%Y-%m-%d %H:%M:%S'),
        }
        # Disparar a tarefa do Celery passando os dados da instância Tarefas e InformacaoAlvo como argumento
        run_webScrappingTask.delay(task_data)
