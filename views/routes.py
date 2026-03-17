from flask import Blueprint, render_template, request, jsonify
import json
from logica_filtros import tranformar_pesquisa_em_filtro, filtros, atributos, lista_nomes

views_bp = Blueprint("views", __name__)

filtros_somente= []
atributos_somente = []
nomes_somente = []

@views_bp.route("/")
def home():
    with open("data/produtos.json", encoding="utf-8") as pro:
        produtos = json.load(pro)
    return render_template("catalogo.html",produtos=produtos)

@views_bp.route("/pesquisar", methods=['GET', 'POST'])
def pesquisar():
    pesquisa = request.json["pesquisa"]
    print("oi", pesquisa)
    filtros_ia = tranformar_pesquisa_em_filtro(pesquisa)
    for f in filtros_ia:
        if f in lista_nomes:
            nomes_somente.append(f)
        elif f in filtros and f not in filtros_somente:
            filtros_somente.append(f)
        elif f in atributos and f not in atributos_somente:
            atributos_somente.append(f)
    #Medida de segurança caso a IA mande vazio
    if len(filtros_somente) == 0:
        filtros_somente.append('nenhum')
    if len(atributos_somente) == 0:
        atributos_somente.append('nenhum')
    if len(nomes_somente) == 0:
        nomes_somente.append('nenhum')

    print(filtros_somente, atributos_somente)
    
    return jsonify({"filtros": filtros_somente, "atributos": atributos_somente, "nomes": nomes_somente})

@views_bp.route("/pegar_produtos", methods=['GET'])
def mandar_produtos():
    with open("data/produtos.json", encoding="utf-8") as pro:
        produtos = json.load(pro)
    return jsonify({"produtos": produtos})