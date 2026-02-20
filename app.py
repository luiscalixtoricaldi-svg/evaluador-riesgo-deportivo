import streamlit as st
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Datos simulados clínicos
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

st.title("Evaluador de Riesgo de Lesión Deportiva")

horas = st.number_input("Horas entrenamiento/semana", min_value=0.0)
rpe = st.number_input("RPE promedio (1-10)", min_value=0.0, max_value=10.0)
sueno = st.number_input("Horas sueño promedio", min_value=0.0)
lesion = st.selectbox("¿Lesión previa?", [0,1])
acwr = st.number_input("ACWR", min_value=0.0)

if st.button("Evaluar riesgo"):
    datos = [[horas,rpe,sueno,lesion,acwr]]
    resultado = modelo.predict(datos)[0]
    
    if resultado == "Alto":
        st.error("Riesgo ALTO → Reducir carga y evaluar preventivamente.")
    elif resultado == "Medio":
        st.warning("Riesgo MEDIO → Monitorizar fatiga y sueño.")
    else:
        st.success("Riesgo BAJO → Mantener planificación actual.")
