from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import ast

load_dotenv()

chave_api = os.getenv("CHAVE_API")



filtros = [
    # Categorias Principais
    'poltrona',  'sofa', 'cama', 'cama casal', 'cama solteiro', 
    'travesseiro', 'colchao', 'acessorio',
]

atributos = ['impermeavel', 'antialergico', 'montessoriano', 'lavavel', 'infantil', 'seguranca', "sofa"]

with open("data/produtos.json", encoding="utf-8") as pro:
        produtos = json.load(pro)

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
Você é um especialista em classificação semântica de móveis.
Sua missão é converter a busca do usuário em uma ÚNICA LISTA contendo os filtros e atributos apropriados.

LISTA DE PALAVRAS PERMITIDAS (Você NUNCA pode inventar uma palavra que não esteja aqui):
- Categorias: {filtros}
- Atributos: {atributos}

### MAPA DE TRADUÇÃO (Exemplos de raciocínio):
- "Divertido", "Bagunça", "Criança", "Cabana" -> Retornar: ["sofa", "cama", "infantil", "seguranca"]
- "Chique", "Elegante", "Moderno", "Premium" -> Retornar: ["poltrona", "sofa", "cama casal"]
- "Saúde", "Limpo", "Alergia", "Espirro" -> Retornar: ["antialergico", "lavavel"]
- "Autonomia", "Livre", "Baixinho" -> Retornar: ["cama solteiro", "montessoriano", "seguranca"]
- "Xixi", "Sujeira", "Cachorro", "agua", "suco"-> Retornar: ["impermeavel", "lavavel"]

### REGRAS DE COMPORTAMENTO:
1. Assuntos Irrelevantes ou Nomes: Se o usuário digitar nomes próprios (ex: Pedro, Maria) ou coisas totalmente sem relação com a loja de móveis (ex: Futebol, Carro, Pizza), retorne EXATAMENTE: ["nenhum"]
2. Buscas Vagas: Se a busca for vaga ("quero algo legal", "me surpreenda"), retorne produtos curinga da lista, como: ["sofa", "poltrona"]
3. Formato da Resposta: Você deve responder ÚNICA E EXCLUSIVAMENTE com a lista no formato de array. Não coloque explicações, não diga "Aqui está", não use blocos de código (```). Apenas a lista.
4. SELETIVIDADE DE ATRIBUTOS: Só adicione termos da lista de ATRIBUTOS se o usuário mencionar explicitamente uma necessidade relacionada (ex: "seguro", "para meu filho", "fácil de limpar"). Se o usuário buscar apenas pelo objeto (ex: "sofa", "algo para sentar"), retorne APENAS a categoria e coloque "nenhum" na parte de atributos.
5. FOCO NA INTENÇÃO: "Algo para sentar" deve retornar apenas categorias como ["sofa", "poltrona"]. Não presuma que quem quer sentar é uma criança ou precisa de segurança extra, a menos que isso seja dito.

EXEMPLO DE RESPOSTA PERFEITA:
["cama casal", "montessoriano", "infantil"]
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