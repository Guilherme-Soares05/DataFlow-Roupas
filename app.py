from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = './database/vendas.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def insert_venda(produto):
    db = get_db()
    data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor = db.cursor()
    cursor.execute("INSERT INTO vendas (produto, quantidade, preco, data_venda) VALUES (?, ?, ?, ?)",
                   (produto, 1, 0.00, data_venda)) # Preço 0 por simplicidade agora
    db.commit()
    db.close()
    print(f"Venda de '{produto}' registrada.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produto/<nome_produto>')
def exibir_produto(nome_produto):
    return render_template('produto.html', produto=nome_produto)

@app.route('/comprar', methods=['POST'])
def comprar_produto():
    data = request.get_json()
    produto = data.get('produto')
    if produto:
        insert_venda(produto)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Produto não especificado'}), 400

@app.route('/vendas', methods=['GET'])
def listar_vendas():
    db = get_db()
    vendas_db = db.execute("SELECT * FROM vendas").fetchall()
    db.close()
    vendas = [dict(row) for row in vendas_db]
    return jsonify(vendas)

if __name__ == '__main__':
    app.run(debug=True)