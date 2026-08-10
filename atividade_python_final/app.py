import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_super_segura'
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Decorador de proteção de rota
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Autenticação
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
            conn.commit()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('E-mail já cadastrado.')
        finally:
            conn.close()
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['senha'], senha):
            session['usuario_id'] = user['id']
            session['usuario_nome'] = user['nome']
            return redirect(url_for('dashboard'))
        flash('Credenciais inválidas.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard e CRUD
@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    # Integração com API externa
    frase = "Sem frase disponível no momento."
    try:
        res = requests.get('https://api.adviceslip.com/advice', timeout=3).json()
        frase = res['slip']['advice']
    except Exception:
        pass

    conn = get_db()
    tarefas = conn.execute(
        'SELECT * FROM tarefas WHERE usuario_id = ?', (session['usuario_id'],)
    ).fetchall()
    conn.close()
    
    return render_template('dashboard.html', tarefas=tarefas, frase=frase)

@app.route('/nova_tarefa', methods=['GET', 'POST'])
@login_required
def nova_tarefa():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        status = request.form['status']
        
        conn = get_db()
        conn.execute(
            'INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)',
            (titulo, descricao, status, session['usuario_id'])
        )
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('form_tarefa.html', tarefa=None)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_tarefa(id):
    conn = get_db()
    tarefa = conn.execute(
        'SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?', (id, session['usuario_id'])
    ).fetchone()

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        status = request.form['status']
        
        conn.execute(
            'UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ? AND usuario_id = ?',
            (titulo, descricao, status, id, session['usuario_id'])
        )
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
        
    conn.close()
    return render_template('form_tarefa.html', tarefa=tarefa)

@app.route('/excluir/<int:id>')
@login_required
def excluir_tarefa(id):
    conn = get_db()
    conn.execute('DELETE FROM tarefas WHERE id = ? AND usuario_id = ?', (id, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# Endpoints JSON (Filtros, Graficos e API REST)
@app.route('/api/tarefas')
@login_required
def api_tarefas():
    status_filter = request.args.get('status')
    conn = get_db()
    if status_filter:
        tarefas = conn.execute(
            'SELECT * FROM tarefas WHERE usuario_id = ? AND status = ?', (session['usuario_id'], status_filter)
        ).fetchall()
    else:
        tarefas = conn.execute(
            'SELECT * FROM tarefas WHERE usuario_id = ?', (session['usuario_id'],)
        ).fetchall()
    conn.close()
    return jsonify([dict(t) for t in tarefas])

@app.route('/api/estatisticas')
@login_required
def api_estatisticas():
    conn = get_db()
    pendentes = conn.execute('SELECT COUNT(*) FROM tarefas WHERE usuario_id = ? AND status = "Pendente"', (session['usuario_id'],)).fetchone()[0]
    andamento = conn.execute('SELECT COUNT(*) FROM tarefas WHERE usuario_id = ? AND status = "Em andamento"', (session['usuario_id'],)).fetchone()[0]
    concluidas = conn.execute('SELECT COUNT(*) FROM tarefas WHERE usuario_id = ? AND status = "Concluída"', (session['usuario_id'],)).fetchone()[0]
    conn.close()
    return jsonify({'pendentes': pendentes, 'andamento': andamento, 'concluidas': concluidas})

@app.route('/progresso')
@login_required
def progresso():
    return render_template('progresso.html')

if __name__ == '__main__':
    app.run(debug=False)