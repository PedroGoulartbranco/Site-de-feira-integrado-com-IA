from flask import Blueprint, render_template, request, jsonify
import json
from logica_filtros import tranformar_pesquisa_em_filtro, filtros

views_bp = Blueprint("views", __name__)

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
    print(filtros_ia)
    return jsonify({"filtros": filtros_ia})

@views_bp.route("/pegar_produtos", methods=['GET'])
def mandar_produtos():
    with open("data/produtos.json", encoding="utf-8") as pro:
        produtos = json.load(pro)
    return jsonify({"produtos": produtos})