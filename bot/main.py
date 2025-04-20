from scraper import buscar_dados
from parser import extrair_dados


if __name__ == "__main__":
    html = buscar_dados()
    dados = extrair_dados(html)
