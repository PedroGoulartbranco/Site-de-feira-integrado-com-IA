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
    'travesseiro', 'colchao', 'acessorio',
]

atributos = ['impermeavel', 'antialergico', 'montessoriano', 'lavavel', 'infantil', 'seguranca', "sofa"]

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
Sua missão é converter a busca do usuário em uma ÚNICA LISTA contendo os filtros, atributos e nomes de modelos apropriados.

LISTA DE PALAVRAS PERMITIDAS (Você NUNCA pode inventar uma palavra que não esteja aqui):
- Categorias: {filtros}
- Atributos: {atributos}
- Modelos Específicos (Nomes dos Produtos): {lista_nomes}

### MAPA DE TRADUÇÃO (Exemplos de raciocínio):
- 'Divertido', 'Bagunça', 'Criança', 'Cabana' -> Retornar: ['sofa', 'cama', 'infantil', 'seguranca']
- 'Chique', 'Elegante', 'Moderno', 'Premium' -> Retornar: ['poltrona', 'sofa', 'cama casal']
- 'Saúde', 'Limpo', 'Alergia', 'Espirro' -> Retornar: ['antialergico', 'lavavel']
- 'Autonomia', 'Livre', 'Baixinho' -> Retornar: ['cama solteiro', 'montessoriano', 'seguranca']
- 'Xixi', 'Sujeira', 'Cachorro', 'agua', 'suco' -> Retornar: ['impermeavel', 'lavavel']

### REGRAS DE COMPORTAMENTO:
1. IDENTIFICAÇÃO DE MODELO (PRIORIDADE): Se o usuário digitar o nome (ou algo muito parecido) de um produto da lista 'Modelos Específicos', retorne o nome exato do modelo presente na lista. O nome do modelo prevalece sobre categorias genéricas.
2. TOLERÂNCIA A ERROS: Ignore erros de digitação, falta de acentos ou trocas de letras (ex: 'berso' -> 'berço', 'poutrona' -> 'poltrona'). Mapeie para o termo correto da lista permitida.
3. FORMATO DA RESPOSTA (OBRIGATÓRIO): Responda ÚNICA E EXCLUSIVAMENTE com a lista no formato de array []. Você é OBRIGADO a usar aspas simples ('') para envolver cada item da lista. Nunca use aspas duplas (""). Não coloque explicações ou blocos de código.
4. SELETIVIDADE: Só adicione ATRIBUTOS se o usuário mencionar necessidade específica (ex: 'fácil de limpar'). Se ele buscar apenas o objeto ou nome, retorne apenas os termos principais.
5. ASSUNTOS IRRELEVANTES: Para nomes próprios de pessoas ou assuntos fora do catálogo de móveis, retorne: ['nenhum']
6. BUSCAS VAGAS: Se a busca for vaga ('algo legal'), use termos curinga: ['sofa', 'poltrona']

EXEMPLO DE RESPOSTA OBRIGATÓRIA:
['cama casal', 'montessoriano', 'infantil']
"""
genai.configure(api_key=chave_api)

model = genai.GenerativeModel(
    #gemini-2.5-flash
    #gemini-3-flash-preview
    model_name='gemini-2.5-flash',
    system_instruction=configuracao_ia,
    generation_config={
          "temperature": 0.3
    }
)

def tranformar_pesquisa_em_filtro(pesquisa):
    response = model.generate_content(pesquisa)
    #Usando a biblioteca ASt como segurança contra comandos vindo da pesquisa
    filtros_ia = ast.literal_eval(response.text)
    filtros_ia = list(set(filtros_ia))

    return filtros_ia