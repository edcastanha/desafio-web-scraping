import os
from flask import Blueprint, request, jsonify
from helpers.service import TaskScraping

blueprint = Blueprint("routes", __name__)


@blueprint.route("/")
def home():
    return "<h1>Bem-vindo à Scrapping Web Teste - II!</h1>"

@blueprint.route("/scrapping" , methods=["POST"])
def scrapping():
    input_args = request.get_json()

    if input_args is None:
        return {"message": "conjunto de entrada invalido"}

    url = input_args.get("url")
    if url is None:
        return {"message": "é necessário passar a entrada img_path"}
    
    codigo = input_args.get("codigo")
    if url is None:
        return {"message": "é necessário passar a entrada img_path"}
    
    key = input_args.get("url")
    if url is None:
        return {"message": "é necessário passar a entrada img_path"}
    
    if filesDown.split(".")[-1] not in ["txt", "pdf"]:
        return {"message": "O arquivo nao contem a extensão valida ( txt ou pdf)"}
    
  from flask import Flask, jsonify, request


@app.route('/scrape', methods=['POST'])
def scrape_data():
   