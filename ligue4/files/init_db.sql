
-- Criação da tabela para armazenar as jogadas
CREATE TABLE jogadas (
    id SERIAL PRIMARY KEY,
    jogador_id INTEGER NOT NULL,
    coluna INTEGER NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
