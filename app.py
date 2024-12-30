from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Necessário para usar sessões

# Dados fictícios de usuários
usuarios = {
    'user1': {'senha': 'senha1', 'nome': 'João Silva', 'cpf': '123.456.789-00', 'endereco': 'Rua A, 123',
              'telefone': '999999999', 'email': 'joao@exemplo.com'},
    'user2': {'senha': 'senha2', 'nome': 'Maria Oliveira', 'cpf': '987.654.321-00', 'endereco': 'Avenida B, 456',
              'telefone': '988888888', 'email': 'maria@exemplo.com'}
}
contas = {
    'user1': ['Conta Corrente - 12345-6', 'Poupança - 78901-2'],
    'user2': ['Conta Corrente - 56789-0']
}

# Variáveis globais da aplicação
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# Função de logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Remove 'usuario' da sessão
    session.pop('conta', None)    # Remove 'conta' da sessão
    return redirect(url_for('login'))  # Redireciona para o login

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def autenticar():
    username = request.form['username']
    password = request.form['password']

    if username in usuarios:
        if usuarios[username]['senha'] == password:
            session['usuario'] = username
            print(session)  # Verifica o conteúdo da sessão
            return redirect(url_for('selecionar_conta'))
        else:
            mensagem = "Senha incorreta. Tente novamente."
            return render_template('login.html', mensagem=mensagem)
    else:
        mensagem = "Usuário não encontrado. Tente novamente."
        return render_template('login.html', mensagem=mensagem)


@app.route('/registrar')
def registrar():
    return render_template('registrar.html')


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    username = request.form['username']
    password = request.form['password']
    nome = request.form['nome']
    cpf = request.form['cpf']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    email = request.form['email']

    # Verifica se o usuário já existe
    if username in usuarios:
        mensagem = "Nome de usuário já existe. Tente outro."
        return render_template('registrar.html', mensagem=mensagem)

    # Registra o novo usuário com os dados completos
    usuarios[username] = {
        'senha': password,
        'nome': nome,
        'cpf': cpf,
        'endereco': endereco,
        'telefone': telefone,
        'email': email
    }
    contas[username] = []  # Novo usuário começa sem contas
    session['usuario'] = username
    return redirect(url_for('login'))


@app.route('/selecionar_conta')
def selecionar_conta():
    # Verifica se o usuário está autenticado (sessão ativa)


    usuario = session['usuario']  # Acessa o usuário autenticado na sessão
    lista_contas = contas.get(usuario, [])  # Recupera as contas associadas ao usuário
    return render_template('selecionar_conta.html', contas=lista_contas)


@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('login'))

    if request.method == 'POST':
        tipo_conta = request.form['tipo_conta']

        # Gerar número da conta automaticamente
        numero_conta = f"{usuario[:3].upper()}-{str(len(contas[usuario]) + 1).zfill(4)}"  # Exemplo: "USE-0001"

        # Adicionar a nova conta à lista de contas do usuário
        nova_conta = f"{tipo_conta} - {numero_conta}"
        contas[usuario].append(nova_conta)

        mensagem = f"Conta {tipo_conta} criada com sucesso! Número da conta: {numero_conta}"
        return render_template('selecionar_conta.html', contas=contas[usuario], mensagem=mensagem)

    return render_template('criar_conta.html')


@app.route('/conta_selecionada', methods=['POST'])
def conta_selecionada():
    session['conta'] = request.form['conta']
    return redirect(url_for('index'))


@app.route('/principal')
def index():
    conta = session.get('conta')
    if not conta:
        return redirect(url_for('selecionar_conta'))

    return render_template('index.html', saldo=saldo, limite=limite,
                           numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES,
                           conta=conta)


@app.route('/depositar', methods=['POST'])
def depositar():
    global saldo, extrato
    valor = float(request.form['valor'])

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        mensagem = "Depósito realizado com sucesso!"
    else:
        mensagem = "Operação falhou! O valor informado é inválido."

    return redirect(url_for('index'))


@app.route('/sacar', methods=['POST'])
def sacar():
    global saldo, extrato, numero_saques
    valor = float(request.form['valor'])

    if valor <= 0:
        mensagem = "Operação falhou! O valor informado é inválido."
    elif valor > saldo:
        mensagem = "Operação falhou! Você não tem saldo suficiente."
    elif valor > limite:
        mensagem = "Operação falhou! O valor do saque excede o limite."
    elif numero_saques >= LIMITE_SAQUES:
        mensagem = "Operação falhou! Número máximo de saques excedido."
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        mensagem = "Saque realizado com sucesso!"

    return redirect(url_for('index'))


@app.route('/extrato')
def ver_extrato():
    global extrato
    conta = session.get('conta')
    if not conta:
        return redirect(url_for('selecionar_conta'))

    extrato_exibido = extrato if extrato else "Não foram realizadas movimentações."
    return render_template('extrato.html', saldo=saldo, extrato=extrato_exibido, conta=conta)


if __name__ == "__main__":
    app.run(debug=True)
