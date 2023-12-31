class Configuration:
    
    # ---------------------------------- RabbitMQ ----------------------------------
    RMQ_SERVER = 'broker-server'
    RMQ_PORT = 5672
    RMQ_USER = 'fake'
    RMQ_PASS = 'fake123'
    RMQ_EXCHANGE = 'teste'

    RMQ_QUEUE_CONSUMER = 'scrapping'
    RMQ_QUEUE_PUBLISHIR = 'processing'
    RMQ_ROUTE_KEY = 'tasks'


    DATABASE_URL = 'postgres-server'
    DATABASE_USER = 'postgres'
    DATABASE_PASS = 'fake123'
    DATABASE_NAME = 'simpleDB'
    DATABASE_PORT = 5432
     
    UPDATE_QUERY = """
        UPDATE 
            webScrappingTask_informacaoalvo 
        SET 
            status = %s WHERE id = %s
    """
    INSER_QUERY = """
        INSERT INTO webScrappingTask_tarefas (
            tarefa,
            status,
            data_inicio,
            data_fim,
            id_informacao_alvo_id
          )
        VALUES (
           %s, %s, %s, %s, %s
           )
    """
