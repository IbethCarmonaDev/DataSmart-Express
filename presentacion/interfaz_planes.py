import streamlit as st
import pandas as pd
from core.configuracion import obtener_parametros

def mostrar_interfaz_planes(ruta_parametros: str):
    st.title("🧩 Planes de Suscripción - DataSmart Express")
    st.markdown("Consulta las funcionalidades incluidas en cada plan y elige el que más se adapte a tus necesidades.")

    # Leer hojas de funcionalidades
    df_func1 = obtener_parametros('PLANES', ruta_parametros)
    df_func2 = obtener_parametros('EN_ANALISIS', ruta_parametros)
    df_info = obtener_parametros('PLANES_INFO', ruta_parametros)

    if 'DESCRIPCION' not in df_func1.columns or 'DESCRIPCION' not in df_func2.columns:
        st.error("❌ Asegúrate de tener la columna 'DESCRIPCION' en las hojas PLANES y EN_ANALISIS.")
        return

    # Preparar funcionalidades
    df_func1 = df_func1.rename(columns={'FUNCIONALIDAD': 'FUNCION'})
    df_func2 = df_func2.rename(columns={'Funcionalidad': 'FUNCION'})
    df_union = pd.concat([df_func1, df_func2], ignore_index=True)

    # Detectar los planes dinámicamente (evita Free y Premium_trial)
    columnas_planes = df_union.columns.difference(['FUNCION', 'DESCRIPCION']).tolist()
    columnas_planes = [p for p in columnas_planes if p not in ['Premium_trial']]
    df_union[columnas_planes] = df_union[columnas_planes].fillna(0).astype(int)

    # Reordenar funcionalidades según orden de aparición en Excel
    df_union['ORDEN'] = range(len(df_union))
    df_union = df_union.sort_values('ORDEN')

    # Mostrar tabla comparativa
    st.subheader("📊 Comparativa general de funcionalidades")
    df_visual = df_union[['DESCRIPCION'] + columnas_planes].copy()
    df_visual = df_visual.rename(columns={"DESCRIPCION": "Funcionalidad"})
    df_final = df_visual.set_index("Funcionalidad").T
    df_final = df_final.replace({1: "✅", 0: "❌"})
    st.dataframe(df_final, use_container_width=True)

    # Mostrar resumen de cada plan (comerciales)
    st.subheader("💳 Elige tu plan ideal")

    for _, row in df_info.iterrows():
        plan = row['PLAN']
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### ✨ Plan {plan}")
            st.markdown(f"💵 **${row['PRECIO_USD']:.2f} USD / {int(row['DURACION_DIAS'])} días**")
            st.markdown(f"📝 _{row['DESCRIPCION CORTA']}_")

            # Mostrar hasta 6 funcionalidades clave
            if plan in df_union.columns:
                beneficios = df_union[df_union[plan] == 1]["DESCRIPCION"].tolist()
                for b in beneficios[:6]:
                    st.markdown(f"- {b.strip()}")
                if len(beneficios) > 6:
                    st.markdown("...y más funcionalidades")
        with col2:
            st.button(f"Suscribirme a {plan}", key=f"btn_{plan.lower()}")
