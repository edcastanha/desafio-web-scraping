import os
import psycopg2
from logging_me import logger

class DatabaseConnection:
    """
    Classe responsável pela conexão e operações com o banco de dados PostgreSQL.

    Args:
    - db_url (str): URL do banco de dados.
    - db_user (str): Nome de usuário do banco de dados.
    - db_pass (str): Senha do banco de dados.
    - db_name (str): Nome do banco de dados.
    - db_port (str): Porta do banco de dados.
    """
    def __init__(self, db_url=None, db_user=None, db_pass=None, db_name=None, db_port=None):
        self.db_url = db_url or os.environ.get('DATABASE_URL', 'postgres-server')
        self.db_user = db_user or os.environ.get('DATABASE_USER', 'postgres')
        self.db_pass = db_pass or os.environ.get('DATABASE_PASS', 'fake123')
        self.db_name = db_name or os.environ.get('DATABASE_NAME', 'simpleDB')
        self.db_port = db_port or os.environ.get('DATABASE_PORT', '5432')
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Estabelece a conexão com o banco de dados.
        """
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_pass,
                host=self.db_url,
                port=self.db_port
            )
            self.cursor = self.conn.cursor()
            logger.info(f"<*_ConnectionDB_*> Connection to database established successfully")
        except psycopg2.Error as e:
            logger.error(f"Error connecting to the database: {e}")

    def update(self, query, params=None):
        """
        Executa uma query de atualização (UPDATE) no banco de dados.

        Args:
        - query (str): Query SQL de atualização.
        - params (tuple): Parâmetros para a query (opcional).
        """
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            logger.info(f"<*_ConnectionDB_*> Update query executed successfully")
        except psycopg2.Error as e:
            self.conn.rollback()
            logger.error(f"Error executing update query: {e}")

    def insert(self, query, params=None):
        """
        Executa uma query de inserção (INSERT) no banco de dados.

        Args:
        - query (str): Query SQL de inserção.
        - params (tuple): Parâmetros para a query (opcional).
        """
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            logger.info(f"<*_ConnectionDB_*> Insert query executed successfully")
        except psycopg2.Error as e:
            self.conn.rollback()
            logger.error(f"Error executing insert query: {e}")

    def select(self, query, params=None):
        """
        Executa uma query de seleção (SELECT) no banco de dados e retorna o resultado.

        Args:
        - query (str): Query SQL de seleção.
        - params (tuple): Parâmetros para a query (opcional).

        Returns:
        - result (list): Resultado da query de seleção.
        """
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except psycopg2.Error as e:
            logger.error(f"Error executing select query: {e}")

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        logger.info(f"<*_ConnectionDB_*> Closing database connection")
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def is_connected(self):
        """
        Verifica se a conexão com o banco de dados está estabelecida.

        Returns:
        - bool: True se estiver conectado, False caso contrário.
        """
        return self.conn is not None
