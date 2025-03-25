import streamlit as st
import pandas as pd
import openai
import re

# Configuración de la página
st.set_page_config(page_title="FinTracker GPT", layout="centered")
st.title("📊 FinTracker + GPT - Asistente Inteligente de Operaciones")

# Configurar la API Key desde los secrets
gpt_key = st.secrets["openai"]["api_key"]
openai.api_key = gpt_key

# Subir archivo Excel
st.markdown("""
Sube un archivo de Excel con los datos de tus operaciones y hazle preguntas como:
- ¿Cuál fue el adelanto de la referencia 00008?
- ¿Cuáles operaciones tiene el comprador X abiertas?
- ¿Muéstrame todas las referencias con un fee de atraso mayor a $500
""")

uploaded_file = st.file_uploader("📁 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, dtype=str)
    st.subheader("Vista previa de la tabla")
    st.dataframe(df.head())

    pregunta = st.text_input("🤖 Escribe tu pregunta sobre el archivo cargado")

    if pregunta:
        with st.spinner("Pensando..."):
            # Armar prompt para el modelo
            prompt = f"""
Eres un experto en analizar archivos de Excel con datos financieros. Con base en la siguiente tabla, responde la pregunta del usuario de forma concisa, clara y en español.

Tabla:
{df.head(30).to_string(index=False)}

Pregunta del usuario:
{pregunta}
"""

            try:
                respuesta = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un analista financiero que ayuda a leer datos de Excel"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=400
                )

                st.success("Respuesta generada:")
                st.write(respuesta.choices[0].message.content)

            except Exception as e:
                st.error(f"Error al consultar GPT: {e}")
