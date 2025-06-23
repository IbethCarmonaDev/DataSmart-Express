
import streamlit as st

def mostrar_kpis(df_kpis_tarjeta, df_tarjetas, plan):
    st.markdown("### 📌 Indicadores Financieros Clave")
    if not df_kpis_tarjeta.empty:
        col1, col2, col3, col4 = st.columns(4)
        for idx, (_, row) in enumerate(df_kpis_tarjeta.iterrows()):
            mensual = row["MENSUAL"]
            anual = row["ANUAL"]
            tipo = str(row.get("TIPO_DATO", "MONEDA")).upper()
            valor_mensual = f"{mensual:,.2f}%" if tipo == "PORCENTAJE" else f"$ {mensual:,.0f}"
            valor_anual = f"{anual:,.2f}%" if tipo == "PORCENTAJE" else f"$ {anual:,.0f}"
            [col1, col2, col3, col4][idx % 4].markdown(
                f"<div style='padding:10px'><strong>{row['GRUPO']}</strong><br>{valor_mensual}<br>📈 Acumulado: {valor_anual}</div>",
                unsafe_allow_html=True
            )
    if plan.upper() in df_tarjetas.columns:
        bloqueados = df_tarjetas[df_tarjetas[plan.upper()] != 1]["KPI"].tolist()
        if bloqueados:
            st.markdown("### 🔒 Indicadores disponibles en planes superiores")
            for kpi in bloqueados:
                st.markdown(f"- 🔒 {kpi}")
