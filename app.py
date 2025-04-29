import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

# Conexión a la base de datos
conn = sqlite3.connect('gastos.db')
c = conn.cursor()

# Función para crear la base de datos y las tablas necesarias
def crear_base_datos():
    c.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
    ''')

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

# Función para registrar un nuevo gasto
def registrar_gasto(categoria, monto, descripcion, fecha):
    if monto <= 0:
        st.error("El monto debe ser mayor a 0.")
        return

    # Insertar gasto en la base de datos
    c.execute('INSERT INTO gastos (categoria, monto, descripcion, fecha) VALUES (?, ?, ?, ?)', 
              (categoria, monto, descripcion, fecha))
    conn.commit()
    st.success("¡Gasto registrado con éxito!")

# Función para mostrar los gastos en una tabla
def mostrar_gastos():
    c.execute('SELECT id, categoria, monto, descripcion, fecha FROM gastos')
    gastos = c.fetchall()

    if gastos:
        df = pd.DataFrame(gastos, columns=["ID", "Categoría", "Monto", "Descripción", "Fecha"])
        df['Monto'] = df['Monto'].apply(lambda x: f"${x:,.2f}")  # Formato de monto con signo $
        st.write("### Lista de Gastos Registrados")
        st.table(df)

        # Opción para eliminar un gasto
        st.write("### Eliminar un Gasto")
        gasto_a_eliminar = st.selectbox("Selecciona el gasto a eliminar", [""] + [f"{gasto[1]} - {gasto[3]} - {gasto[4]}" for gasto in gastos])
        
        if gasto_a_eliminar:
            gasto_id = gastos[[f"{gasto[1]} - {gasto[3]} - {gasto[4]}" for gasto in gastos].index(gasto_a_eliminar)][0]
            if st.button(f"Eliminar gasto {gasto_a_eliminar}"):
                eliminar_gasto(gasto_id)
                st.success("¡Gasto eliminado con éxito!")
                mostrar_gastos()  # Mostrar los gastos nuevamente después de la eliminación
    else:
        st.write("No tienes gastos registrados.")

# Función para eliminar un gasto
def eliminar_gasto(gasto_id):
    c.execute('DELETE FROM gastos WHERE id = ?', (gasto_id,))
    conn.commit()

# Función para calcular la suma de los gastos
def calcular_suma_gastos():
    c.execute('SELECT SUM(monto) FROM gastos')
    suma = c.fetchone()[0]
    return suma if suma else 0.0

# Función para agregar una nueva categoría
def agregar_categoria(categoria):
    c.execute('INSERT INTO categorias (nombre) VALUES (?)', (categoria,))
    conn.commit()

# Función principal de la aplicación
def main():
    st.title("GASTOS FAMILIA DOMINGUEZ ALAMILLA")
    
    # Disposición del layout con columnas
    col1, col2 = st.columns([3, 1])
    
    # Mostrar los gastos y la suma total
    with col1:
        mostrar_gastos()
        st.write(f"**Total de Gastos: ${calcular_suma_gastos():,.2f}**")

    # Registrar un nuevo gasto
    with col2:
        st.subheader("Nuevo Gasto")
        
        # Entrada para categoría (con selección o personalización)
        categorias = []
        c.execute('SELECT nombre FROM categorias')
        categorias_db = c.fetchall()
        if categorias_db:
            categorias = [cat[0] for cat in categorias_db]
        
        categoria = st.selectbox("Selecciona una categoría", categorias + ["Otra (Agregar nueva)"])

        # Si se elige "Otra", permitir agregar una nueva categoría
        if categoria == "Otra (Agregar nueva)":
            nueva_categoria = st.text_input("Nombre de la nueva categoría")
            if nueva_categoria:
                agregar_categoria(nueva_categoria)
                categoria = nueva_categoria

        monto = st.number_input("Monto", min_value=0.01, format="%.2f")
        descripcion = st.text_area("Descripción")
        fecha = st.date_input("Fecha", value=datetime.today())

        if st.button("Registrar Gasto"):
            if categoria and monto > 0 and fecha:
                registrar_gasto(categoria, monto, descripcion, str(fecha))
            else:
                st.error("Por favor, completa todos los campos del gasto.")

# Crear las tablas necesarias si no existen
crear_base_datos()

# Ejecutar la aplicación
if __name__ == '__main__':
    main()
