import psycopg2

DATABASE_URL = "postgresql://dataflow:password@db:5432/dataflow_db"

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Execute o schema.sql para criar a tabela
    with open('database/schema.sql', 'r') as f:
        cur.execute(f.read())

    # Inserir alguns dados de exemplo
    cur.execute("INSERT INTO vendas (produto, quantidade, preco) VALUES (%s, %s, %s)", ('Camiseta', 10, 29.99))
    cur.execute("INSERT INTO vendas (produto, quantidade, preco) VALUES (%s, %s, %s)", ('Calça Jeans', 5, 59.99))
    cur.execute("INSERT INTO vendas (produto, quantidade, preco) VALUES (%s, %s, %s)", ('Tênis', 8, 89.99))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado com sucesso!")