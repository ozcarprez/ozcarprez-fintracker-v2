import streamlit as st
import pandas as pd
import openai
import re

# API key desde secrets.toml (configurado en Streamlit Cloud)
openai.api_key = st.secrets["openai"]["api_key"]

st.set_page_config(page_title="FinTracker 2.0", layout="centered")
st.title("📊 FinTracker 2.0 – Asistente Inteligente de Operaciones")

st.markdown("""
Sube un archivo de Excel con los datos de tus operaciones y hazle preguntas como:
- ¿Qué balances envió el vendedor X?
- ¿Cuánto se adelantó en las referencias 00008, 00010 y 00046?
- Muéstrame todas las operaciones del comprador Y que estén abiertas.
""")

uploaded_file = st.file_uploader("📁 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, dtype=str)
    st.subheader("📊 Vista previa de la tabla")
    st.dataframe(df.head())

    pregunta = st.text_input("🤖 Escribe tu pregunta sobre el archivo cargado")

    if pregunta:
        try:
            # Convertimos el DataFrame a texto (puedes limitar columnas si gustas)
            context = df.to_csv(index=False)

            prompt = f"""
Tengo esta tabla con datos de operaciones:

{context}

Ahora responde a esta pregunta basada solo en la tabla:
{pregunta}
"""

            with st.spinner("Consultando GPT..."):
                respuesta = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un asistente experto en análisis de operaciones. Responde con datos exactos de la tabla, sin inventar nada."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )

                mensaje = respuesta["choices"][0]["message"]["content"]
                st.success("✅ Respuesta de GPT:")
                st.write(mensaje)

        except Exception as e:
            st.error(f"❌ Error al consultar GPT:\n\n{e}")
