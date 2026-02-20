import streamlit as st
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import ListFlowable, ListItem
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
import datetime

# ===============================
# MODELO
# ===============================
X = np.array([
    [5,4,8,0,0.9],
    [12,8,6,1,1.5],
    [8,6,7,0,1.1],
    [15,9,5,1,1.7],
    [6,3,8,0,0.8],
    [10,7,6,1,1.4],
    [7,5,7,0,1.0],
    [14,9,5,1,1.8]
], dtype=np.float32)

y = np.array(["Bajo","Alto","Medio","Alto","Bajo","Alto","Medio","Alto"])

modelo = DecisionTreeClassifier(max_depth=3)
modelo.fit(X,y)

# ===============================
# INTERFAZ
# ===============================
st.set_page_config(page_title="Evaluador Clínico Deportivo", layout="centered")
st.title("Evaluador Clínico de Riesgo de Lesión")

st.subheader("Datos del deportista")

nombre = st.text_input("Nombre del deportista")
horas = st.number_input("Horas entrenamiento/semana", min_value=0.0)
rpe = st.number_input("RPE promedio (1-10)", min_value=0.0, max_value=10.0)
sueno = st.number_input("Horas sueño promedio", min_value=0.0)
lesion = st.selectbox("¿Lesión previa?", [0,1])
acwr = st.number_input("ACWR", min_value=0.0)

if st.button("Evaluar riesgo"):

    datos = [[horas,rpe,sueno,lesion,acwr]]
    resultado = modelo.predict(datos)[0]

    # ===============================
    # RECOMENDACIONES
    # ===============================
    if resultado == "Alto":
        recomendacion = """
        • Reducir carga externa 20–30%
        • Implementar trabajo preventivo neuromuscular
        • Monitorizar ACWR semanalmente
        • Evaluar calidad del sueño
        """
        st.error("Riesgo ALTO")
    elif resultado == "Medio":
        recomendacion = """
        • Ajustar microciclo
        • Monitorizar RPE diario
        • Trabajo preventivo específico
        """
        st.warning("Riesgo MEDIO")
    else:
        recomendacion = """
        • Mantener planificación
        • Control semanal de carga
        """
        st.success("Riesgo BAJO")

    st.markdown("### Recomendaciones clínicas:")
    st.write(recomendacion)

    # ===============================
    # REGISTRO
    # ===============================
    registro = {
        "Fecha": datetime.datetime.now(),
        "Nombre": nombre,
        "Horas": horas,
        "RPE": rpe,
        "Sueño": sueno,
        "Lesión previa": lesion,
        "ACWR": acwr,
        "Resultado": resultado
    }

    df = pd.DataFrame([registro])
    st.dataframe(df)

    # ===============================
    # GENERAR PDF
    # ===============================
    pdf = SimpleDocTemplate("informe_riesgo.pdf")
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Informe de Evaluación de Riesgo de Lesión", styles["Heading1"]))
    elements.append(Spacer(1, 0.5 * inch))

    for key, value in registro.items():
        elements.append(Paragraph(f"<b>{key}:</b> {value}", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Recomendaciones:</b>", styles["Heading2"]))
    elements.append(Paragraph(recomendacion, styles["Normal"]))

    pdf.build(elements)

    with open("informe_riesgo.pdf", "rb") as f:
        st.download_button("Descargar informe en PDF", f, file_name="informe_riesgo.pdf")
