from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'chave secreta para os nao uçar'

tutores = []
pets = []
agendamento = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrartutor', methods=['GET', 'POST'])
def cadastrartutor():
    if request.method == 'POST':
        codigo = len(tutores) + 1
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmaSenha')

        if confirmar_senha != senha:
            flash("As senhas não coincidem!", 'danger')
            return redirect(url_for('cadastrartutor'))

        maiuscula = any(c.isupper() for c in senha)
        minuscula = any(c.islower() for c in senha)
        numero = any(c.isdigit() for c in senha)
        especial = any(not c.isalnum() for c in senha)

        if not (maiuscula and minuscula and numero and especial):
            flash("A senha deve conter maiúscula, minúscula, número e caractere especial.", 'danger')
            return redirect(url_for('cadastrartutor'))

        tutores.append({
            'codigo': codigo,
            'nome': nome,
            'telefone': telefone,
            'email': email,
            'senha': senha
        })

        flash('Tutor cadastrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastrartutor.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        for tutor in tutores:
            if tutor['email'] == email and tutor['senha'] == senha:
                flash('Login realizado com sucesso!', 'success')
                return render_template('lista_usuario.html', tutores=tutores)

        flash('Email ou senha incorretos!', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/cadastrarpet', methods=['GET', 'POST'])
def cadastrarpet():
    if request.method == 'POST':
        id = len(pets) + 1
        nome_pet = request.form.get('nome_pet')
        raca_pet = request.form.get('raca_pet')
        peso_pet = request.form.get('peso_pet')
        genero = request.form.get('genero')
        nome_tutor = request.form.get('nome_tutor')
        telefone_tutor = request.form.get('telefone_tutor')

        pets.append({
            'id': id,
            'nome_pet': nome_pet,
            'raca_pet': raca_pet,
            'peso_pet': peso_pet,
            'genero': genero,
            'nome_tutor': nome_tutor,
            'telefone_tutor': telefone_tutor
        })

        flash("Pet cadastrado com sucesso!")
        return redirect(url_for('dadospets'))

    return render_template('cadastrarpet.html')

@app.route('/lista_pet')
def dadospets():
    return render_template('lista_pet.html', pets=pets, agendamentos=agendamentos)

@app.route('/editar_pet/<int:id>', methods=['GET', 'POST'])
def editar_pet(id):
    pet = next((p for p in pets if p['id'] == id), None)
    if not pet:
        flash('Pet não encontrado!', 'danger')
        return redirect(url_for('dadospets'))

    if request.method == 'POST':
        pet['nome_pet'] = request.form.get('nome_pet')
        pet['raca_pet'] = request.form.get('raca_pet')
        pet['peso_pet'] = request.form.get('peso_pet')
        pet['genero'] = request.form.get('genero')
        pet['nome_tutor'] = request.form.get('nome_tutor')
        pet['telefone_tutor'] = request.form.get('telefone_tutor')
        flash('Pet atualizado com sucesso!', 'success')
        return redirect(url_for('dadospets'))

    return render_template('editarpet.html', pet=pet)

@app.route('/excluir/<int:id>')
def excluir(id):
    global pets
    pet = next((p for p in pets if p['id'] == id), None)
    if pet:
        pets.remove(pet)
        flash('Pet excluído com sucesso!', 'success')
    else:
        flash('Pet não encontrado!', 'danger')

    if len(pets) == 0:
        return redirect(url_for('cadastrarpet'))
    return redirect(url_for('dadospets'))

@app.route('/agendar/<int:pet_id>', methods=['GET', 'POST'])
def agendar(pet_id):
    pet = next((p for p in pets if p['id'] == pet_id), None)
    if not pet:
        flash('Pet não encontrado!', 'danger')
        return redirect(url_for('lista_pet'))

    if request.method == 'POST':
        data = request.form.get('data')
        motivo = request.form.get('motivo')

        if not data or not motivo:
            flash('Preencha todos os campos!', 'danger')
            return redirect(url_for('agendar', pet_id=pet_id))

        agendamentos.append({
            'pet_id': pet_id,
            'nome_pet': pet['nome_pet'],
            'data': data,
            'motivo': motivo
        })

        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('lista_pet'))

    return render_template('agendar.html', pet=pet)

@app.route('/calcularsoro', methods=['GET', 'POST'])
def calcularsoro():
    total = None
    if request.method == 'POST':
        nivel_soro = {'Leve': 50, 'Moderada': 75, 'Grave': 100}
        try:
            peso = float(request.form['peso'])
            quantidade = request.form['quantidade']
            if quantidade in nivel_soro:
                resultado = nivel_soro[quantidade] * peso
                total = f"Quantidade de soro necessária: {resultado:.2f}ml"
        except ValueError:
            flash('Insira apenas números válidos.', 'danger')
    return render_template('calcularsoro.html', total=total)

@app.route('/calcularmedicamento', methods=['GET', 'POST'])
def calcularmedicamento():
    resultado = None
    if request.method == 'POST':
        try:
            peso = float(request.form['peso'])
            quantidades = float(request.form['quantidades'])
            total = peso * quantidades
            flash(f"Dosagem recomendada: {total:.2f}mg")
        except ValueError:
            flash("Insira valores válidos.", 'danger')
    return render_template('calcularmedicamento.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)