import streamlit as st
import pandas as pd
import openai
import re

st.set_page_config(page_title="FinTracker 2.0", layout="centered")
st.title("📊 FinTracker 2.0 – Asistente Inteligente de Operaciones")

st.markdown("""
Sube un archivo de Excel con los datos de tus operaciones y hazle preguntas como:
- ¿Qué balances se han enviado?
- ¿Cuánto se adelantó en las referencias 00008, 00010 y 00046?
- Muéstrame todas las operaciones de un comprador que estén abiertas.
""")

uploaded_file = st.file_uploader("📁 Sube tu archivo Excel", type=["xlsx"])

def responder_con_gpt(pregunta, contexto):
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    respuesta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente que responde preguntas sobre operaciones financieras basadas en tablas de Excel."},
            {"role": "user", "content": f"Tabla:\n{contexto}\n\nPregunta: {pregunta}"}
        ]
    )
    return respuesta.choices[0].message.content.strip()

if uploaded_file:
    df = pd.read_excel(uploaded_file, dtype=str)
    st.subheader("📄 Vista previa de la tabla")
    st.dataframe(df.head())

    pregunta = st.text_input("🤖 Escribe tu pregunta sobre el archivo cargado")

    if pregunta:
        with st.spinner("Consultando GPT..."):
            try:
                contexto = df.head(20).to_string(index=False)  # Puedes ajustar la cantidad de filas si es necesario
                respuesta = responder_con_gpt(pregunta, contexto)
                st.success(respuesta)
            except Exception as e:
                st.error(f"Error al consultar GPT: {e}")
