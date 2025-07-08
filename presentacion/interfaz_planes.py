# interfaz_planes.py
import streamlit as st
import pandas as pd
from configuracion import obtener_parametros  # Tu lector de Excel

def mostrar_interfaz_planes():
    st.title("🧩 Planes de Suscripción - DataSmart Express")
    st.markdown("Consulta las funcionalidades incluidas en cada plan y elige el que más se adapte a tus necesidades.")

    # Leer hojas de Excel
    df_planes_func = obtener_parametros('PLANES')
    df_planes_analisis = obtener_parametros('EN_ANALISIS')

    # Validar que ambas hojas tengan columna DESCRIPCION
    if 'DESCRIPCION' not in df_planes_func.columns or 'DESCRIPCION' not in df_planes_analisis.columns:
        st.error("❌ Asegúrate de agregar una columna llamada 'DESCRIPCION' en las hojas PLANES y EN_ANALISIS.")
        return

    # Unificar columnas y estandarizar
    df_planes_func = df_planes_func.rename(columns={"FUNCIONALIDAD": "FUNCION"}).copy()
    df_planes_analisis = df_planes_analisis.rename(columns={"Funcionalidad": "FUNCION"}).copy()

    # Concatenar ambas hojas en una sola tabla
    df_union = pd.concat([df_planes_func, df_planes_analisis], ignore_index=True)

    # Reemplazar NaN con ceros y asegurar que los valores de planes sean enteros
    planes_disponibles = ['Free', 'Basico', 'Pro', 'Premium', 'Premium_trial']
    df_union[planes_disponibles] = df_union[planes_disponibles].fillna(0).astype(int)

    # Mostrar tabla comparativa transpuesta
    st.subheader("📊 Comparativa general de funcionalidades")
    df_visual = df_union[['DESCRIPCION'] + planes_disponibles].copy()
    df_visual = df_visual.rename(columns={"DESCRIPCION": "Funcionalidad"})
    df_comparativa = df_visual.set_index("Funcionalidad").T.reset_index().rename(columns={"index": "PLAN"})
    df_comparativa = df_comparativa.replace({1: "✅", 0: "❌"})
    st.dataframe(df_comparativa, use_container_width=True)

    # Mostrar sección por plan
    st.subheader("💳 Elige tu plan ideal")
    for plan in ['Basico', 'Pro', 'Premium']:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### ✨ Plan {plan}")
            st.markdown("**Incluye:**")
            beneficios = df_union[df_union[plan] == 1]["DESCRIPCION"].tolist()
            for b in beneficios[:6]:  # Mostrar solo 6 por ahora
                st.markdown(f"- {b.strip()}")
            if len(beneficios) > 6:
                st.markdown("...y más funcionalidades")
        with col2:
            st.button(f"Suscribirme a {plan}", key=f"btn_{plan.lower()}")

