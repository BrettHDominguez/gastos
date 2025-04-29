# app.py
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Seguimiento de Gastos", layout="centered")
st.title("📊 Seguimiento de Gastos Personales")

# Conexión a la base de datos
conn = sqlite3.connect('gastos.db', check_same_thread=False)
c = conn.cursor()

# Formulario para agregar nuevo gasto
with st.form("nuevo_gasto"):
    st.subheader("Agregar nuevo gasto")
    categoria = st.selectbox("Categoría", ["Alimentación", "Transporte", "Servicios", "Ocio", "Salud", "Otros"])
    monto = st.number_input("Monto", min_value=0.0, format="%.2f")
    descripcion = st.text_input("Descripción (opcional)")
    fecha = st.date_input("Fecha", value=datetime.today())
    submitted = st.form_submit_button("Agregar")

    if submitted:
        c.execute("INSERT INTO gastos (categoria, monto, descripcion, fecha) VALUES (?, ?, ?, ?)",
                  (categoria, monto, descripcion, fecha.strftime("%Y-%m-%d")))
        conn.commit()
        st.success("✅ Gasto agregado correctamente")

# Filtros
st.sidebar.header("🔍 Filtros")
categorias = [row[0] for row in c.execute("SELECT DISTINCT categoria FROM gastos").fetchall()]
fecha_min = c.execute("SELECT MIN(fecha) FROM gastos").fetchone()[0]
fecha_max = c.execute("SELECT MAX(fecha) FROM gastos").fetchone()[0]

categoria_filtro = st.sidebar.multiselect("Filtrar por categoría", categorias, default=categorias)
fecha_inicio = st.sidebar.date_input("Desde", value=pd.to_datetime(fecha_min) if fecha_min else datetime.today())
fecha_fin = st.sidebar.date_input("Hasta", value=pd.to_datetime(fecha_max) if fecha_max else datetime.today())

# Mostrar datos
query = f"""
SELECT * FROM gastos
WHERE categoria IN ({','.join('?' for _ in categoria_filtro)})
AND fecha BETWEEN ? AND ?
ORDER BY fecha DESC
"""
parametros = categoria_filtro + [fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d")]
df = pd.read_sql_query(query, conn, params=parametros)

st.subheader("📄 Historial de gastos")
st.dataframe(df)

# Resumen
st.subheader("📈 Resumen")
if not df.empty:
    resumen = df.groupby("categoria")["monto"].sum().reset_index()
    st.bar_chart(resumen.set_index("categoria"))
else:
    st.info("No hay datos para mostrar.")

conn.close()
