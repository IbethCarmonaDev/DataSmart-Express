# interfaz_planes.py
import streamlit as st
import pandas as pd
from core.configuracion import obtener_parametros

def mostrar_interfaz_planes(ruta_parametros: str):
    st.title("🧩 Planes de Suscripción - DataSmart Express")
    st.markdown("Consulta las funcionalidades incluidas en cada plan y elige el que más se adapte a tus necesidades.")

    # --- Cargar hojas ---
    df_func1 = obtener_parametros('PLANES', ruta_parametros)
    df_func2 = obtener_parametros('EN_ANALISIS', ruta_parametros)
    df_info = obtener_parametros('PLANES_INFO', ruta_parametros)

    # --- Validar estructura ---
    if 'DESCRIPCION' not in df_func1.columns or 'DESCRIPCION' not in df_func2.columns:
        st.error("❌ Las hojas deben tener la columna 'DESCRIPCION'.")
        return

    # --- Unificar funcionalidades ---
    df_func1 = df_func1.rename(columns={'FUNCIONALIDAD': 'FUNCION'})
    df_func2 = df_func2.rename(columns={'Funcionalidad': 'FUNCION'})
    df_union = pd.concat([df_func1, df_func2], ignore_index=True)

    # --- Detectar planes en orden original ---
    columnas_totales = df_union.columns.tolist()
    columnas_planes = [col for col in columnas_totales if col not in ['FUNCION', 'DESCRIPCION', 'ORDEN', 'Premium_trial']]
    columnas_planes_ordenadas = [p for p in columnas_planes if p]  # limpia nulos

    # --- Limpiar y preparar ---
    df_union[columnas_planes_ordenadas] = df_union[columnas_planes_ordenadas].fillna(0).astype(int)
    df_union['ORDEN'] = range(len(df_union))
    df_union = df_union.sort_values('ORDEN')

    # --- Mostrar tabla comparativa ---
    st.subheader("📊 Comparativa general de funcionalidades")

    df_visual = df_union[['DESCRIPCION'] + columnas_planes_ordenadas].copy()
    df_visual = df_visual.rename(columns={"DESCRIPCION": "Funcionalidad"})
    df_visual[columnas_planes_ordenadas] = df_visual[columnas_planes_ordenadas].replace({1: "✅", 0: "❌"})

    st.dataframe(df_visual.set_index("Funcionalidad"), use_container_width=True)

    # --- Mostrar descripción por plan comercial ---
    st.subheader("💳 Elige tu plan ideal")

    for _, row in df_info.iterrows():
        plan = row['PLAN']
        if plan not in columnas_planes_ordenadas:
            continue  # ignorar si no está en columnas funcionales

        col1, col2 = st.columns([3, 1])
        with col1:
            #precio = f"${int(row['PRECIO_COP']):,} COP".replace(",", ".")

            moneda = row['MONEDA'].strip().upper()
            precio = row['PRECIO']

            if moneda == "COP":
                precio_str = f"${int(precio):,} COP".replace(",", ".")
            elif moneda == "USD":
                precio_str = f"${precio:.2f} USD"
            else:
                precio_str = f"{precio} {moneda}"

            st.markdown(f"### ✨ Plan {plan}")
            #st.markdown(f"💵 **{precio} / {int(row['DURACION_DIAS'])} días**")
            st.markdown(f"💵 **{precio_str} / {int(row['DURACION_DIAS'])} días**")
            st.markdown(f"📝 _{row['DESCRIPCION CORTA']}_")

            beneficios = df_union[df_union[plan] == 1]["DESCRIPCION"].tolist()
            for b in beneficios[:6]:
                st.markdown(f"- {b.strip()}")
            if len(beneficios) > 6:
                st.markdown("...y más funcionalidades")


        with col2:
            st.button(f"Suscribirme a {plan}", key=f"btn_{plan.lower()}")

