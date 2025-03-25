from openai import OpenAI
import streamlit as st
import pandas as pd
import re

# Inicializa el cliente de OpenAI
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="FinTracker 2.0", layout="centered")
st.title("📊 FinTracker 2.0 – Asistente Inteligente de Operaciones")

st.markdown("""
Sube un archivo de Excel con los datos de tus operaciones y hazle preguntas como:
- ¿Qué balances se han enviado?
- ¿Cuánto se adelantó en las referencias 00008, 00010 y 00046?
- ¿Muéstrame todas las operaciones que estén abiertas?
""")

uploaded_file = st.file_uploader("📁 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, dtype=str)
    st.subheader("Vista previa de la tabla")
    st.dataframe(df.head())

    pregunta = st.text_input("🤖 Escribe tu pregunta sobre el archivo cargado")

    if pregunta:
        try:
            # Pasa la tabla como contexto + la pregunta
            contexto = df.to_csv(index=False)
            full_prompt = f"""Tengo el siguiente archivo con datos de operaciones:

{contexto}

Responde a esta pregunta basada en el archivo anterior:
{pregunta}
"""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": full_prompt},
                ]
            )

            respuesta = response.choices[0].message.content
            st.success(respuesta)

        except Exception as e:
            st.error(f"❌ Error al consultar GPT:\n\n{str(e)}")
