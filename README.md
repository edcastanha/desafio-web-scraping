# PoC Web Scraping

## EXTRAÇÃO E ORGANIZAÇÃO DE DADOS WEB

`<b>`Descrição:`</b>` O desafio é desenvolver um programa em Python capaz de acessar e extrair informações de um website específico, organizando-as de forma eficaz.

*! Importante ressaltar que o uso do Selenium* ou bibliotecas similares** não é permitido.

`<b>`Critérios de Avaliação:`</b>`

 Organização dos Dados: A maneira como os dados são estruturados e armazenados para fácil acesso e manipulação.

 Lógica de Programação: A clareza, eficiência e eficácia da lógica empregada para acessar, extrair e organizar os dados.

 Leitura de Arquivos: A habilidade em lidar com a leitura dos arquivos disponibilizados no website, bem como a interpretação correta dos dados contidos neles.

 Download de Arquivos: A implementação de uma solução robusta para o download dos arquivos disponíveis, garantindo a integridade dos dados.

Website Alvo: https://site_alvo.com.br

Códigos de Acesso: 123456, 12345

Após a inserção dos códigos, o candidato obterá acesso aos arquivos relevantes que deverão ser processados.

Publicação: O código finalizado deve ser publicado em um repositório GitHub, com um README explicativo.

`<b>`Observações:`</b>`

* Selenium é uma ferramenta que permite controlar um navegador web pelo computador. Funciona em diferentes navegadores e sistemas operacionais, e pode ser usado com várias linguagens de programação, como Python. Geralmente é usado para testar aplicativos web automaticamente, mas também ajuda a coletar dados de sites quando não há APIs disponíveis.
* Qualquer biblioteca que permita o controle do navegador do usuário.

## Da pesquisa sobre características e classificação do Selenium em relacao a outras ferramentas de Web Scraping.

Conforme a breve descrição acima, o Selenium tem como origem a automação de testes de aplicativos web, mas também pode ser utilizado para extração de dados de sites quando não há APIs disponíveis.

Devido à restrição de não utilização da biblioteca Selenium e outras semelhantes, como PyAutoGUI e Playwright, para automação de tarefas em navegadores web e sistemas operacionais, surgiu a dúvida se outras bibliotecas e ferramentas (BeautifulSoup, lxml e Scrapy) focadas em scraping se enquadrariam como quebra de requisito.

Sendo assim, aproveitei a oportunidade para realizar uma análise comparativa entre BeautifulSoup e Scrapy para web scraping. Um exemplo de sintaxe e desempenho encontra-se em `./PoC_Scripts_Jupyter/src/` <<< [Veja mais](./PoC_Scripts_Jupyter/) >>> .

# `<center>` Do Desafio - Script Jupyter Noteboo `</center>`

## 1 - PoC Web Scraping - EXTRAÇÃO E ORGANIZAÇÃO DE DADOS WEB

### Pré-requisitos

- Git
- Docker
- Docker-Compose

* imagen final com tamanho de 876.19 MB baseada na [imagen docker-stacks-foundation](https://github.com/jupyter/docker-stacks/tree/main/images/docker-stacks-foundation)

### Execução - via Container Docker

```

$ git clone .https://github.com/edcastanha/scraping_api

$ cd Poc_Scripts_Jupyter/

$ docker-compose up

```
