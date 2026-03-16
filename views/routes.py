from flask import Blueprint, render_template, request, jsonify
import json
from logica_filtros import tranformar_pesquisa_em_filtro, filtros, atributos

views_bp = Blueprint("views", __name__)

filtros_somente= []
atributos_somente = []

@views_bp.route("/")
def home():
    with open("data/produtos.json", encoding="utf-8") as pro:
        produtos = json.load(pro)
    return render_template("catalogo.html",produtos=produtos)

@views_bp.route("/pesquisar", methods=['GET', 'POST'])
def pesquisar():
    pesquisa = request.json["pesquisa"]
    print(pesquisa)
    filtros_ia = tranformar_pesquisa_em_filtro(pesquisa)
    for f in filtros_ia:
        if f in filtros and f not in filtros_somente:
            filtros_somente.append(f)
        elif f in atributos and f not in atributos_somente:
            atributos_somente.append(f)

    print(filtros_somente, atributos_somente)
    
    return jsonify({"filtros": filtros_somente, "atributos": atributos_somente})

@views_bp.route("/pegar_produtos", methods=['GET'])
def mandar_produtos():
    with open("data/produtos.json", encoding="utf-8") as pro:
        produtos = json.load(pro)
    return jsonify({"produtos": produtos})