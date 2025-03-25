import streamlit as st
import pandas as pd
import re
from openai import OpenAI

# Configura la app
st.set_page_config(page_title="FinTracker 2.0", layout="centered")
st.title("📊 FinTracker 2.0 – Asistente Inteligente de Operaciones")

st.markdown("""
Sube un archivo de Excel con los datos de tus operaciones y hazle preguntas como:
- ¿Qué balances se enviaron?
- ¿Cuánto se adelantó en las referencias 00008, 00010 y 00046?
- ¡Muéstrame todas las operaciones abiertas de un comprador!
""")

uploaded_file = st.file_uploader("📁 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, dtype=str)
    st.subheader("📋 Vista previa de la tabla")
    st.dataframe(df.head())

    pregunta = st.text_input("🤖 Escribe tu pregunta sobre el archivo cargado")

    if pregunta:
        # Intentar extraer un número de referencia tipo FR-1234 o similar
        match = re.search(r"FR-\d+", pregunta)

        if match:
            ref_number = match.group()
            fila = df[df["REFERENCE_NUMBER"] == ref_number]

            if not fila.empty:
                contexto = fila.to_string(index=False)

                try:
                    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "Eres un experto en operaciones financieras. Responde con precisión usando el contexto proporcionado."},
                            {"role": "user", "content": f"Con esta información:
{contexto}

¿Puedes decirme cuál es el late fee de la referencia {ref_number}?"}
                        ]
                    )
                    respuesta = response.choices[0].message.content
                    st.success(respuesta)
                except Exception as e:
                    st.error(f"Error al consultar GPT: {e}")
            else:
                st.warning(f"No se encontró la referencia {ref_number} en el archivo.")
        else:
            st.info("Por favor incluye un número de referencia válido en tu pregunta. Ej: FR-1234")

else:
    st.info("Por favor sube un archivo Excel para comenzar.")
