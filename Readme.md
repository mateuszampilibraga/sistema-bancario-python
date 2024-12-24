# Sistema Bancário com Python e Flask

## Descrição

Este projeto foi desenvolvido como parte de um desafio prático da DIO, focado na criação de um sistema bancário simples utilizando **Python** e o framework **Flask**. O objetivo é criar um sistema que permita o gerenciamento de contas bancárias, incluindo funcionalidades como depósito, saque e visualização de extratos. O sistema também implementa limitações como o número máximo de saques diários e a validação de transações para garantir um comportamento financeiro seguro e confiável.

## Funcionalidades

- **Criar Conta Bancária**: O sistema inicializa com um saldo de R$ 0,00 e um limite de saque de R$ 500,00.
- **Depositar**: Permite ao usuário adicionar valores ao saldo da conta.
- **Sacar**: Realiza saques, respeitando o limite de saldo e o número máximo de saques diários (3).
- **Extrato**: Exibe um extrato das últimas transações realizadas.
- **Validação**: Valida depósitos e saques com mensagens de erro detalhadas, como valores inválidos, saldo insuficiente e limite de saques atingido.

## Tecnologias Utilizadas

- **Python 3.x**
- **Flask** (Framework web para Python)
- **HTML/CSS** (para renderização de páginas web)

## Estrutura do Projeto

- `app.py`: Arquivo principal que contém a lógica do servidor Flask.
- `templates/`: Diretório que contém os arquivos HTML para renderizar as páginas da web.
  - `index.html`: Página principal onde os depósitos, saques e saldo são exibidos.
  - `extrato.html`: Página para visualização do extrato bancário.
  
## Como Rodar o Projeto

### Pré-requisitos

Certifique-se de ter o **Python 3.x** instalado em sua máquina. Para instalar o Flask, use o seguinte comando:

```bash
pip install flask
```

### Executando o Servidor

1. Clone este repositório para sua máquina local:

```bash
git clone https://github.com/mateuszampilibraga/sistema-bancario-python.git
```

2. Navegue até o diretório do projeto:

```bash
cd nome-do-repositorio
```

3. Execute o aplicativo Flask:

```bash
python app.py
```

O servidor estará disponível em `http://127.0.0.1:5000/`.

### Acessando o Sistema

- Na página principal, você pode realizar depósitos, saques e visualizar o saldo.
- A página de extrato exibe todas as transações realizadas.

## Melhorias Possíveis

- Adicionar autenticação de usuários para proteger as contas.
- Armazenar dados de transações em um banco de dados para persistência.
- Implementar diferentes tipos de conta com funcionalidades específicas (por exemplo, contas poupança).
- Melhorar a interface de usuário com JavaScript e CSS.

## Contribuindo

Sinta-se à vontade para fazer um **fork** deste repositório e enviar **pull requests** com melhorias ou correções.