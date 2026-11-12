from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# === Inicializar banco de dados ===
def init_db():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            concluida INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# === Página principal — mostra todas as tarefas ===
@app.route('/')
def index():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas ORDER BY id DESC')
    tarefas = cursor.fetchall()
    conn.close()
    return render_template('index.html', tarefas=tarefas)

# === Adicionar nova tarefa ===
@app.route('/adicionar', methods=['POST'])
def adicionar():
    titulo = request.form['titulo'].strip()
    if titulo:
        conn = sqlite3.connect('tarefas.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tarefas (titulo) VALUES (?)', (titulo,))
        conn.commit()
        conn.close()
    return redirect('/')

# === Marcar como concluída / não concluída ===
@app.route('/alternar/<int:id>')
def alternar(id):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT concluida FROM tarefas WHERE id = ?', (id,))
    status = cursor.fetchone()[0]
    novo_status = 0 if status == 1 else 1
    cursor.execute('UPDATE tarefas SET concluida = ? WHERE id = ?', (novo_status, id))
    conn.commit()
    conn.close()
    return redirect('/')

# === Excluir tarefa ===
@app.route('/excluir/<int:id>')
def excluir(id):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
