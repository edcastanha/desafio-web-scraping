from django.db import models
from django.core.exceptions import ValidationError


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
            'data_atualizado': self.data_cadastro.strftime("%d/%m/%Y %H:%M:%S"),
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
            'data_atualizado': self.data_cadastro.strftime("%d/%m/%Y %H:%M:%S"),
        }
    
class Tarefas(baseModel):
    id_informacao_alvo = models.ForeignKey(InformacaoAlvo, on_delete=models.CASCADE)
    tarefa = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Tarefa: {self.tarefa}, Status: {self.status}"