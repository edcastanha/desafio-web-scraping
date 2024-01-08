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

class InformacaoAlvo(BaseModel):
    # Opções para o campo 'status'
    CHOICE_STATUS = (
        ("Aguardando", "Aguardando"),
        ("Processando", "Processando"),
        ("Finalizado", "Finalizado"),
        ("Error", "Error"),
    )
    token = models.CharField(max_length=100, unique=True)
    url_alvo = models.URLField()
    codigo_acesso = models.CharField(blank=False)
    status = models.CharField(
        max_length=11, choices=CHOICE_STATUS, default="Aguardando"
    )
    url_arquivo = (
        models.URLField()
    )  # URL de arquivo: bucket S3, link de download ou FTP

    def __str__(self):
        return f"Código: {self.codigo_acesso}, URL: {self.url_alvo}"



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
def task_pre_save(sender, instance, created, **kwargs):
    # Verifica se a instância foi criada (created=True) e executa a tarefa de pre-salva se sim.
    if created:
        try:
            task_instance = instance

            # Chama a função para executar a tarefa de web scraping passando a instância
            run_webScrappingTask(task_instance)
            
        except Exception as e:
            # Trate o erro de acordo com a sua lógica
            # Por exemplo, você pode registrar o erro em um arquivo de log
            print(f"Erro ao executar a tarefa de web scraping: {e}")