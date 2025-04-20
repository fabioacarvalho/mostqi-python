#!/bin/bash

# Ativar o modo de erro
set -e

echo "Criando ambiente virtual..."
python3 -m venv venv

echo "Ativando o ambiente virtual..."
source venv/bin/activate

echo "Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Agora sá rodar o bot..."