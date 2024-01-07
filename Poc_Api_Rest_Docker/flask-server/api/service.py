import os
import requests
from html.parser import HTMLParser
from urllib.parse import urlparse
from datetime import datetime

class CustomHTMLParser(HTMLParser):
    '''
    Classe que herda de HTMLParser e implementa métodos para capturar links
    
    Atributos:
        links: lista de tuplas (código, arquivo, link)
        codigo: código de acosso, chave para o dicionário de links na requisição POST 
        title_code: títulos para raspagem HTML
        title_file: título do arquivo
        in_div: flag para indicar se o parser está dentro de uma tag div
        current_tag: tag atual
        old_tag: tag anterior
        
    Métodos:
        handle_starttag: captura tags de abertura
        handle_endtag: captura tags de fechamento
        handle_data: captura dados
        get_links: retorna a lista de links
    '''
    def __init__(self, codigo):
        super().__init__()
        self.csrf_token = None
        self.links = []
        self.codigo = codigo
        self.title_code = None
        self.title_file = None
        self.in_div = False
        self.current_tag = None
        self.old_tag = None

    def handle_starttag(self, tag, attrs):
        # Verifica a tag 'input' para encontrar o token CSRF
        if tag == 'input':
            attrs = dict(attrs)
            if attrs.get('type') == 'hidden' and attrs.get('name') == 'csrf':
                self.csrf_token = attrs.get('value')

        # Lida com as tags 'body', 'div' e 'a' para capturar informações relevantes
        if tag == 'body':
            self.current_tag = 'body'
            self.in_div = False
        elif tag == 'div':
            self.in_div = True
            self.current_tag = 'div'
        elif tag == 'a' and self.in_div:
            self.current_tag = 'a'
            self.in_div = False
            attrs = dict(attrs)
            href = attrs.get('href')
            if href:
                self.links.append((self.title_code, self.title_file, href))
    
    def handle_endtag(self, tag):
        # Lida com o fechamento de tags para controlar o contexto
        if tag in ('head', 'body', 'div'):
            self.old_tag = tag

    def handle_data(self, data):
        # Captura e limpa os dados dentro das tags div
        if self.current_tag == 'div' and self.old_tag == 'head' and data.strip() != "":
            self.title_code = data.strip()
        if self.current_tag == 'div' and self.old_tag == 'div' and self.in_div and data.strip() != "":
            self.title_file = data.strip()

    def get_links(self):
        return self.links


class TaskScraping:
    '''
    Classe que implementa a raspagem dos dados, ao receber uma `URL`(site alvo) e um `CODIGO` (código de acesso)
        - primeira chamada do tipo GET para aquisição do token CSRF.
        - segunda chamada do tipo POST para aquisição dos paramentros url e codigo.
        - terceira chamada do tipo GET para aquisição dos arquivos.
    
    Atributos:
        url: url do site alvo
        base_path: caminho base para salvar os arquivos
        codigo: código de acesso
        session: sessão HTTP
        headers: cabeçalho HTTP
        csrf_token: token CSRF
    
    Métodos:
        is_valid_code: verifica se o código pode ser convertido em um número inteiro
        get_csrf_token: obtém o token CSRF da página
        check_status_code: verifica o status code da resposta HTTP
        download_files: faz o download dos arquivos
        scrape: inicializa as solicitações para a execução dos processamentos
    '''
    def __init__(self, url, codigo):
        self.csrf_token = None
        self.url = url
        self.base_path = 'volume'
        self.codigo = codigo
        self.session = requests.Session()
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
            self.check_status_code(response)
            
            parser = CustomHTMLParser(self.codigo)
            parser.feed(response.text)
            self.csrf_token = parser.csrf_token

        except requests.RequestException as e:
            raise e

    def check_status_code(self, response, success_code=200):
        # Verifica o status code da resposta HTTP
        if response.status_code != success_code:
            raise requests.RequestException(f"Erro no pedido HTTP. Status Code: {response.status_code}, verifique o `CODIGO` de acesso.")

    def download_files(self):
        # Faz o download dos arquivos
        try:
            if not self.csrf_token or not self.is_valid_code():
                raise Exception("Token CSRF ou código inválido.")

            payload = {'codigo': self.codigo, 'csrf': self.csrf_token}
            
            parser = CustomHTMLParser(self.codigo)
            response = self.session.post(self.url, data=payload, headers=self.headers)
            self.check_status_code(response)

            parser.feed(response.text)
            links = parser.get_links()
            
            for code, folder, link in links:
                if not code.isdigit() and int(code) != self.codigo:
                    raise Exception("Divergências no CÓDIGO de acesso e Arquivos")

                parsed_url = urlparse(self.url)
                file_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{parsed_url.path}/{link}"
                file_name = os.path.basename(link)

                current_date = datetime.now().strftime('%Y-%m-%d')

                folder_path = os.path.join(self.base_path, str(self.codigo), current_date, folder)
                file_path = os.path.join(folder_path, file_name)

                response_file = self.session.get(file_url, headers=self.headers)
                self.check_status_code(response)
                
                if not os.path.exists(file_path):
                    os.makedirs(folder_path, exist_ok=True)
                    with open(file_path, 'wb') as file:
                        file.write(response_file.content)
                        print(f"Arquivo {file_name} salvo em {file_path}")
                else:
                    print(f"Arquivo {file_name} já existe em {file_path}")
                            
        except requests.RequestException as e:
            raise e

    def scrape(self):
        # Executa a raspagem dos dados
        try:
            self.get_csrf_token()
            self.download_files()
        except requests.RequestException as e:
            print(f"Erro na solicitação HTTP: {e}")
        except Exception as e:
            print(f"Erro: {e}")