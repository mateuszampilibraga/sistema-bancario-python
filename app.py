from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

@app.route('/')
def index():
    return render_template('index.html', saldo=saldo, limite=limite, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES)

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

    return render_template('index.html', saldo=saldo, limite=limite, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES, mensagem=mensagem)

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

    return render_template('index.html', saldo=saldo, limite=limite, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES, mensagem=mensagem)

@app.route('/extrato')
def ver_extrato():
    global extrato
    extrato_exibido = extrato if extrato else "Não foram realizadas movimentações."
    return render_template('extrato.html', saldo=saldo, extrato=extrato_exibido)

if __name__ == "__main__":
    app.run(debug=True)
