import sqlite3
from datetime import datetime

DATABASE = './database/vendas.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def insert_venda(produto, quantidade, preco):
    db = get_db()
    data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor = db.cursor()
    cursor.execute("INSERT INTO vendas (produto, quantidade, preco, data_venda) VALUES (?, ?, ?, ?)",
                   (produto, quantidade, preco, data_venda))
    db.commit()
    db.close()
    print(f"Venda de '{produto}' adicionada com sucesso!")

if __name__ == '__main__':
    insert_venda('Camiseta Azul', 2, 25.99)
    insert_venda('Calça Jeans', 1, 79.50)
    insert_venda('Vestido Floral', 3, 45.00)
    insert_venda('Tênis Esportivo', 1, 120.00)
    insert_venda('Meias (par)', 5, 9.90)
    print("\nDados de vendas de teste inseridos.")