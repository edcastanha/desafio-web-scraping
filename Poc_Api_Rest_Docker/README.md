# EXTRAÇÃO E ORGANIZAÇÃO DE DADOS WEB

**Descrição**:

O desafio é desenvolver um programa em Python capaz de acessar e extrair informações de um website específico, organizando-as de forma eficaz.

*! Importante ressaltar que o uso do Selenium* ou bibliotecas similares** não é permitido.

**Critérios de Avaliação:**

 Organização dos Dados: A maneira como os dados são estruturados e armazenados para fácil acesso e manipulação.
 Lógica de Programação: A clareza, eficiência e eficácia da lógica empregada para acessar, extrair e organizar os dados.
 Leitura de Arquivos: A habilidade em lidar com a leitura dos arquivos disponibilizados no website, bem como a interpretação correta dos dados contidos neles.
 Download de Arquivos: A implementação de uma solução robusta para o download dos arquivos disponíveis, garantindo a integridade dos dados.

* *Website Alvo:*
  url = site_alvo.com.br
* *Códigos de Acesso:*
  codigo = 123456

Após a inserção dos códigos, o candidato obterá acesso aos arquivos relevantes que deverão ser processados.
Publicação: O código finalizado deve ser publicado em um repositório GitHub, com um README explicativo.

**Observações:**

* Selenium é uma ferramenta que permite controlar um navegador web pelo computador. Funciona em diferentes navegadores e sistemas operacionais, e pode ser usado com várias linguagens de programação, como Python. Geralmente é usado para testar aplicativos web automaticamente, mas também ajuda a coletar dados de sites quando não há APIs disponíveis.
* Qualquer biblioteca que permita o controle do navegador do usuário.

# Do Desafio - API REST - Flask

## 1 - PoC Web Scraping - EXTRAÇÃO E ORGANIZAÇÃO DE DADOS WEB

### Pré-requisitos

- Git
- Docker
- Docker-Compose

## Execução - via Container Docker

```
$ git clone .https://github.com/edcastanha/scraping_api
# >>> Cloning into 'desafio-web-scraping'...
$ cd desafio-web-scraping/Poc_Api_Rest_Docker/
$ docker-compose up
```

### Arquitetura Geral:

1. **Servidor Django:**
   * Será responsável pela definição dos modelos de dados do cliente, URLs e configurações relacionadas.
2. **API Flask:**
   * Oferecerá endpoints para interação com o sistema, permitindo que os clientes sejam cadastrados, URLs sejam associadas a tarefas e configurações sejam gerenciadas.
3. **Celery com RabbitMQ:**
   * O Celery será usado para a gestão de tarefas assíncronas. RabbitMQ será o broker de mensagens para orquestrar as filas.

Aqui está uma descrição detalhada de cada componente:

1. Servidor Django:

* **Modelos de Dados:**
  * Criará modelos de dados para clientes, URLs e configurações de tarefas.
  * Exemplo:
    * Modelo Cliente: Nome, Email, etc.
    * Modelo Alvo: URL, CODIGO, Descrição, etc.
    * Modelo Tarefa: Tipo (diária, semanal, quinzenal, mensal), Parâmetros, Cliente Associado, Alvo Associada, etc.
* **Administração de Clientes:**
  * Fornecerá funcionalidades CRUD (Criar, Ler, Atualizar, Deletar) para gerenciar informações dos clientes.
* **Gerenciamento de URLs e Tarefas:**
  * Permitirá associar URLs às tarefas e configurar a frequência de execução das tarefas para cada cliente.

2. API Flask:

* **Endpoints para Cadastro e Gestão:**
  * Oferecerá endpoints tratamento de eventos na fila scrapping (RBMQ), validacao de codigo, URLs.
  * Exemplo:
    * `/api/scrapping`: Endpoints para criar arquivos frutos das validacoes e processamento de task.
    * `/api/tasks`: Endpoints para definir a frequência e parâmetros das tarefas.
* **Validação de Dados:**
  * Validará os dados recebidos antes de armazená-los no servidor Django.

3. Celery com RabbitMQ:

* **Configuração do Celery:**
  * Será configurado para gerenciar tarefas assíncronas.
  * Definirá diferentes workers para processar tarefas diárias, semanais, quinzenais e mensais.
* **Orquestração de Tarefas:**
  * As tarefas serão enfileiradas no RabbitMQ, aguardando processamento pelos workers do Celery.
  * Os workers serão configurados para executar as tarefas de acordo com a frequência especificada.
* **Processamento das Tarefas:**
  * Cada tipo de tarefa (diária, semanal, quinzenal, mensal) terá um worker dedicado para executar o tratamento e extração de dados das URLs associadas aos clientes.

Essa arquitetura permitirá que os clientes sejam cadastrados, URLs sejam associadas a tarefas com diferentes frequências e que o sistema execute essas tarefas de forma assíncrona usando o Celery com RabbitMQ para orquestrar a execução das filas.



***`<center>`! LEMBRETE ! `</center>`***

 **execute para remover os volumes e imagens do docker:**

```
docker-compose down -v --rmi all
```

---

## Conclusão