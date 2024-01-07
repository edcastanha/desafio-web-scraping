from flask import Blueprint, request, jsonify
import os

blueprint = Blueprint("routes", __name__)


@blueprint.route("/")
def home():
    return "<h1>Bem-vindo à Scrapping Web Teste - II!</h1>"

@blueprint.route("/scrapping" , methods=["POST"])
def scrapping():
    input_args = request.get_json()

    if input_args is None:
        return {"message": "conjunto de entrada invalido"}

    url = input_args.get("img")
    if img_path is None:
        return {"message": "é necessário passar a entrada img_path"}
    
    if img_path.split(".")[-1] not in ["jpg", "png", "jpeg"]:
        return {"message": "é necessário passar a entrada img_path com extensão .jpg, .png ou .jpeg"}
    
    try: 
        obj = service.represent(
            img_path=img_path,
            model_name=model_name,
            detector_backend=detector_backend,
            enforce_detection=enforce_detection,
            align=align,
        )
        return obj
    except Exception as e:
        return {"error": str(e)}
