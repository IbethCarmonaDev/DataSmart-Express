import streamlit as st
import pandas as pd
from analisis_estado_resultados import generar_estado_resultados_detallado, generar_estado_resultados_todos_los_meses
from analisis_lenguaje import generar_conclusiones
from analisis_avanzado import generar_conclusiones_avanzadas, generar_tabla_comparativa_html
from PIL import Image

def generar_html_estado_resultados(df, df_kpis_tarjeta):
    tipo_kpis = {row["GRUPO"]: str(row.get("TIPO_DATO", "MONEDA")).upper() for _, row in df_kpis_tarjeta.iterrows()}
    def formatear(valor, grupo):
        tipo = tipo_kpis.get(grupo, "MONEDA")
        if pd.isnull(valor): return ""
        if tipo == "PORCENTAJE": return f"{valor:.2f}%"
        elif tipo == "DECIMAL": return f"{valor:.2f}"
        else: return f"$ {valor:,.0f}"

    df = df.copy()
    if "AÑO" in df.columns: df.drop(columns=["AÑO"], inplace=True)
    if "MES" in df.columns: df.drop(columns=["MES"], inplace=True)

    html = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
            text-align: center;
        }
        td:nth-child(1), td:nth-child(2) {
            text-align: left;
        }
        td:nth-child(3), td:nth-child(4) {
            text-align: right;
        }
    </style>
    <table>
        <thead>
            <tr>
                <th>Grupo</th>
                <th>Cuenta</th>
                <th>Mensual</th>
                <th>Anual</th>
            </tr>
        </thead>
        <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>"
        html += f"<td>{row.get('GRUPO', '')}</td>"
        html += f"<td>{row.get('CUENTA', '')}</td>"
        html += f"<td>{formatear(row.get('MENSUAL', ''), row.get('GRUPO', ''))}</td>"
        html += f"<td>{formatear(row.get('ANUAL', ''), row.get('GRUPO', ''))}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html

st.set_page_config(page_title="DataSmart Express", layout="wide")

# Mostrar logo si existe
try:
    logo = Image.open("Logo.png")
    st.image(logo, width=200)
except:
    st.write("")

st.markdown("## 📈 DataSmart Express", unsafe_allow_html=True)
st.markdown("_Estado de Resultados Inteligente con KPIs Financieros_", unsafe_allow_html=True)

archivo_datos = st.file_uploader("🗅️ Carga el archivo de datos", type=["xlsx"])
archivo_parametros = st.file_uploader("⚙️ Carga el archivo de parámetros", type=["xlsx"])

if archivo_datos and archivo_parametros:
    df_datos = pd.read_excel(archivo_datos, sheet_name=0)
    df_parametros = archivo_parametros

    año = st.selectbox("1⃣ Selecciona el año", sorted(df_datos["AÑO"].unique(), reverse=True))
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    mes_nombre = st.selectbox("2⃣ Selecciona el mes", list(meses.values()))
    mes = list(meses.keys())[list(meses.values()).index(mes_nombre)]

    centros = ["TODOS"] + sorted(df_datos["CENTRO_COSTOS"].dropna().unique())
    centro = st.selectbox("3⃣ Selecciona centro de costos (opcional)", centros)

    # Solo se genera una vez cuando se cargan los archivos o cambia el año
    if "estado_todos" not in st.session_state or st.session_state.get("año_actual") != año:
        st.session_state.estado_todos = generar_estado_resultados_todos_los_meses(df_datos, df_parametros, centro)
        st.session_state.año_actual = año

    df_estado, df_kpis = generar_estado_resultados_detallado(df_datos, df_parametros, año, mes, centro)
    df_estado["AÑO"] = año
    df_estado["MES"] = mes

    st.markdown("### 📌 Indicadores Financieros Clave", unsafe_allow_html=True)
    if not df_kpis.empty:
        col1, col2, col3, col4 = st.columns(4)
        columnas = [col1, col2, col3, col4]
        for idx, (_, row) in enumerate(df_kpis.iterrows()):
            mensual = row["MENSUAL"]
            anual = row["ANUAL"]
            tipo = str(row.get("TIPO_DATO", "MONEDA")).upper()

            if tipo == "PORCENTAJE":
                valor_mensual = f"{mensual:,.2f}%"
                valor_anual = f"{anual:,.2f}%"
            elif tipo == "DECIMAL":
                valor_mensual = f"{mensual:,.2f}"
                valor_anual = f"{anual:,.2f}"
            else:
                valor_mensual = f"$ {mensual:,.0f}"
                valor_anual = f"$ {anual:,.0f}"

            columnas[idx % 4].markdown(
                f"""
                <div style='background-color:#f8f9fa; padding:15px; border-radius:10px;
                            box-shadow: 2px 2px 6px rgba(0,0,0,0.05); margin-bottom:10px'>
                    <h5 style='margin-bottom:0px;'>{row['GRUPO']}</h5>
                    <h2 style='margin:5px 0; color:#0066cc'>{valor_mensual}</h2>
                    <p style='margin:0; font-size:16px; color:#2e8b57; font-weight:600'>
                        📈 Acumulado: {valor_anual}
                    </p>
                </div>
                """, unsafe_allow_html=True
            )

    st.markdown("---", unsafe_allow_html=True)
    st.markdown("### 👀 Análisis en Lenguaje Natural", unsafe_allow_html=True)
    st.markdown(generar_conclusiones(df_kpis), unsafe_allow_html=True)

    st.markdown("### 🚀 Análisis Avanzado")
    df_comparativo, resumen_avanzado = generar_conclusiones_avanzadas(df_kpis, st.session_state.estado_todos, archivo_parametros, año, mes)
    st.markdown(generar_tabla_comparativa_html(df_comparativo), unsafe_allow_html=True)
    st.markdown(resumen_avanzado, unsafe_allow_html=True)

    st.markdown("---", unsafe_allow_html=True)
    st.markdown("### 📜 Estado de Resultados Detallado", unsafe_allow_html=True)
    def aplicar_formato(df, df_kpis_tarjeta):
        tipo_kpis = {row["GRUPO"]: str(row.get("TIPO_DATO", "MONEDA")).upper() for _, row in df_kpis_tarjeta.iterrows()}
        def formatear(valor, grupo):
            tipo = tipo_kpis.get(grupo, "MONEDA")
            if pd.isnull(valor): return ""
            if tipo == "PORCENTAJE": return f"{valor:.2f}%"
            elif tipo == "DECIMAL": return f"{valor:.2f}"
            else: return f"$ {valor:,.0f}"
        df_formateado = df.copy()
        for col in ["MENSUAL", "ANUAL"]:
            df_formateado[col] = df_formateado.apply(lambda row: formatear(row[col], row["GRUPO"]), axis=1)
        if "AÑO" in df_formateado.columns:
            df_formateado.drop(columns=["AÑO"], inplace=True)
        if "MES" in df_formateado.columns:
            df_formateado.drop(columns=["MES"], inplace=True)
        return df_formateado.style.set_properties(
            subset=["MENSUAL", "ANUAL"],
            **{"text-align": "right"}
        ).set_table_styles(
            [{'selector': 'th', 'props': [('text-align', 'center')]}]
        )

    df_estado_formateado = aplicar_formato(df_estado, df_kpis)
    st.markdown(generar_html_estado_resultados(df_estado, df_kpis), unsafe_allow_html=True)
