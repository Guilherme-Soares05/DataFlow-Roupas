from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = './database/vendas.db' # Caminho para o nosso banco de dados SQLite

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/vendas', methods=['GET'])
def listar_vendas():
    db = get_db()
    vendas_db = db.execute("SELECT * FROM vendas").fetchall()
    db.close()
    vendas = [dict(row) for row in vendas_db] # Converter para uma lista de dicionários
    return jsonify(vendas)

if __name__ == '__main__':
    app.run(debug=True)