from flask import Blueprint, render_template, request, jsonify
import json

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def home():
    filtros = ['Nenhum']
    with open("data/produtos.json", encoding="utf-8") as pro:
        produtos = json.load(pro)
    return render_template("catalogo.html", filtros=filtros, produtos=produtos)

@views_bp.route("/pesquisar", methods=['GET', 'POST'])
def pesquisar():
    pesquisa = request.json["pesquisa"]
    print(pesquisa)
 
    return jsonify({"pesquisa": pesquisa})