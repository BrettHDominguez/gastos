import sqlite3

# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect('gastos.db')
c = conn.cursor()

# Crear tabla de usuarios si no existe
c.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Crear tabla de gastos si no existe
c.execute('''
CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,
    monto REAL NOT NULL,
    descripcion TEXT,
    fecha TEXT NOT NULL,
    usuario_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
''')

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()
