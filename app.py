
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="FinTracker 2.0", layout="centered")
st.title("📊 FinTracker 2.0 – Asistente Inteligente de Operaciones")

st.markdown("""
Sube un archivo de Excel con los datos de tus operaciones y hazle preguntas como:
- ¿Qué balances envió Alfredo Belmonte Torres?
- ¿Cuánto se adelantó en las referencias 00008, 00010 y 00046?
- Muéstrame todas las operaciones de Exceptional Future que estén abiertas.
""")

uploaded_file = st.file_uploader("📁 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, dtype=str)
    df.columns = df.columns.str.upper()
    df["REFERENCE_NUMBER"] = df["REFERENCE_NUMBER"].astype(str).str.zfill(5)
    
    st.subheader("Vista previa de la tabla")
    st.dataframe(df.head())

    pregunta = st.text_input("🤖 Escribe tu consulta")

    if pregunta:
        pregunta = pregunta.lower()

        resultados = pd.DataFrame()
        total_balance = 0

        # Buscar por vendedor
        vendedores = df["SELLER_NAME"].dropna().unique()
        for nombre in vendedores:
            if nombre.lower() in pregunta:
                resultados = df[df["SELLER_NAME"].str.lower() == nombre.lower()]
                break

        # Buscar por comprador si no hubo resultado por vendedor
        if resultados.empty:
            compradores = df["BUYER_NAME"].dropna().unique()
            for nombre in compradores:
                if nombre.lower() in pregunta:
                    resultados = df[df["BUYER_NAME"].str.lower() == nombre.lower()]
                    break

        # Buscar por múltiples referencias si hay números
        if resultados.empty:
            ref_matches = re.findall(r"\d{2,5}", pregunta)
            if ref_matches:
                ref_nums = [r.zfill(5) for r in ref_matches]
                resultados = df[df["REFERENCE_NUMBER"].isin(ref_nums)]

        # Buscar por estado (open/closed)
        if resultados.empty and "open" in pregunta:
            resultados = df[df["STATE"].str.lower() == "open"]
        elif resultados.empty and "closed" in pregunta:
            resultados = df[df["STATE"].str.lower() == "closed"]

        if resultados.empty:
            st.warning("No encontré resultados para tu consulta.")
        else:
            mostrar = resultados[["REFERENCE_NUMBER", "SELLER_NAME", "BUYER_NAME", "TOTAL_ADVANCE_AMOUNT", "LIQUIDATION_BALANCE_RETURNED", "STATE"]].copy()
            mostrar.columns = ["Referencia", "Vendedor", "Comprador", "Monto Adelantado", "Balance Enviado", "Estado"]

            st.success("Resultados encontrados:")
            st.dataframe(mostrar)

            # Calcular total
            try:
                mostrar["Balance Enviado"] = mostrar["Balance Enviado"].replace('[\$,]', '', regex=True).astype(float)
                total = mostrar["Balance Enviado"].sum()
                st.markdown(f"### 🪙 Total balance enviado: ${total:,.2f}")
            except:
                st.info("No se pudo calcular el total porque los valores no están en formato numérico.")

            # Botón de descarga
            csv = mostrar.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar resultados como CSV",
                data=csv,
                file_name="resultados_fintracker.csv",
                mime="text/csv"
            )
