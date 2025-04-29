import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('gastos.db')
    return conn

# Función para registrar un nuevo usuario
def registrar_usuario(nombre, email, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)', (nombre, email, password))
    conn.commit()
    conn.close()

# Función para verificar si el usuario existe
def login_usuario(email, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE email = ? AND password = ?', (email, password))
    user = c.fetchone()
    conn.close()
    return user

# Función para mostrar y actualizar las categorías
def mostrar_categorias():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM categorias')
    categorias = c.fetchall()
    conn.close()
    return [categoria[1] for categoria in categorias]

def agregar_categoria(nueva_categoria):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO categorias (nombre_categoria) VALUES (?)', (nueva_categoria,))
    conn.commit()
    conn.close()

# Función para agregar un gasto
def agregar_gasto(id_usuario, categoria, monto, descripcion, fecha):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO gastos (id_usuario, categoria, monto, descripcion, fecha) VALUES (?, ?, ?, ?, ?)', 
              (id_usuario, categoria, monto, descripcion, fecha))
    conn.commit()
    conn.close()

# Interfaz de usuario
st.title("App de Seguimiento de Gastos Personales")

# Página de inicio
opcion = st.selectbox('Selecciona una opción:', ['Iniciar sesión', 'Registrarse'])

if opcion == 'Iniciar sesión':
    email = st.text_input('Email')
    password = st.text_input('Contraseña', type='password')
    if st.button('Iniciar sesión'):
        usuario = login_usuario(email, password)
        if usuario:
            st.success('¡Bienvenido, ' + usuario[1] + '!')
            st.session_state.usuario_id = usuario[0]  # Guardamos el ID del usuario en la sesión

            # Mostrar categorías existentes
            categorias = mostrar_categorias()
            categoria = st.selectbox('Selecciona una categoría:', categorias)
            monto = st.number_input('Monto', min_value=0.0, step=0.1)
            descripcion = st.text_area('Descripción')
            fecha = st.date_input('Fecha', value=datetime.today())

            if st.button('Agregar Gasto'):
                agregar_gasto(st.session_state.usuario_id, categoria, monto, descripcion, str(fecha))
                st.success('Gasto registrado correctamente.')

            # Opción para agregar nuevas categorías
            nueva_categoria = st.text_input('Agregar nueva categoría')
            if st.button('Agregar Categoría'):
                agregar_categoria(nueva_categoria)
                st.success(f'Categoría "{nueva_categoria}" agregada correctamente.')
        
        else:
            st.error('Email o contraseña incorrectos.')

elif opcion == 'Registrarse':
    nombre = st.text_input('Nombre')
    email = st.text_input('Email')
    password = st.text_input('Contraseña', type='password')
    if st.button('Registrarse'):
        registrar_usuario(nombre, email, password)
        st.success('Usuario registrado correctamente. Ahora puedes iniciar sesión.')
