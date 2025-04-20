# mostqi-python

# Estrutura Sugerida do Projeto

## Bot via terminal

```bash
mostqi-python/
│
├── bot/
│   ├── __init__.py
│   ├── main.py             # ponto de entrada
│   ├── scraper.py          # lógica de scraping com playwright
│   └──  parser.py           # limpeza e transformação dos dados
│
├── tests/
│   └── test_scraper.py     # testes com pytest
│
├── data/
│   └── output.json         # saída dos dados
│
├── requirements.txt
└── README.md
```

## Instalação

Para utilizar é necessário que você tenha o Docker instalado e configurado, tendo isso basta rodar o comando abaixo e acessar a URL `http://localhost:8080/apidocs/` para ter acesso a automação.

```bash
docker compose up --build
```

## Como utilizar

Após executar o build do container, no terminal vai aparecer uma solicitação para você adicionar o nome, NIS ou CPF desejado. Feito isso a automação será iniciado e dentro do diretório data você vai encontrar as informações que foram geradas, sendo elas:

- Screenshot da tela de beneficio;
- JSON com os dados requisitados.

# Desafios enfrentados

1 - O xPath do Termo estava excedendo o timeout por não estar visível devido a um erro de permissao 403.
> A solução foi adicionar `user_agent`.

2 - Problemas com o checkbox.
> Foi solucionado forçando a marcação do item com javascript.

3 - Devido ao site identificar que era uma automação o mesmo começou a apresentar uma verificação via captcha.
> Solucao criar uma funcao que resolve o mesmo utilizando uma API de terceiro no entando como é paga deixei desabilitada.

> Outra solução seria utilizar o propio Soup resgatando os dados utilizando após obter o content da pagina anterior e obter o href do botão detalhar e assim fazendo uma requisição para a página e obtendo os detalhes e extraindo as informações. Não foi implementado devido a falta de tempo.
