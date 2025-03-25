import streamlit as st
import pandas as pd
import re
from openai import OpenAI

# Configura tu clave API desde los secretos de Streamlit
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="FinTracker 2.0", layout="centered")
st.title("📊 FinTracker 2.0 - Asistente Inteligente de Operaciones")

st.markdown("""
Sube un archivo de Excel con los datos de tus operaciones y hazle preguntas como:
- ¿Qué balances están pendientes por enviar?
- ¿Cuánto se adelantó en las referencias 00008, 00010 y 00046?
- Muéstrame todas las operaciones de cierto comprador que estén abiertas.
""")

uploaded_file = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, dtype=str)
    st.subheader("Vista previa de la tabla")
    st.dataframe(df.head())

    pregunta = st.text_input("🤖 Escribe tu pregunta sobre el archivo cargado")

    if pregunta:
        try:
            df.columns = df.columns.str.upper().str.strip()
            contenido_tabla = df.head(30).to_markdown(index=False)  # Limita filas para evitar error de tokens

            mensaje = f"""Con esta información:

{contenido_tabla}

Responde la siguiente pregunta:
{pregunta}
"""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": mensaje},
                ]
            )

            respuesta = response.choices[0].message.content
            st.success("Respuesta de GPT:")
            st.markdown(respuesta)

        except Exception as e:
            st.error(f"❌ Error al consultar GPT:\n{e}")
