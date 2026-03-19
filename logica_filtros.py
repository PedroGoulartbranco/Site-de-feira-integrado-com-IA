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
Sua missão é converter a busca do usuário em uma ÚNICA LISTA de termos técnicos para filtragem.

LISTA DE PALAVRAS PERMITIDAS:
- Categorias: {filtros}
- Atributos: {atributos}
- Modelos Específicos: {lista_nomes}

### REGRAS DE COMPORTAMENTO (ESTRITAS):

1. HIERARQUIA DE RETORNO: 
   - Se o usuário busca por uma CATEGORIA (ex: 'sofá', 'cama'), retorne APENAS o termo da categoria. 
   - NÃO retorne nomes de modelos específicos se o usuário usou um termo genérico.

2. FILTRAGEM POR ATRIBUTO:
   - Se o usuário mencionar 'capa' ou termos relacionados a protetores, retorne APENAS o termo 'capa'. 
   - NÃO adicione 'lavavel' ou outros sinônimos se o termo 'capa' já existir na lista permitida.

3. CONCISÃO MÁXIMA:
   - O objetivo é gerar o MENOR array possível que satisfaça a busca. 

4. TOLERÂNCIA A ERROS: 
   - Corrija erros de digitação baseando-se APENAS na lista permitida.

5. FORMATO DA RESPOSTA (OBRIGATÓRIO): 
   - Responda APENAS o array: ['item1', 'item2']. 
   - Use aspas simples (''). Sem explicações ou blocos de código.

6. BUSCAS ALEATÓRIAS OU SUGESTÕES:
   - Se o usuário pedir "algo aleatório", "uma sugestão", "qualquer produto" ou "me surpreenda", você deve ESCOLHER UM NOME DE MODELO da lista {lista_nomes} ao seu critério e retornar apenas ele dentro do array.
   - Exemplo de busca: 'me dê um produto aleatório' -> Retorno: ['Cama Joy'] (ou qualquer outro nome da lista).

7. BUSCAS REALMENTE IRRELEVANTES:
   - Somente se o usuário falar de assuntos que não existem na lista (ex: política, futebol, nomes de pessoas que não são produtos), retorne: ['nenhum'].
"""
genai.configure(api_key=chave_api)


lista_modelos = ['gemini-2.0-flash', 'gemini-2.5-flash-lite']
atual = 0
nome_modelo = 'gemini-2.5-flash'

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
    response = model.generate_content(pesquisa)
        
    #Usando a biblioteca ASt como segurança contra comandos vindo da pesquisa
    filtros_ia = ast.literal_eval(response.text)
    print("IA respondeu com sucesso!")
    filtros_ia = list(set(filtros_ia))
    print(filtros_ia)

    return filtros_ia