CREATE TABLE IF NOT EXISTS vendas (
    id SERIAL PRIMARY KEY,
    produto VARCHAR(255) NOT NULL,
    quantidade INTEGER NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    data_venda TIMESTAMP DEFAULT NOW()
);