# interfaz_planes.py
import streamlit as st
import pandas as pd
from core.configuracion import obtener_parametros

def mostrar_interfaz_planes(ruta_parametros: str):
    st.title("🧩 Planes de Suscripción - DataSmart Express")
    st.markdown("Consulta las funcionalidades incluidas en cada plan y elige el que más se adapte a tus necesidades.")

    # Leer hojas desde Excel
    df_planes_func = obtener_parametros('PLANES', ruta_parametros)
    df_planes_analisis = obtener_parametros('EN_ANALISIS', ruta_parametros)

    # Validar columnas esperadas
    if 'DESCRIPCION' not in df_planes_func.columns or 'DESCRIPCION' not in df_planes_analisis.columns:
        st.error("❌ Las hojas PLANES y EN_ANALISIS deben tener una columna llamada 'DESCRIPCION'.")
        return

    # Unificar estructura
    df_planes_func = df_planes_func.rename(columns={"FUNCIONALIDAD": "FUNCION"}).copy()
    df_planes_analisis = df_planes_analisis.rename(columns={"Funcionalidad": "FUNCION"}).copy()
    df_union = pd.concat([df_planes_func, df_planes_analisis], ignore_index=True)

    # Detectar columnas que son planes (quitar columnas técnicas)
    columnas_planes = df_union.columns.difference(['FUNCION', 'DESCRIPCION']).tolist()
    columnas_planes = [col for col in columnas_planes if col not in ['Premium_trial']]  # ocultar Premium_trial

    # Asegurar que estén como int
    df_union[columnas_planes] = df_union[columnas_planes].fillna(0).astype(int)

    # Armar visualización
    df_visual = df_union[['DESCRIPCION'] + columnas_planes].copy()
    df_visual = df_visual.rename(columns={"DESCRIPCION": "Funcionalidad"})

    # Transponer: Planes como columnas
    df_final = df_visual.set_index("Funcionalidad").T
    df_final = df_final.replace({1: "✅", 0: "❌"})

    st.subheader("📊 Comparativa general de funcionalidades")
    st.dataframe(df_final, use_container_width=True)

    # Mostrar resumen y botón por cada plan (excepto Free)
    st.subheader("💳 Elige tu plan ideal")
    planes_comerciales = [p for p in columnas_planes if p != "Free"]

    for plan in planes_comerciales:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### ✨ Plan {plan}")
            st.markdown("**Incluye:**")
            beneficios = df_union[df_union[plan] == 1]["DESCRIPCION"].tolist()
            for b in beneficios[:6]:
                st.markdown(f"- {b.strip()}")
            if len(beneficios) > 6:
                st.markdown("...y más funcionalidades")
        with col2:
            st.button(f"Suscribirme a {plan}", key=f"btn_{plan.lower()}")
