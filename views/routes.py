from flask import Blueprint, render_template
import json

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def home():
    filtros = ['Nenhum']
    with open("data/produtos.json", encoding="utf-8") as pro:
        produtos = json.load(pro)
    return render_template("catalogo.html", filtros=filtros, produtos=produtos)