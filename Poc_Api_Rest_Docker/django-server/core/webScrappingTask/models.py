from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.helpers.tasks import run_webScrappingTask
from core.helpers.loggingMe import logger

# Classe base para todos os modelos, contendo informações de data de cadastro e atualização
class BaseModel(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Modelo para salvar informações sobre as URLs de destino, códigos de acesso, status e caminhos de arquivos
class InformacaoAlvo(BaseModel):
    # Opções para o campo 'status'
    CHOICE_STATUS = (
        ('Aguardando', 'Aguardando'), 
        ('Finalizado', 'Finalizado'),
        ('Error', 'Error'),
    ) 
    token = models.CharField(max_length=100, unique=True)
    url_alvo = models.URLField()
    codigo_acesso = models.CharField(max_length=12, blank=False)
    status = models.CharField(max_length=10, choices=CHOICE_STATUS, default='Aguardando')
    url_arquivo = models.URLField()  # URL de arquivo: bucket S3, link de download ou FTP

    def __str__(self):
        return f"Código: {self.codigo_acesso}, URL: {self.url_alvo}"
    
    def get_data(self):
        # Retorna dados formatados para a instância InformacaoAlvo
        return {
            'id': self.id,
            'token': self.token,
            'url_alvo': self.url_alvo,
            'codigo_acesso': self.codigo_acesso,
            'status': self.status,
            'path_arquivo': self.url_arquivo,  # Corrigido para 'url_arquivo'
            'data_atualizado': self.data_atualizacao.strftime("%d/%m/%Y %H:%M:%S"),
        }
    
class Tarefas(BaseModel):
    id_informacao_alvo = models.ForeignKey(InformacaoAlvo, on_delete=models.CASCADE)
    tarefa = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Tarefa: {self.tarefa}, Status: {self.status}"


# Signal para executar uma tarefa após salvar uma nova instância de InformacaoAlvo
@receiver(post_save, sender=InformacaoAlvo)
def tarefa_pre_save(sender, instance, created, **kwargs):
    logger.info(f"Tarefa pre-salva inicializada para {instance}")
    # Verifica se a instância foi criada (created=True) e executa a tarefa de pre-salva se sim.
    if created:
        # Cria um dicionário com os dados da instância Tarefas e InformacaoAlvo
        task_data = {
            'id_informacao_alvo': instance,
            'tarefa': instance.token,
            'data_inicio': instance.data_cadastro.strftime('%Y-%m-%d %H:%M:%S'),
        }
        # Dispara a tarefa do Celery passando os dados das instâncias Tarefas e InformacaoAlvo como argumento
        run_webScrappingTask.delay(task_data)
