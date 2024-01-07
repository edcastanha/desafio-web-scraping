from django.contrib import admin
from core.webScrappingTask.models import Clientes, Tarefas, InformacaoAlvo


admin.site.register(Clientes)
admin.site.register(Tarefas)
admin.site.register(InformacaoAlvo)