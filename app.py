import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Control de Carga Científico", layout="wide")
st.title("Sistema Científico de Control de Carga")

archivo = "base_datos.csv"

if not os.path.exists(archivo):
    df = pd.DataFrame(columns=["Fecha","Nombre","Duracion","RPE","Carga"])
    df.to_csv(archivo, index=False)

df = pd.read_csv(archivo)

# ===============================
# REGISTRO
# ===============================
st.sidebar.header("Registrar sesión")

nombre = st.sidebar.text_input("Nombre del deportista")
duracion = st.sidebar.number_input("Duración (min)", min_value=0)
rpe = st.sidebar.slider("RPE", 1, 10)

if st.sidebar.button("Guardar sesión"):
    carga = duracion * rpe
    nueva_fila = {
        "Fecha": datetime.datetime.now(),
        "Nombre": nombre,
        "Duracion": duracion,
        "RPE": rpe,
        "Carga": carga
    }
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_csv(archivo, index=False)
    st.sidebar.success("Sesión guardada")

# ===============================
# ANÁLISIS
# ===============================
st.header("Análisis Científico")

if len(df["Nombre"].unique()) > 0:

    seleccionado = st.selectbox("Seleccionar deportista", df["Nombre"].unique())
    datos = df[df["Nombre"] == seleccionado]

    if len(datos) >= 7:

        ultimos_7 = datos.tail(7)["Carga"]
        ultimos_14 = datos.tail(14)["Carga"]

        carga_aguda = ultimos_7.mean()
        carga_cronica = datos.tail(28)["Carga"].mean()
        acwr = carga_aguda / carga_cronica if carga_cronica != 0 else 0

        monotonia = carga_aguda / ultimos_7.std() if ultimos_7.std() != 0 else 0
        strain = carga_aguda * monotonia

        semana_actual = ultimos_7.sum()
        semana_previa = ultimos_14.head(7).sum() if len(ultimos_14) >= 14 else 0

        tendencia = semana_actual - semana_previa

        col1, col2, col3 = st.columns(3)
        col1.metric("ACWR", round(acwr,2))
        col2.metric("Monotonía", round(monotonia,2))
        col3.metric("Strain", round(strain,2))

        # ===============================
        # INTERPRETACIÓN
        # ===============================
        st.subheader("Interpretación Clínica")

        if acwr > 1.5:
            st.error("🔴 ACWR elevado → riesgo alto")
        elif 1.2 < acwr <= 1.5:
            st.warning("🟡 ACWR moderado")
        else:
            st.success("🟢 ACWR dentro zona óptima (0.8–1.2 ideal)")

        if monotonia > 2:
            st.warning("Monotonía alta → poca variabilidad de carga")
        
        if strain > 6000:
            st.warning("Strain elevado → alto estrés acumulado")

        if tendencia > 1000:
            st.warning("Incremento brusco de carga semanal")
        elif tendencia < -1000:
            st.info("Disminución marcada de carga")

        # ===============================
        # GRÁFICO
        # ===============================
        fig, ax = plt.subplots()
        ax.plot(datos["Carga"].values)
        ax.set_title("Evolución de Carga")
        ax.set_xlabel("Sesiones")
        ax.set_ylabel("Carga sRPE")
        st.pyplot(fig)

    else:
        st.info("Necesitas al menos 7 sesiones registradas para análisis científico.")
