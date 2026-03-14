from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def home():
    filtros = ['Nenhum']
    return render_template("catalogo.html", filtros=filtros)