import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('gastos.db')
c = conn.cursor()

# Crear tabla de usuarios
c.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Crear tabla de categorías
c.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_categoria TEXT NOT NULL
)
''')

# Crear tabla de gastos (incluyendo referencia al usuario)
c.execute('''
CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    categoria TEXT NOT NULL,
    monto REAL NOT NULL,
    descripcion TEXT,
    fecha TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
)
''')

conn.commit()
conn.close()

