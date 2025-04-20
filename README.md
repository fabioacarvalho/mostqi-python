# mostqi-python

# Estrutura Sugerida do Projeto

```bash
mostqi-python/
│
├── bot/
│   ├── __init__.py
│   ├── main.py             # ponto de entrada
│   ├── scraper.py          # lógica de scraping com playwright
│   ├── parser.py           # limpeza e transformação dos dados
│   └── exporter.py         # exporta para JSON, CSV, etc.
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


# Problemas enfretados

1 - O xPath do Termo estava excedendo o timeout por nao estar visível devido a um erro de permissao 403 e a solução foi adicionar `user_agent`.

2 - Problemas com o checkbox e solucionado com o `page.check()`.

