# Arquivo: routers.py

class TarefasRouter:
    """
    Um roteador de banco de dados para o modelo Tarefas.
    Este roteador redireciona operações do modelo Tarefas para o banco de dados MySQL.
    """

    def db_for_read(self, model, **hints):
        """
        Decide o banco de dados para operações de leitura.
        Retorna 'mysql_db' se o modelo for Tarefas, caso contrário, None.
        """
        if model._meta.model_name == 'tarefas':
            return 'mysql_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Decide o banco de dados para operações de escrita.
        Retorna 'mysql_db' se o modelo for Tarefas, caso contrário, None.
        """
        if model._meta.model_name == 'tarefas':
            return 'mysql_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relacionamentos entre diferentes bancos de dados.
        Retorna True se qualquer modelo for Tarefas, caso contrário, None.
        """
        if obj1._meta.model_name == 'tarefas' or obj2._meta.model_name == 'tarefas':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Decide se a migração de um modelo deve ser permitida no banco de dados especificado.
        Retorna True se o modelo for Tarefas e o banco de dados for 'mysql_db', caso contrário, None.
        """
        if model_name == 'tarefas':
            return db == 'mysql_db'
        return None
