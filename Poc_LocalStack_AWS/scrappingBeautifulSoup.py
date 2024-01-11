import os
import requests
from urllib.parse import urlparse
from datetime import datetime
from bs4 import BeautifulSoup
import time
from .logging_me import logger  # Importa o módulo logger

class Jobs:
    '''
    Classe que implementa a raspagem dos dados, ao receber uma `URL`(site alvo) e um `CODIGO` (código de acesso)
    
    - Primeira chamada do tipo GET para aquisição do token CSRF.
    - Segunda chamada do tipo POST para aquisição dos parâmetros url e código.
    - Terceira chamada do tipo GET para aquisição dos arquivos.

    ... (Docstring omitida por questões de espaço)
    '''
    def __init__(self, url, codigo):
        # Inicializa os atributos da classe
        self.csrf_token = None
        self.url = url
        self.base_path = 'ftp'
        self.codigo = codigo
        self.session = requests.Session()  # Cria uma sessão HTTP
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def is_valid_code(self):
        # Verifica se o código pode ser convertido em um número inteiro
        try:
            int(self.codigo)
            return True
        except ValueError:
            return False
        
    def get_csrf_token(self):
        # Obtém o token CSRF da página
        try:
            response = self.session.get(self.url, headers=self.headers)
            self.check_status_code(response)  # Verifica o status da resposta HTTP
            
            soup = BeautifulSoup(response.text, 'html.parser')
            self.csrf_token = soup.find('input', {'name': 'csrf_token'}).get('value')

        except requests.RequestException as e:
            # Registra o erro ao obter o token CSRF
            logger.error(f"Erro ao obter o token CSRF: {e}")
            raise e  # Relança a exceção para lidar com ela em um nível superior

    def check_status_code(self, response, success_code=200):
        # Verifica o status code da resposta HTTP
        if response.status_code != success_code:
            error_msg = f"Erro no pedido HTTP. Status Code: {response.status_code}, verifique o `CODIGO` de acesso."
            logger.error(error_msg)
            raise requests.RequestException(error_msg)  # Lança uma exceção caso o status code não seja o esperado

    def download_files(self):
        # Faz o download dos arquivos
        try:
            if not self.csrf_token or not self.is_valid_code():
                raise Exception("Token CSRF ou código inválido.")

            payload = {'codigo': self.codigo, 'csrf': self.csrf_token}
            
            response = self.session.post(self.url, data=payload, headers=self.headers)
            self.check_status_code(response)  # Verifica o status da resposta HTTP

            soup = BeautifulSoup(response.text, 'html.parser')
            links = [(a.get('data-code'), a.get('data-folder'), a.get('href')) for a in soup.find_all('a', {'class': 'download-link'})]
            
            for code, folder, link in links:
                # Verifica divergências entre o código de acesso e os arquivos
                if not code.isdigit() and int(code) != self.codigo:
                    raise Exception("Divergências no CÓDIGO de acesso e Arquivos")

                parsed_url = urlparse(self.url)
                file_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{parsed_url.path}/{link}"
                file_name = os.path.basename(link)

                current_date = datetime.now().strftime('%Y-%m-%d')

                folder_path = os.path.join(self.base_path, str(self.codigo), current_date, folder)
                file_path = os.path.join(folder_path, file_name)

                response_file = self.session.get(file_url, headers=self.headers)
                self.check_status_code(response_file)  # Verifica o status da resposta HTTP
                
                if not os.path.exists(file_path):
                    os.makedirs(folder_path, exist_ok=True)
                    with open(file_path, 'wb') as file:
                        file.write(response_file.content)
                        logger.info(f"Arquivo {file_name} salvo em {file_path}")
                else:
                    logger.info(f"Arquivo {file_name} já existe em {file_path}")
                            
        except requests.RequestException as e:
            # Registra o erro durante o download dos arquivos
            logger.error(f"Erro durante o download dos arquivos: {e}")
            raise e  # Relança a exceção para lidar com ela em um nível superior
        except Exception as e:
            # Registra erro inesperado durante o download dos arquivos
            logger.error(f"Erro inesperado durante o download dos arquivos: {e}")
            raise e  # Relança a exceção para lidar com ela em um nível superior

    def scrape(self):
        # Executa a raspagem dos dados
        try:
            start_time = time.time()
            self.get_csrf_token()
            self.download_files()
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"Tempo total de execução: {execution_time} segundos")
        except requests.RequestException as e:
            # Registra erro na solicitação HTTP
            logger.error(f"Erro na solicitação HTTP: {e}")
            raise e  # Relança a exceção para lidar com ela em um nível superior
        except Exception as e:
            # Registra erro inesperado
            logger.error(f"Erro: {e}")
            raise e  # Relança a exceção para lidar com ela em um nível superior
