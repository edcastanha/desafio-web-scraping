from html.parser import HTMLParser

class CustomHTMLParser(HTMLParser):
    '''
    Classe que herda de HTMLParser e implementa métodos para capturar links

    Atributos:
        links: lista de tuplas (código, arquivo, link)
        codigo: código de acesso, chave para o dicionário de links na requisição POST
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
