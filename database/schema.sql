DROP TABLE IF EXISTS vendas;

CREATE TABLE vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    data_venda TEXT NOT NULL
);