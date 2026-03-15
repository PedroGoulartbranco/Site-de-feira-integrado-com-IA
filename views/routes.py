from flask import Blueprint, render_template, request, jsonify
import json
from logica_filtros import tranformar_pesquisa_em_filtro

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
    filtros_ia = tranformar_pesquisa_em_filtro(pesquisa)
    print(filtros_ia)
    return jsonify({"pesquisa": pesquisa})