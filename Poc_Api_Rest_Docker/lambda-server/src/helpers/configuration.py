class Configuration:
    
    # ---------------------------------- RabbitMQ ----------------------------------
    RMQ_SERVER = 'broker-server'
    RMQ_PORT = 5672
    RMQ_USER = 'guest'
    RMQ_PASS = 'guest'
    RMQ_EXCHANGE = 'secedu'

    RMQ_QUEUE_PUBLISHIR = 'tasks'
    RMQ_ROUTE_KEY = 'init'


    DATABASE_URL = 'postgres-server'
    DATABASE_USER = 'postgres'
    DATABASE_PASS = 'fake123'
    DATABASE_NAME = simpleDB
    DATABASE_PORT = 5432
     
    UPDATE_QUERY = """
        UPDATE 
            webScrappingTask_InformacaoAlvo 
        SET 
            status = %s WHERE id = %s
    """
    INSER_QUERY = """
        INSERT INTO webScrappingTask_tarefas (
            id_informacao_alvo_id, 
            tarefa, 
            status, 
            data_inicio, 
            data_fim
          )
        VALUES (
           %s, %s, %s, %s, %s, %s, %s
           )
    """
