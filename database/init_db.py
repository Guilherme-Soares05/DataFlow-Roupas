import sqlite3

DATABASE = 'vendas.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return conn

def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados SQLite inicializado com sucesso!")