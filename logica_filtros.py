from dotenv import load_dotenv
import os

load_dotenv()

chave_api = os.getenv("CHAVE_API")
print(chave_api)

filtros = ['poltrona', 'piscina', 'sofa', 'cama', 'cama casal', 'cama solteiro', 'traveseiro',
           'colchao']

def tranformar_pesquisa_em_filtro(pesquisa):
    pass