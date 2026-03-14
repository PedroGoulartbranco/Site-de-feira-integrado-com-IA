from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

chave_api = os.getenv("CHAVE_API")

filtros = ['poltrona', 'piscina', 'sofa', 'cama', 'cama casal', 'cama solteiro', 'traveseiro',
           'colchao']

configuracao_ia = f"""
Você é um classificador de buscas para um site de móveis.
Sua única função é ler o que o usuário deseja e retornar quais filtros da lista abaixo combinam com o desejo dele.

LISTA DE FILTROS PERMITIDOS:
{filtros}

REGRAS CRÍTICAS:
1. RESPONDA APENAS OS FILTROS, SEPARADOS POR VÍRGULA.
2. NÃO dê explicações, NÃO peça desculpas, NÃO diga "Aqui estão os filtros".
3. Se o usuário pedir algo que não existe na lista, responda: "nenhum".
4. Se o usuário pedir algo que envolva mais de um filtro, mande todos (ex: "sofa, poltrona").
5. Analise a intenção: se ele disser "quero dormir", você manda "cama, colchao, travesseiro".
"""
genai.configure(api_key=chave_api)

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=configuracao_ia
)

response = model.generate_content("Gosto de sofa")

print(response.text)

def tranformar_pesquisa_em_filtro(pesquisa):
    pass