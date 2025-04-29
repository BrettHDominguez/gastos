import sqlite3
import streamlit as st
import pandas as pd

# Conexión a la base de datos
def obtener_conexion():
    conn = sqlite3.connect('gastos.db')
    return conn

# Registrar un nuevo usuario
def registrar_usuario(nombre, email, password):
    conn = obtener_conexion()
    c = conn.cursor()
    
    # Insertar el nuevo usuario
    try:
        c.execute('INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)', (nombre, email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("El correo electrónico ya está registrado.")
    finally:
        conn.close()

# Verificar si un usuario existe
def verificar_usuario(email, password):
    conn = obtener_conexion()
    c = conn.cursor()
    
    c.execute('SELECT id FROM usuarios WHERE email = ? AND password = ?', (email, password))
    usuario = c.fetchone()
    conn.close()
    return usuario

# Agregar un gasto
def agregar_gasto(categoria, monto, descripcion, fecha, usuario_id):
    conn = obtener_conexion()
    c = conn.cursor()
    
    c.execute('INSERT INTO gastos (categoria, monto, descripcion, fecha, usuario_id) VALUES (?, ?, ?, ?, ?)', 
              (categoria, monto, descripcion, fecha, usuario_id))
    conn.commit()
    conn.close()

# Mostrar los gastos de un usuario
def mostrar_gastos(usuario_id):
    conn = obtener_conexion()
    c = conn.cursor()
    
    c.execute('SELECT categoria, monto, descripcion, fecha FROM gastos WHERE usuario_id = ?', (usuario_id,))
    gastos = c.fetchall()
    
    conn.close()
    return gastos

# Función principal de la app
def main():
    st.title("Seguimiento de Gastos Personales")

    menu = ["Iniciar sesión", "Registrar"]
    opcion = st.sidebar.selectbox("Elige una opción", menu)

    if opcion == "Registrar":
        st.subheader("Registro de Usuario")
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Registrar"):
            registrar_usuario(nombre, email, password)
            st.success("Usuario registrado con éxito. Ahora puedes iniciar sesión.")

    elif opcion == "Iniciar sesión":
        st.subheader("Iniciar sesión")
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar sesión"):
            usuario = verificar_usuario(email, password)
            
            if usuario:
                st.success(f"Bienvenido, {email}!")
                usuario_id = usuario[0]
                
                # Mostrar gastos
                st.subheader("Agregar Gasto")
                categoria = st.text_input("Categoría del gasto")
                monto = st.number_input("Monto", min_value=0.0)
                descripcion = st.text_area("Descripción")
                fecha = st.date_input("Fecha", format="YYYY-MM-DD")
                
                if st.button("Agregar gasto"):
                    agregar_gasto(categoria, monto, descripcion, fecha, usuario_id)
                    st.success("Gasto agregado con éxito.")
                
                # Mostrar lista de gastos
                st.subheader("Tus Gastos")
                gastos = mostrar_gastos(usuario_id)
                if gastos:
                    df = pd.DataFrame(gastos, columns=["Categoría", "Monto", "Descripción", "Fecha"])
                    st.dataframe(df)
                else:
                    st.info("No tienes gastos registrados.")
            else:
                st.error("Credenciales incorrectas. Intenta de nuevo.")

if __name__ == "__main__":
    main()
