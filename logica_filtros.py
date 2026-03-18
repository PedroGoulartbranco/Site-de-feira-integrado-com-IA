from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import ast

load_dotenv()

chave_api = os.getenv("CHAVE_API")

lista_nomes = []

filtros = [
    # Categorias Principais
    'poltrona',  'sofa', 'cama', 'cama casal', 'cama solteiro', 
    'travesseiro', 'colchao', 'acessorio', 'cama junior', "capa"
]

atributos = ['impermeavel', 'capa','antialergico', 'montessoriano', 'lavavel', 'infantil', 'seguranca']

with open("data/produtos.json", encoding="utf-8") as pro:
        produtos = json.load(pro)

for produto in produtos:
    lista_nomes.append(produto["name"])

prompt_para_classificar_filtro_produtos = f"""
    Você é um classificador de buscas para um site de móveis.
    Vou te mandar o produtos junto com suas descricoes IGNORE PRECO e IMG
    Voce vai ler o nome do produto e a descricao e com base na lista de filtro para cada produto que 
    voce me fale quais filtros colcoar em cada produto
    POde ter mais de um filtro por produto
    Filtros: {filtros}
    Atributos para serem usado nos filtros tambem: {atributos}
    Produtos: {produtos}
"""

configuracao_ia = f"""
Você é um especialista em classificação semântica de móveis da Bell'Baby.
Sua missão é converter a busca do usuário em uma ÚNICA LISTA de termos técnicos para filtragem.

LISTA DE PALAVRAS PERMITIDAS:
- Categorias: {filtros}
- Atributos: {atributos}
- Modelos Específicos: {lista_nomes}

### REGRAS DE COMPORTAMENTO (ESTRITAS):

1. HIERARQUIA DE RETORNO: 
   - Se o usuário busca por uma CATEGORIA (ex: 'sofá', 'cama'), retorne APENAS o termo da categoria. 
   - NÃO retorne nomes de modelos específicos se o usuário usou um termo genérico.
   - Retorne um modelo específico APENAS se o usuário digitar o nome exato ou parte única do nome do produto (ex: 'Cama Joy', 'Poltrona Slim').

2. FILTRAGEM POR ATRIBUTO:
- Se o usuário mencionar termos relacionados a capas (ex: 'capa'), mapear para o atributo 'lavavel'.
- Se mencionar necessidades como 'impermeável', 'antialérgico', etc, usar os atributos correspondentes.

3. CONCISÃO MÁXIMA:
   - O objetivo é gerar o MENOR array possível que satisfaça a busca. 
   - Se o usuário busca 'sofá e capa', NÃO retorne os nomes dos sofás. Retorne apenas os filtros que o código JS usará para reduzir a lista.

4. TOLERÂNCIA A ERROS: 
   - Corrija erros de digitação (ex: 'soffa' -> 'sofa') baseando-se APENAS na lista permitida.

5. FORMATO DA RESPOSTA (OBRIGATÓRIO): 
   - Responda APENAS o array: ['item1', 'item2']. 
   - Use aspas simples (''). Sem explicações, sem blocos de código Markdown, sem texto extra.

6. BUSCAS IRRELEVANTES OU VAZIAS:
   - Se não houver correspondência ou for assunto fora de móveis, retorne: ['nenhum'].

EXEMPLO DE SAÍDA PARA 'Quero ver sofás que possam lavar a capa':
['sofa', 'lavavel']
"""
genai.configure(api_key=chave_api)

lista_modelos = ['gemini-3-flash-preview', 'gemini-2.5-flash']
atual = 0
nome_modelo = 'gemini-3-flash-preview'

def criar_modelo(indice):
     model = genai.GenerativeModel(
        #gemini-2.5-flash
        #gemini-3-flash-preview
        model_name=lista_modelos[indice],
        system_instruction=configuracao_ia,
        generation_config={
            "temperature": 0.3
        }
    )
     return model

model = criar_modelo(atual)

def tranformar_pesquisa_em_filtro(pesquisa):
    atual = 0
    try:
        response = model.generate_content(pesquisa)
    except:
        if (atual == 0):
            atual = 1
        else:
            atual = 0
        model = criar_modelo(atual)
        response = model.generate_content(pesquisa)
        
    #Usando a biblioteca ASt como segurança contra comandos vindo da pesquisa
    filtros_ia = ast.literal_eval(response.text)
    filtros_ia = list(set(filtros_ia))

    return filtros_ia