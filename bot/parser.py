import json
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime


def extrair_dados(html):
    soup = BeautifulSoup(html, "html.parser")

    # Extrair da tabela
    tabela = soup.find("table", {"id": "tabela-visao-geral-sancoes"})
    dados_tabela = []

    if tabela:
        linhas = tabela.find("tbody").find_all("tr")
        for linha in linhas:
            colunas = linha.find_all("td")
            if len(colunas) >= 4:
                nis = colunas[1].get_text(strip=True)
                nome = colunas[2].get_text(strip=True)
                valor = colunas[3].get_text(strip=True)
                dados_tabela.append({
                    "nis": nis,
                    "nome": nome,
                    "valor_recebido": valor
                })

    # Extrair CPF e Localidade
    dados_secao = soup.find("section", {"class": "dados-tabelados"})
    cpf = localidade = nome_completo = None

    if dados_secao:
        campos = dados_secao.find_all("div", class_="col-xs-12")
        for campo in campos:
            strong = campo.find("strong")
            span = campo.find("span")
            if strong and span:
                titulo = strong.get_text(strip=True).lower()
                valor = span.get_text(strip=True)
                if "cpf" in titulo:
                    cpf = valor
                elif "localidade" in titulo:
                    localidade = valor
                elif "nome" in titulo:
                    nome_completo = valor

    _href = soup.find("a", {"id": "btnDetalharBpc"})

    resultado = {
        "cpf": cpf,
        "localidade": localidade,
        "nome_completo": nome_completo,
        "beneficios": dados_tabela,
        "detalhes": []
    }

    # Salvar no JSON
    data_path = Path("../data")
    data_path.mkdir(parents=True, exist_ok=True)
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(data_path / f"{nome_completo.replace(' ', '_')}_dados_extraidos_{date}.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)
