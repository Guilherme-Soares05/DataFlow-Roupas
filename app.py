from flask import Flask, render_template, jsonify, request
import psycopg2
from datetime import datetime

app = Flask(__name__)

DATABASE_URL = "postgresql://dataflow:password@db:5432/dataflow_db"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def insert_venda(produto):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO vendas (produto, quantidade, preco, data_venda) VALUES (%s, %s, %s, NOW())",
                (produto, 1, 0.00,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Venda de '{produto}' registrada.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produto/<nome_produto>')
def exibir_produto(nome_produto):
    return render_template('produto.html', produto=nome_produto)

@app.route('/comprar/<nome_produto>', methods=['POST'])
def comprar_produto(nome_produto):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        data = request.get_json()
        quantidade = data.get('quantidade')
        preco = data.get('preco')

        if quantidade is None or preco is None:
            return jsonify({'error': 'Quantidade e preço são obrigatórios.'}), 400

        cur.execute("INSERT INTO vendas (produto, quantidade, preco, data_venda) VALUES (%s, %s, %s, NOW())", (nome_produto, quantidade, preco))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': f'{quantidade} unidades de {nome_produto} compradas com sucesso!'}), 201
    except psycopg2.Error as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/vendas', methods=['GET'])
def listar_vendas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, produto, quantidade, preco, data_venda FROM vendas")
    vendas = cur.fetchall()
    cur.close()
    conn.close()
    vendas_list = []
    for venda in vendas:
        vendas_list.append({
            'id': venda[0],
            'produto': venda[1],
            'quantidade': venda[2],
            'preco': venda[3],
            'data_venda': venda[4].isoformat() if venda[4] else None
        })
    return jsonify(vendas_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)