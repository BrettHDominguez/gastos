# crear_base_datos.py
import sqlite3

conn = sqlite3.connect('gastos.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,
    monto REAL NOT NULL,
    descripcion TEXT,
    fecha TEXT NOT NULL
)
''')

conn.commit()
conn.close()
