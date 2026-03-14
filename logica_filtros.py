from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

load_dotenv()

chave_api = os.getenv("CHAVE_API")

filtros = [
    # Categorias Principais
    'poltrona', 'piscina', 'sofa', 'cama', 'cama casal', 'cama solteiro', 
    'travesseiro', 'colchao', 'acessorio', 'brinquedo',
    
    # Atributos
    'impermeavel', 'antialergico', 'montessoriano', 'lavavel', 'infantil', 'seguranca'
]

with open("data/produtos.json", encoding="utf-8") as pro:
        produtos = json.load(pro)

prompt_para_classificar_filtro_produtos = f"""
    Você é um classificador de buscas para um site de móveis.
    Vou te mandar o produtos junto com suas descricoes IGNORE PRECO e IMG
    Voce vai ler o nome do produto e a descricao e com base na lista de filtro para cada produto que 
    voce me fale quais filtros colcoar em cada produto
    POde ter mais de um filtro por produto
    Filtros: {filtros}
    Produtos: {produtos}
"""

configuracao_ia = f"""
Você é um especialista em classificação semântica de móveis.
Sua missão é converter o desejo do usuário em FILTROS TÉCNICOS.

LISTA DE FILTROS: {filtros}

REGRAS DE OURO:
- Busca por "animado", "bagunça" ou "brincar" -> retornar: brinquedo, infantil, lúdico.
- Busca por "chique", "elegante" ou "luxo" -> retornar: premium, [categoria do móvel].
- Busca por "limpeza", "xixi" ou "sujeira" -> retornar: lavavel, impermeavel.
- SEMPRE responda apenas os termos da lista, sem textos extras.
- Se houver dúvida, retorne os filtros mais abrangentes.

EXEMPLO: 
Produto: CAMA CASAL MONTESSORIANA LISA
Descricao: Cama infantil de estilo montessoriano e minimalista. Focada em autonomia e segurança para bebês e crianças pequenas. Estrutura baixa, estofada com espuma D35 Soft e design clean (cabeceira lisa). Ideal para quem busca decoração acolhedora, moderna e funcional (tecido repelente a líquidos e capa lavável). Vibe: segura, independente, prática, higiênica e elegante. Palavras-chave: quarto de bebê, transição berço, infantil, macio, fácil de limpar, proteção, design europeu.
Filtros: ["cama", "cama casal", "montessoriano", "infantil", "seguranca", "lavavel", "impermeavel"]
Isso é para voce ter um exemplo
"""
genai.configure(api_key=chave_api)

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=configuracao_ia,
    generation_config={
          "temperature": 0.2
    }
)

response = model.generate_content("Quero algo animado")

print(response.text)

def tranformar_pesquisa_em_filtro(pesquisa):
    pass