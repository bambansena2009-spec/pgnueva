CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS service (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    price NUMERIC(12,2) NOT NULL DEFAULT 0,
    category VARCHAR(80) NOT NULL DEFAULT 'General',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO service (name, description, price, category) VALUES
('Diseño Creativo', 'Diseño de interfaces modernas para proyectos digitales.', 250000, 'Diseño'),
('Desarrollo Web', 'Construcción de páginas web responsive con tecnologías actuales.', 650000, 'Desarrollo'),
('Automatización', 'Implementación de soluciones para optimizar procesos digitales.', 450000, 'Tecnología')
ON CONFLICT DO NOTHING;
