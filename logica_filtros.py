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
- NUNCA mande a resposta vazia se for mandar vazia escreva ['Nenhum']

### MAPA DE TRADUÇÃO:
- "Criativo", "Animado", "Divertido", "Bagunça", "Cabana" -> Retornar: sofa, brinquedo, ludico, infantil
- "Chique", "Elegante", "Moderno", "Design" -> Retornar: premium, poltrona, cama
- "Saúde", "Limpo", "Alergia", "Espirro" -> Retornar: travesseiro, colchao, antialergico
- "Autonomia", "Livre", "Baixinho" -> Retornar: cama, montessoriano

### Regra Busca Abstrata
-Se o usuário digitar algo muito vago, aleatório ou que não tenha um filtro direto (ex: "quero algo legal", "me surpreenda", "aleatório"), NÃO responda "nenhum".

-Em vez disso, retorne os nossos produtos coringa: (sofa, brinquedo) ou (cama, montessoriano, seguranca) ou (poltrona, conforto) ou filtro unico.

-A ideia é sempre tentar mostrar algo, a menos que ele peça algo ofensivo ou totalmente fora do nicho de móveis (como "pizza" ou "carro").

EXEMPLO: 
Produto: CAMA CASAL MONTESSORIANA LISA
Descricao: Cama infantil de estilo montessoriano e minimalista. Focada em autonomia e segurança para bebês e crianças pequenas. Estrutura baixa, estofada com espuma D35 Soft e design clean (cabeceira lisa). Ideal para quem busca decoração acolhedora, moderna e funcional (tecido repelente a líquidos e capa lavável). Vibe: segura, independente, prática, higiênica e elegante. Palavras-chave: quarto de bebê, transição berço, infantil, macio, fácil de limpar, proteção, design europeu.
Filtros: ["cama", "cama casal", "montessoriano", "infantil", "seguranca", "lavavel", "impermeavel"]
Isso é para voce ter um exemplo
"""
genai.configure(api_key=chave_api)

model = genai.GenerativeModel(
    #gemini-2.5-flash
    model_name='gemini-3-flash-preview',
    system_instruction=configuracao_ia,
    generation_config={
          "temperature": 0.3
    }
)


response = model.generate_content("Infantil")

print(response.text, response.usage_metadata.total_token_count)

def tranformar_pesquisa_em_filtro(pesquisa):
    pass