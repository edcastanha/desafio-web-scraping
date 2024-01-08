from flask import Blueprint, request, jsonify
from helpers.service import TaskScraping

blueprint = Blueprint("routes", __name__)


@blueprint.route("/")
def home():
    return "<h1>Bem-vindo à Scrapping Web Teste - II!</h1>"

@blueprint.route("/scrapping" , methods=["POST"])
def scrapping():
    '''
    Classe deve verificar url e codigo e disparar publisher para Fila de tasks com mensagem contendo url e codigos validos
    '''
    input_args = request.get_json()

    if input_args is None:
        return {"message": "conjunto de entrada invalido"}

    url = input_args.get("url")
    if url is None:
        return {"message": "é necessário passar a entrada url"}
    
    codigo = input_args.get("codigo")
    if codigo is None:
        return {"message": "é necessário passar a entrada codigo"}
    
   
retomando
