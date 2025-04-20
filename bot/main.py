from scraper import buscar_dados
from parser import extrair_dados
from exporter import salvar_json


if __name__ == "__main__":
    html = buscar_dados()
    dados = extrair_dados(html)
    # salvar_json(dados, "data/output.json")
