from playwright.sync_api import sync_playwright
import os
from datetime import datetime
from solve_captcha import solve
import requests
from bs4 import BeautifulSoup


def take_screenshot(page, filename="screenshot"):
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("../data", exist_ok=True)
    _filename = f"{filename}_{date}.png"
    page.screenshot(path=f"../data/{_filename}")


def handle_cookies(page):
    try:
        page.locator('#accept-all-btn').wait_for(timeout=5000)
        print("Aceitar cookies encontrado. Clicando...")
        page.click("#accept-all-btn")
    except TimeoutError:
        # Screenshot antes de tentar localizar o campo
        take_screenshot(page, "erro_timeout_cookies")
        pass


def buscar_dados():
    with sync_playwright() as p:
        input_value = str(input("Digite o nome da pessoa: "))
        print("Iniciando o Playwright...")

        url = "https://portaldatransparencia.gov.br/pessoa-fisica/busca/lista?pagina=1&tamanhoPagina=10"
        
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        page = context.new_page()

        page.goto(url, wait_until="networkidle")

        print("Acessando o site...")

        # Verifica se o botão "Aceitar todos" existe e está visível
        try:
            handle_cookies(page)
        except:
            pass

        # Preencher termo de busca
        page.locator('input#termo').wait_for(state="visible")
        page.fill('input#termo', input_value)

        print("Preenchendo o termo de busca...")

        # Marcar filtro "Beneficiário de Programa Social"
        page.click('#accordion1')
        checkbox = page.locator('#beneficiarioProgramaSocial')
        checkbox.scroll_into_view_if_needed()
        page.evaluate("document.querySelector('#beneficiarioProgramaSocial').click()")

        # Clicar no botão de buscar
        page.click('#btnConsultarPF')

        print("Clicando no botão de buscar...")

        # Esperar os resultados aparecerem
        page.wait_for_selector('a.link-busca-nome')

        try:
            handle_cookies(page)
        except:
            pass

        print("Resultados encontrados primeira pagina!")

        # Pegando o primeiro link
        primeiro_link = page.locator('a.link-busca-nome').first
        # texto = primeiro_link.inner_text()
        # href = primeiro_link.get_attribute('href')

        # Clicar e esperar os detalhes carregarem
        primeiro_link.click()
        page.wait_for_load_state('networkidle')

        try:
            handle_cookies(page)
        except:
            pass

        # Recebimento de Recursos
        page.click('#accordion1')
        
        # Screenshot
        take_screenshot(page, f"{input_value}_recebimento_recursos")


        # Devido aos captchas que podem aparecer, é necessário esperar um pouco mais de codigo para resolver e algumas opcões que sao pagas.
        # # Detalhes do BPC
        # page.click('#btnDetalharBpc')

        # try:
        #     handle_cookies(page)
        # except:
        #     pass

        # try:
        #     page.locator('#amzn-captcha-verify-button').wait_for(state="visible", timeout=5000)
        #     print("Captcha encontrado. Resolvendo...")
        #     page.wait_for_selector('#amzn-btn-verify-internal')
        #     iv = page.get_attribute('input[name="iv"]', 'value')
        #     cp_context = page.get_attribute('input[name="context"]', 'value')
        #     sitekey = page.get_attribute('#captcha-box', 'data-sitekey')
        #     solve(page.url, sitekey, iv, cp_context)
        #     take_screenshot(page, f"{input_value}_captcha")
        # except:
        #     pass

        # page.wait_for_selector('.dados-detalhados')


        # Pegar o HTML da página
        html = page.content()

        browser.close()
        return html


def scrape_table_from_href(href: str) -> list[dict]:
    url = f"https://portaldatransparencia.gov.br{href}?ordenarPor=mesFolha&direcao=desc"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'id': 'tabelaDetalhe'})
    if not table:
        raise ValueError("Nenhuma tabela encontrada na página.")

    headers = [th.text.strip() for th in table.find_all('th')]
    if not headers:
        raise ValueError("A tabela não possui cabeçalhos (th).")

    data = []
    for row in table.find_all('tr')[1:]:  # Pula o cabeçalho
        cells = [td.text.strip() for td in row.find_all(['td', 'th'])]
        if len(cells) == len(headers):
            data.append(dict(zip(headers, cells)))
        else:
            continue

    return data
