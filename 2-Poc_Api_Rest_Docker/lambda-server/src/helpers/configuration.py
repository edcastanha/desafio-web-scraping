class Configuration:
    
    # ---------------------------------- RabbitMQ ----------------------------------
    RMQ_SERVER = 'broker-server'
    RMQ_PORT = 5672
    RMQ_USER = 'fake'
    RMQ_PASS = 'fake123'
    RMQ_EXCHANGE = 'teste'

    RMQ_QUEUE_CONSUMER = 'scrapping'
    RMQ_QUEUE_PUBLISHIR = 'scrapping'
    RMQ_ROUTE_KEY = 'api-django'
