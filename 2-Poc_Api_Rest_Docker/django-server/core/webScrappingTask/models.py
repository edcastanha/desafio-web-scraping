from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.helpers.tasks import run_webScrappingTask
from core.helpers.loggingMe import logger
import json

# Classe base para todos os modelos, contendo informações de data de cadastro e atualização
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TargetSiteData(BaseModel):
    CHOICE_STATUS = (
        ("A", "Aguardando"),
        ("P", "Processando"),
        ("F", "Finalizado"),
        ("E", "Error"),
    )
    target_url = models.URLField()
    codes = models.JSONField(blank=False)
    status_process = models.CharField(
        max_length=1, choices=CHOICE_STATUS, default="A"
    )
    url_file = models.URLField(blank=True) # URL de arquivo: bucket S3, link de download ou FTP

    def __str__(self):
        return f"Código: {self.access_code}, URL: {self.target_url}, STATUS: {self.status_process}"

class TaskProcessing(BaseModel):
    id_target = models.ForeignKey(TargetSiteData, on_delete=models.CASCADE)
    access_code = models.IntegerField(blank=False)
    processing = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Tarefa: {self.id_target}, Status: {self.processing}"

# Signal para executar uma tarefa após salvar uma nova instância de TargetSiteData
@receiver(post_save, sender=TargetSiteData)
def task_pre_save(sender, instance, created, **kwargs):
    if created:
        logger.debug(f':: Models - task_pre_save:: created {type(instance).__name__}')
        try:
            # Itera sobre os códigos de acesso e cria uma nova TaskProcessing
            for access_code in instance.codes:
                task_processing = TaskProcessing.objects.create(
                    id_target=instance,
                    access_code=access_code,
                    processing=False
                )

                # Serializa a instância para um formato JSON incluindo o código de acesso
                serialized_instance = json.dumps({
                    "id": instance.pk,
                    "codigo": access_code,
                    "url": instance.target_url,
                    "task_id": task_processing.pk
                })
                logger.debug(f':: Models - task_pre_save:: DATA={serialized_instance}')

                # Chama a função para executar a tarefa de web scraping passando a instância
                run_webScrappingTask(serialized_instance) 
                
        except Exception as e:
            error_message = f"Uma exceção do tipo {type(e).__name__} ocorreu com a mensagem: {str(e)}"
            logger.error(f'<:: Models - task_pre_save:: Exception: {error_message}')