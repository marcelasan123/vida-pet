from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = ('chave secreta para os nao uçar')

tutores = []
pets = []
consultas = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastrartutor', methods=['GET', 'POST'])
def cadastrartutor():
    if request.method == 'POST':
        nome = request.form.get('nomeTutor')
        telefone = request.form.get('telefoneTutor')
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
            flash("A senha deve ter pelo menos uma letra maiúscula, minúscula, número e caractere especial.", 'danger')
            return redirect(url_for('cadastrartutor'))

        tutores.append({
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
                return redirect(url_for('cadastrarpet'))

        flash('Email ou senha incorretos!', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/cadastrarpet', methods=['GET', 'POST'])
def cadastrarpet():
    if request.method == 'POST':
        id = len(pets)
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

        flash('Pet cadastrado com sucesso!', 'success')
        return redirect(url_for('dadospets'))

    return render_template('cadastrarpet.html')


@app.route('/dadospets')
def dadospets():
    return render_template('dadospets.html', pets=pets)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 0 <= id < len(pets):
        if request.method == 'POST':
            pets[id]['nome_pet'] = request.form['nome']
            pets[id]['raca_pet'] = request.form['raca']
            pets[id]['peso_pet'] = request.form['peso']
            pets[id]['genero'] = request.form.get('sexo', '')
            flash('Dados do pet atualizados com sucesso!', 'success')
            return redirect(url_for('dadospets'))

        return render_template('editar.html', pets=pets[id], id=id)

    flash('Pet não encontrado!', 'danger')
    return redirect(url_for('dadospets'))


@app.route('/excluir/<int:id>')
def excluir(pet_id):
    if 0 <= pet_id < len(pets):
        pets.pop(pet_id)
        flash('Pet excluído com sucesso!', 'success')
    else:
        flash('Pet não encontrado!', 'danger')
    return redirect(url_for('dadospets'))


@app.route('/agendamento', methods=['GET', 'POST'])
def agendamento():
    if request.method == 'POST':
        id = len(consultas),
        nome = request.form['nome']
        celular = request.form['celular']
        email = request.form['email']
        especie = request.form['especie']
        data_hora = request.form['data_hora']
        nome_pet = request.form['nome_pet']

        consulta = {
            'nome': nome,
            'celular': celular,
            'email': email,
            'especie': especie,
            'data_hora': data_hora,
            'nome_pet': nome_pet
        }
        print(consultas)

        consultas.append(consulta)



        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('dadosconsultas'))

    return render_template('agendamento.html')


@app.route('/dadosconsultas', methods=['GET', 'POST'])
def dadosconsultas():
    return render_template('dadosconsultas.html', consultas=consultas)


@app.route('/calcularsoro', methods=['GET', 'POST'])
def calcularsoro():
    total = None
    if request.method == 'POST':
        nivel_soro = {
            'Leve' : 50,
            'Moderada': 75,
            'Grave': 100,
        }
        try:
            peso = float(request.form['peso'])
            quantidade = request.form['quantidade']
            if quantidade in nivel_soro:
                resultado = nivel_soro[quantidade] * peso
            total = (f"Quantidade de soro necessária: {resultado:.2f}ml")
        except ValueError:
            flash('Insira apenas números válidos.', 'danger')

    return render_template('calcularsoro.html', total=total)


@app.route('/calcularmedicamento', methods=['GET', 'POST'])
def calcularmedicamento():
    resultado = None
    if request.method == 'POST':
            peso = float(request.form['peso'])
            quantidades = float(request.form['quantidades'])
            total = peso * quantidades
            print(peso)
            print(quantidades)
            flash(f"Dosagem recomendada: {total:.2f}mg ")

    return render_template('calcularmedicamento.html', resultado=resultado)


if __name__ == '__main__':
    app.run(debug=True)
