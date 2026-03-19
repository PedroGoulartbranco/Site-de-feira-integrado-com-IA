from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import ast

load_dotenv()

#chave_api = os.getenv("CHAVE_API")
chave_api = os.environ.get("GOOGLE_API_KEY")

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
Sua missão é converter a busca ou situação do usuário em uma ÚNICA LISTA de termos das listas permitidas.

LISTA DE PALAVRAS PERMITIDAS:
- Categorias: {filtros}
- Atributos: {atributos}
- Modelos Específicos: {lista_nomes}

### REGRAS DE COMPORTAMENTO (ESTRITAS):

1. INTERPRETAÇÃO DE CENÁRIOS (O CÉREBRO):
   - Se o usuário descrever uma situação, você deve "traduzir" para os termos das listas permitidas.
   - EXEMPLO: "criança brincando com água" ou "derramou suco" -> Retorne os atributos correspondentes: ['infantil', 'impermeavel', 'lavavel'].
   - EXEMPLO: "tenho pet" ou "cachorro" -> Retorne: ['lavavel'].

2. HIERARQUIA E CONCISÃO: 
   - Se o usuário busca por CATEGORIA (ex: 'sofá'), retorne apenas a categoria. 
   - Se mencionar 'capa', retorne apenas 'capa'. Não adicione 'lavavel' se 'capa' já for o termo principal.

3. BUSCA POR NOME:
   - Se o usuário digitar um nome que exista em {lista_nomes}, retorne o nome exato do modelo dentro da lista.

4. FORMATO DA RESPOSTA (OBRIGATÓRIO): 
   - Responda APENAS o array plano: ['item1', 'item2']. 
   - Use aspas simples ('). Sem explicações, sem blocos de código (```), apenas a lista.

5. BUSCAS ALEATÓRIAS OU SUGESTÕES:
   - Se o usuário pedir sugestão ou algo aleatório, escolha UM nome da lista {lista_nomes} e retorne: ['Nome Escolhido'].

6. BUSCAS REALMENTE IRRELEVANTES:
   - Retorne ['nenhum'] APENAS se o assunto não tiver NENHUMA relação com móveis, proteção ou uso doméstico (ex: política, futebol, receitas). 
   - "Criança" e "água" SÃO relevantes pois remetem a atributos de proteção.
"""
genai.configure(api_key=chave_api)


lista_modelos = ['gemini-2.5-flash', 'gemini-3.1-flash-lite-preview']
atual = 0
nome_modelo = lista_modelos[1]

def criar_modelo(indice, erro=False):
   global nome_modelo
   if erro:
         if nome_modelo == 'gemini-3.1-flash-lite-preview':
             nome_modelo = lista_modelos[0]
         else:
             nome_modelo = lista_modelos[1]
   model = genai.GenerativeModel(
        #gemini-2.5-flash
        #gemini-3-flash-preview
        model_name=nome_modelo,
        system_instruction=configuracao_ia,
        generation_config={
            "temperature": 0.3
        }
    )
   return model

model = criar_modelo(atual)

def tranformar_pesquisa_em_filtro(pesquisa):
   global model
   try:
      response = model.generate_content(pesquisa)
   except:
      model = criar_modelo(atual, erro=True)
      response = model.generate_content(pesquisa)
        
   #Usando a biblioteca ASt como segurança contra comandos vindo da pesquisa
   filtros_ia = ast.literal_eval(response.text)
   print("IA respondeu com sucesso!")
   filtros_ia = list(set(filtros_ia))
   print(filtros_ia)

   return filtros_ia