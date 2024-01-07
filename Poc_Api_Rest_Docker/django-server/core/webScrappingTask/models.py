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

# Modelo para salvar informações do cliente, modelo ficticio
class Clientes(baseModel):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    # Adicione outros campos conforme necessário, como telefone, contrato, etc.

    def __str__(self):
        return self.nome
    
    def get_data(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'data_atualizado': self.data_atualizacao.strftime("%d/%m/%Y %H:%M:%S"),
        }


# Modelo para salvar informações sobre as URLs de destino, códigos de acesso, status e caminhos de arquivos
class InformacaoAlvo(baseModel):
    CHOICE_STATUS = ( # Nao usarei abreviacao
        ('Aguardando', 'Aguardando'), 
        ('Finalizado', 'Finalizado'),
        ('Error', 'Error'),
        ) 
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    url_alvo = models.URLField()
    codigo_acesso = models.CharField(max_length=12, blank=False, )
    status = models.CharField(max_length=10, choices=CHOICE_STATUS, default='Aguardando')
    url_arquivo = models.URLField()  # link bucket S3, url de download ou ate mesmo um ftp ()

    def __str__(self):
        return f"Cliente: {self.cliente}, URL: {self.url_alvo}"
    
    def get_data(self):
        return {
            'id': self.id,
            'cliente': self.cliente.nome,
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


@receiver(post_save, sender=Tarefas)
def tarefa_pre_save(sender, instance, created, **kwargs):
    if created or instance.data_inicio != instance.data_fim:
        if instance.data_inicio > timezone.now():
            raise ValueError("A data de início não pode ser no futuro")

        if instance.data_fim and instance.data_fim < instance.data_inicio:
            raise ValueError("A data de término não pode ser antes da data de início")

        # Acessar todos os campos do modelo InformacaoAlvo associado à instância Tarefas
        informacao_alvo = instance.id_informacao_alvo
        informacao_alvo_data = {
            'id': informacao_alvo.id,
            'cliente': informacao_alvo.cliente.nome,
            'url_alvo': informacao_alvo.url_alvo,
            'codigo_acesso': informacao_alvo.codigo_acesso,
            'status': informacao_alvo.status,
            'url_arquivo': informacao_alvo.url_arquivo,
            # Adicione outros campos conforme necessário
        }

        # Criar um dicionário com os dados da instância Tarefas e InformacaoAlvo
        task_data = {
            'tarefas_id': instance.id,
            'tarefa': instance.tarefa,
            'status': instance.status,
            'data_inicio': instance.data_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'data_fim': instance.data_fim.strftime('%Y-%m-%d %H:%M:%S') if instance.data_fim else None,
            'informacao_alvo': informacao_alvo_data,
            # Adicione outros campos conforme necessário
        }
        # Disparar a tarefa do Celery passando os dados da instância Tarefas e InformacaoAlvo como argumento
        run_webScrappingTask.delay(task_data)
